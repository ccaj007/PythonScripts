import requests
from bs4 import BeautifulSoup
import datetime

url = "https://pixelford.com/blog/"
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'html.parser')
a_tags = soup.find_all('a', class_="entry-title-link")
blogs = soup.find_all('article', class_='type-post')
s
for blog in blogs:
    title = blog.find('a', class_="entry-title-link").get_text()
    datetime_string = blog.find('time', class_="entry-time").get('datetime')
    blog_datetime = datetime.datetime.fromisoformat(datetime_string)
    pretty_date = blog_datetime.strftime("%b %d %Y")
    print(f"{pretty_date} - {title}")

