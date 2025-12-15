import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.services.user_service.app.core.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL_ASYNC = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None

    def connect(self):
        logger.info("Подключение к БД...")

        self.engine = create_async_engine(
            DATABASE_URL_ASYNC,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        logger.info("БД подключена")

    async def disconnect(self):
        logger.info("Отключение БД...")
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.SessionLocal = None
            logger.info("БД отключена")

    async def check_connection(self) -> bool:
        if not self.engine:
            return False
        try:
            async with self.engine.connect() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Ошибка соединения с БД: {e}")
            return False

    async def get_db(self):
        if not self.SessionLocal:
            raise RuntimeError("БД не инициализирована")
        async with self.SessionLocal() as db:
            yield db


db_manager = DatabaseManager()
