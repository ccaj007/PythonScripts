#!/usr/bin/env python3
r"""
Command-line script for bulk update of wheel permissions
Usage:

# Add multiple users to a surface on dev wheel
./wheel-perms.py add-permissions  -w wheel-oil-dev -u 'MAVEN\james.borne' -u 'henry.mulherin' -s WTI-MACRO

# Remove user from all ES-JR surfaces
./wheel-perms.py rem-permissions -u 'henry.mulherin' -s 'ES-JR*'

# List all prod wheel surfaces a user has permission on
./wheel-perms.py list-permissions -u 'henry.mulherin'

# List all prod wheel instances
./wheel-perms.py list-wheels

# List all surfaces that are part of Index desk
./wheel-perms.py list-surfaces -d 'Index'


"""
import os
import re
import sys
import json
import argparse
import requests
import click
import logging
#import ldap3
import fnmatch

logger = logging.getLogger(__name__)


DEFAULT_WHEEL_INSTANCES = sorted([
    "wheel-longend",
    "wheel-shortend",
    "wheel-shortend-us",
    "wheel-index",
    "wheel-oil",
    "wheel-metals",
    "wheel-index-chi",
    "wheel-index-us",
    "wheel-treasuries",
])
KEYCLOAK_TOKEN = os.environ.get('KEYCLOAK_TOKEN')
KEYCLOAK_TOKEN_DEV = os.environ.get('KEYCLOAK_TOKEN_DEV')

SESSION = requests.Session()

def request(method, url, data=None):
    headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json-patch+json',
            'User-Agent': 'wheel-perms.py',
    }
    if method != 'GET':
        if '-dev.mavensecurities.com' in url:
            assert KEYCLOAK_TOKEN_DEV, "No KEYCLOAK_TOKEN_DEV Token Provided"
            headers["Authorization"] = f"Bearer {KEYCLOAK_TOKEN_DEV}"
        else:
            assert KEYCLOAK_TOKEN, "No KEYCLOAK_TOKEN Token Provided"
            headers["Authorization"] = f"Bearer {KEYCLOAK_TOKEN}"

    response = None
    try:
        req = SESSION.request(method, url, 
            headers=headers,
            data=(json.dumps(data) if data is not None else data),
            timeout=(1.05, 5)
        )
        try:
            response = req.json()
        except:
            response = req.text

        if req.status_code != 200:
            # Not successful print debug
            print (f">> [{req.status_code}] {method} {url}")
            print (">> " + re.sub(r"\n", "\n>> ", json.dumps(data, indent=3)))
            print (f"<< [{req.status_code}]")
            print (f"<< {response}")

        req.raise_for_status()
    except Exception as e:
        logger.error(f"{method} {url} FAILED: {e}")
        sys.exit(1)

    return response

def request_get(url):
    """Helper GET Method"""
    return request('GET', url)

def ldap_lookup_user(username):
    AD_BIND_USER = 'svcCompliance@mavensecurities.com'
    AD_BIND_PWD = '0rangeSausage'
    ldap_server = ldap3.Server('ldap://ixwdc01.mavensecurities.com')
    ldap_conn = ldap3.Connection(ldap_server, AD_BIND_USER, AD_BIND_PWD, read_only=True)

    with ldap_conn as query:
        query.search(
            search_base="DC=mavensecurities,DC=com",
            search_filter=f'(&(objectClass=user)(sAMAccountName={username}))',
            attributes=[ 'memberof', 'sAMAccountName' ]
        )
        for entry in query.entries:
            return entry
        print (f"Username: {username} not found!")

class Permission:
    def __init__(self, wheel, surface, name):
        self.wheel = wheel
        self.surface = surface
        self.name = name

    @property
    def instance(self):
        return self.wheel.instance

    @property
    def user(self):
        return self.normalise(self.name)

    @property
    def desk(self):
        return self.surface.desk

    def __str__(self):
        return self.name

    @staticmethod
    def normalise(username):
        return re.sub(r'^MAVEN\\', "", username, flags=re.IGNORECASE).lower()

    @classmethod
    def truename(cls, username):
        return f'MAVEN\\{ldap_lookup_user(cls.normalise(username)).sAMAccountName}'


class Surface:
    def __init__(self, wheel, desk, name):
        self.wheel = wheel
        self._desk = desk
        self.name = name
        self._config = None
        self._permissions = None

    @property
    def surface(self):
        return self.name

    @property
    def instance(self):
        return self.wheel.instance

    @property
    def desk(self):
        return self._desk.replace(' ', '-')

    @property
    def permissions(self):
        if not self._config:
            self._config = request_get(f"{self.wheel.url}/vols/{self.name}/config")
            self._permissions = [ Permission(self.wheel, self, p) for p in self._config['AuthorizedGroups'] ]
        return self._permissions

    def add_permission(self, username):
        perms = request_get(f"{self.wheel.url}/vols/{self.name}/config")['AuthorizedGroups']
        perms.append(username)
        logger.info(f"{self.wheel.url} ADDING {username} to {self.name}")
        request('POST', f"{self.wheel.url}/Commands/ChangePermissions/{self.name}", {"AuthorizedGroups": perms})

    def remove_permission(self, username):
        perms = request_get(f"{self.wheel.url}/vols/{self.name}/config")['AuthorizedGroups']
        assert username in perms, f"username {username} not in {self.name}"
        perms.remove(username)
        logger.info(f"{self.wheel.url} REMOVING {username} from {self.name}")
        request('POST', f"{self.wheel.url}/Commands/ChangePermissions/{self.name}", {"AuthorizedGroups": perms})

    def __str__(self):
        return self.name

class Wheel:

    def __init__(self, instance):
        self.instance = instance
        self.url = f"http://{instance}.mavensecurities.com"
        self._config = None
        self._surface_lk = {}

    @property
    def surfaces(self):
        if not self._config:
            self._config = request_get(f"{self.url}/")

            for dc in self._config['Desks']:
                desk = dc['Name']
                for s in dc['Surfaces']:
                    self._surface_lk[s] = Surface(self, desk, s)

        return self._surface_lk.values()

    @property
    def desks(self):
        return [ s.desk for s in self.surfaces ]

    @property
    def users(self):
        return [ p.user for p in self.permissions ]

    @property
    def permissions(self):
        sp = []
        for s in self.surfaces:
            for p in s.permissions:
                sp.append(p)
        return sp

    def __str__(self):
        return self.instance


class WheelCollection:

    def __init__(self, args):
        self.instances = { w: Wheel(w) for w in args.instances or DEFAULT_WHEEL_INSTANCES }
        self.args = args
        self.desk_filter = args.desks
        self.surface_filter = args.surfaces
        self.user_filter = args.users

    def filter(self, obj):
        show = True

        if self.desk_filter and hasattr(obj, 'desk'):
            if not any(fnmatch.fnmatch(str(obj.desk).lower(), d.lower()) for d in self.desk_filter):
                show = False

        if self.surface_filter and hasattr(obj, 'surface'):
            if not any(fnmatch.fnmatch(str(obj.surface), s) for s in self.surface_filter):
                show = False
        
        if self.surface_filter and hasattr(obj, 'surfaces'):
            for surface in obj.surfaces:
                if not any(fnmatch.fnmatch(str(surface), s) for s in self.surface_filter):
                    show = False

        if self.user_filter and hasattr(obj, 'users'):
            for user in obj.users:
                if not any(fnmatch.fnmatch(user.user, Permission.normalise(u)) for u in self.user_filter):
                    show = False

        if self.user_filter and hasattr(obj, 'user'):
            if not any(fnmatch.fnmatch(obj.user, Permission.normalise(u)) for u in self.user_filter):
                show = False

        return show

    @property
    def surfaces(self):
        for w in self.instances.values():
            yield from w.surfaces

    @property
    def permissions(self):
        for w in self.instances.values():
            yield from w.permissions

    def list_wheels(self):
        print ("[Wheel Instances]")
        wheel_list = [ w for w in self.instances.values() if self.filter(w) ]
        assert wheel_list, "No wheels found"
        for w in self.instances.values():
            print (f"{str(w):<20} {w.url}")

    def list_surfaces(self):
        print ("[Wheel Surfaces]")
        surface_list = [ s for s in self.surfaces if self.filter(s) ]
        assert surface_list, "No surfaces found"
        for s in sorted(surface_list, key=lambda v: v.desk):
            print (f"{s.instance:<20} {s.desk:<15} {s.name}")

    def list_permissions(self):
        print ("[Wheel Surface Permissions]")
        permission_list = [ p for p in self.permissions if self.filter(p) ]
        assert permission_list, "No surfaces found"
        for p in sorted(permission_list, key=lambda v: (v.desk, str(v.surface))):
            if self.filter(p):
                print (f"{p.instance:<20} {p.desk:<15} {str(p.surface):<12} {p.name}")


    def add_permissions(self):
        print ("[Grant User Permissions]")
        assert self.args.users, "Users Needed"
        assert self.args.surfaces or self.args.desks, "Surface or Desk Needed"

        surface_list = [ s for s in self.surfaces if self.filter(s) ]
        assert surface_list, "No surfaces found"

        user_list = [ Permission.truename(u) for u in self.args.users ]
        assert user_list, "No valid users provided"

        granted, needed = set(), []

        for username in user_list:
            for s in surface_list:
                existing = [ p for p in s.permissions if self.filter(p) ]
                if existing:
                    granted.update(existing)
                else:
                    needed.append((s, username))

        [ print (f"{p.instance}:{str(p.surface)} {p.name} HAS PERMISSIONS") for p in granted ]
        print ()

        [ print (f"{s.instance}:{str(s.surface)} {username} ADD PERMISSIONS") for s, username in needed ]
        print ()

        if not needed:
            print ("No Actions to take")
        elif click.confirm('Do you want to continue?', default=True):
            for s, username in needed:
                s.add_permission(username)

    def rem_permissions(self):
        print ("[Remove User Permissions]")
        assert self.args.users, "Users Needed"
        remove = []
        for p in sorted(self.permissions, key=lambda v: (v.desk, str(v.surface))):
            if self.filter(p):
                remove.append(p)

        [ print (f"REMOVE PERMISSIONS: {p.instance}:{str(p.surface)} {p.name}") for p in remove ]
        print ("")

        if not remove:
            print ("No Actions to take")
        elif click.confirm('Do you want to continue?', default=True):
            for p in remove:
                p.surface.remove_permission(p.name)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument("--wheel", "-w", action='append', dest="instances", help="wheel filter", default=None)
    parser.add_argument("--desk", "-d", action='append', dest="desks", help="desk filter", default=None)
    parser.add_argument("--surface", "-s", action='append', dest="surfaces", help="surface filter", default=None)
    parser.add_argument("--user", "-u", action='append', dest="users", help="user filter", default=None)

    actions = [ 'list-wheels', 'list-surfaces', 'list-permissions', 'add-permissions', 'rem-permissions' ]
    parser.add_argument('action', choices=actions)

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, datefmt="%Y-%m-%d %H:%M:%S", format='[%(levelname)s]: %(message)s')
    logging.debug(args)

    try:
        wc = WheelCollection(args)

        if args.action == 'list-wheels':
            wc.list_wheels()
        elif args.action == 'list-surfaces':
            wc.list_surfaces()
        elif args.action == 'list-permissions':
            wc.list_permissions()
        elif args.action == 'add-permissions':
            wc.add_permissions()
        elif args.action == 'rem-permissions':
            wc.rem_permissions()

    except AssertionError as e:
        logger.error(e)
        sys.exit(1)
