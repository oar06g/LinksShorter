import random
import string
import re


def validate_url(url):
    regex = re.compile(
        r'^(https?|ftp):\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(\/.*)?$', re.IGNORECASE
    )
    return re.match(regex, url)

v = validate_url("https://www.youtube.com/watch?v=SO7aRgetsS0&list=PL0YstkxpZANFkkPdYaOpRrQolAcrzJp9M&index=25")
print(v)