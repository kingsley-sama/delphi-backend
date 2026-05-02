from typing import Annotated
from models import User
from fastapi import Depends, HTTPException, status
from auth import get_current_user

def require_role(required_role: str):
    def role_checker(user:Annotated[User, Depends(get_current_user)]):
        if user.role != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbiden")
        return user
    return role_checker