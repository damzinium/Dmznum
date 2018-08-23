import string
from random import *

def SECRET_KEY(min, max):
	allchars = string.ascii_letters + string.punctuation + string.hexdigits
	password = "".join(choice(allchars) for x in range(randint(min, max)))
	return password
