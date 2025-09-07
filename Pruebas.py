import bcrypt

# Admin
admin_pass = "Admin123".encode("utf-8")
admin_hash = bcrypt.hashpw(admin_pass, bcrypt.gensalt())
print(admin_hash.decode())

# Usuario
user_pass = "Usuario123".encode("utf-8")
user_hash = bcrypt.hashpw(user_pass, bcrypt.gensalt())
print(user_hash.decode())
