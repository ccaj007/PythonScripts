"""
https://www.codewars.com/kata/52223df9e8f98c7aa7000062

How can you tell an extrovert from an introvert at NSA?
Va gur ryringbef, gur rkgebireg ybbxf ng gur BGURE thl'f fubrf.

I found this joke on USENET, but the punchline is scrambled. Maybe you can decipher it?
According to Wikipedia, ROT13 is frequently used to obfuscate jokes on USENET.

For this task you're only supposed to substitute characters. Not spaces, punctuation, numbers, etc.

"""

def rot13(message):
    in_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    out_string = "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"

    translate_dict = {in_string[i]: out_string[i] for i in range(len(in_string))}

    table = str.maketrans(translate_dict)
    return message.translate(table)

print(rot13("EBG13 rknzcyr."))

