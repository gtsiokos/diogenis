import hashlib

def get_hashed_username(username):
	uname_hashed = hashlib.sha256(username)
	return uname_hashed.hexdigest()
