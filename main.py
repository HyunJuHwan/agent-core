from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from executor.executor import initialize_mcp_session
from router.route import router
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시
    await initialize_mcp_session()
    yield
    # 앱 종료 시 (필요 시)
    # await shutdown_tasks()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (운영환경에선 특정 도메인만 허용 권장)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Agent Core is running"}
