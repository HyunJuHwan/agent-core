from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일을 시스템 환경 변수로 로드

class Settings:
    LLM_URL: str = os.getenv("LLM_URL", "http://localhost:11434/api/generate")
    MCP_URL: str = os.getenv("MCP_URL", "http://localhost:1337/mcp")
    IMAGE_BASE_URL = os.getenv("IMAGE_BASE_URL", "http://localhost:8001/image")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

settings = Settings()
