import random
import string
import re

# from LinksShorter.config import SessionLocal
# from LinksShorter.models import Links
# from LinksShorter.app import db

# def validate_url(url):
#     regex = re.compile(
#         r'^(https?|ftp):\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(\/.*)?$', re.IGNORECASE
#     )
#     return re.match(regex, url)

# v = validate_url("https://www.youtube.com/watch?v=SO7aRgetsS0&list=PL0YstkxpZANFkkPdYaOpRrQolAcrzJp9M&index=25")
# print(v)

# def validate_slug(slug):
#     return re.match(r'^[a-zA-Z0-9_-]{3,20}$', slug)

# async def is_slug_unique(slug):
#     async with SessionLocal() as session:
#         result = await session.execute(
#             db.select(Links).filter_by(short_url=slug)
#         )
#         return result.scalar() is None


def generate_short_link(length=6):
    characters = string.ascii_letters + string.digits
    short_link = ''.join(random.choice(characters) for _ in range(length))
    return short_link

# short_link = generate_short_link(6)
# print(f"Generated Short Link: {short_link}")
