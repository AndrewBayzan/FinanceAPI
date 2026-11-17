from app.core.security import (
    create_access_token,
    decode_access_token
)

token = create_access_token(1)

# print("JWT:", token)

payload = decode_access_token(token)

print(token)
print