from .database import db_manager  # noqa

async def get_db():
    async for db in db_manager.get_db():
        yield db
