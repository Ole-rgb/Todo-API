# the function of this file it to check whether the request is autorized or not [Verification fo the protected route]

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import auth.jwt_handler as JWTHandler

#subclass from HTTPBearer to persist auth on the routes
class JWTBearer(HTTPBearer):
    #enable todo_error so that errors get reported automatically
    def __init__(self, auto_error : bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)
        
    #everytime the JWTBearer is invoked, new credentials get created, if the credentials are "bad" 
    #raise a exception
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    #verifies whether a tokes is valid (passes a string to the decodeJWT-method and returns the outcome)
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False # a false flag
        payload = JWTHandler.decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid