import os


class Settings:
    DB_USER: str = os.getenv("SERVICE1_DB_USER")
    DB_PASSWORD: str = os.getenv("SERVICE1_DB_PASSWORD")
    DB_NAME: str = os.getenv("SERVICE1_DB_NAME")
    DB_HOST: str = os.getenv("SERVICE1_DB_HOST")
    DB_PORT: str = os.getenv("SERVICE1_DB_PORT")

    JWT_SECRET: str = os.getenv("JWT_SECRET", "change_me")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

    @property
    def DATABASE_URL(self) -> str:
        if not all([
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_NAME,
            self.DB_HOST,
            self.DB_PORT
        ]):
            raise RuntimeError("Не заданы все переменные окружения для БД")

        return (
            f"postgresql://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()
