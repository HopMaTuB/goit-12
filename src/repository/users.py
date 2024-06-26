from src.schemas import UserModel
from src.repository.auth import Hash, create_access_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.configuration.models import User
from typing import Optional

hash_handler = Hash()


class UsernameToken(Exception):
    pass

class Wrongpassword(Exception):
    pass

class LoginFailed(Exception):
    pass 


class UserService:

    @staticmethod
    def get_user(username: str, db: Session) -> Optional[User]:
        return db.query(User).filter(User.email == username).first()


    @staticmethod
    def check_user_available(username: str, db: Session):
        exist_user = UserService.get_user(username,db)
        if exist_user:
            raise UsernameToken
        
    @staticmethod
    def create_new_user(body:UserModel, db: Session):
        UserService.check_user_available(username=body.email, db=Session)
        new_user = User(email=body.email,password=hash_handler.get_password_hash(body.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def check_password(entered_password: str, database_password: str):
        if not hash_handler.verify_password(entered_password, database_password):
            raise Wrongpassword
        
    @staticmethod
    def login_user(body: OAuth2PasswordRequestForm, db: Session):
        user = UserService.get_user(body.username ,db = db)
        if user is None or not hash_handler.verify_password(body.password, user.password):
            raise LoginFailed
        
        access_token = create_access_token(data={"sub": user.email})
        return access_token

        

    


