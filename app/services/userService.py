from app.repository.user import UserRepository
from app.schemas.users import User, UserDocument


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    async def create_user(self, user: User) -> str:
        try:
            # check exist user
            userDB = await self.repo.get_user(user.telegram_id)
            if (userDB):
                # if exist return id user from DB
                return str(userDB.id)
            # else create new user
            userDB = UserDocument(telegram_id=user.telegram_id,
                                  username=user.username)
            resultDB = await self.repo.create_user(userDB)
            
        except Exception as e:
            raise Exception(f"user create service: {e}")
        

        return str(resultDB.id)
       

    async def get_user(self, telegram_id:int) -> User:
        try:
            user = await self.repo.get_user(telegram_id)
        except Exception as e:
            raise Exception(f"user get service: {e}")
        
        return User(id=user.id,
                    telegram_id=user.telegram_id,
                    username=user.username,
                    created_at=user.created_at)
    