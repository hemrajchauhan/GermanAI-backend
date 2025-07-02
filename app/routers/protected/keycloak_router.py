from fastapi import APIRouter, Depends
from app.auth.keycloak import verify_jwt_token
# from app.services.keycloak_service import keycloak

router = APIRouter()

@router.get("/protected/")
def protected_route(user: dict = Depends(verify_jwt_token)):
    return {"hello": user["preferred_username"]}

# @router.get("/secure-endpoint")
# def secure_endpoint(user=Depends(keycloak.get_current_user)):
#     return {"user": user}

