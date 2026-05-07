import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str           = os.getenv("BASE_URL", "https://www.saucedemo.com")
    STANDARD_USER: str      = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER: str        = os.getenv("LOCKED_USER", "locked_out_user")
    PASSWORD: str           = os.getenv("PASSWORD", "secret_sauce")
    HEADLESS: bool          = os.getenv("HEADLESS", "true").lower() == "true"
    IMPLICIT_WAIT: int      = int(os.getenv("IMPLICIT_WAIT", 10))
    PAGE_LOAD_TIMEOUT: int  = int(os.getenv("PAGE_LOAD_TIMEOUT", 30))


settings = Settings()
