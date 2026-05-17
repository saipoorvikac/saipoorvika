from fastapi import Depends, HTTPException
from jose import jwt

SECRET = "secretkey"

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_checker