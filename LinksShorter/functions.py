import random
import string

def generate_short_link(length=6):
  characters = string.ascii_letters + string.digits
  short_link = ''.join(random.choice(characters) for _ in range(length))
  return short_link
