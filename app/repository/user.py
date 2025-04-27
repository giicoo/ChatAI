from app.schemas.users import UserDocument


class UserRepository:
    async def create_user(self, user: UserDocument) -> UserDocument:
        await user.insert() 
        return user

    async def get_user(self, telegram_id: int) -> UserDocument:
        user = await UserDocument.find_one(UserDocument.telegram_id==telegram_id)
        return user
