import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
    TIMEOUT: int = int(os.getenv("TIMEOUT", 30))


settings = Settings()
