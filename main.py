from routers import users, whatsapp, telegram, document, chat_bot, address
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from middleware.auth_middleware import AuthMiddleware
from fastapi.staticfiles import StaticFiles
from services.ingest import main_loop

scheduler = BackgroundScheduler()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)
app.include_router(whatsapp.router)
app.include_router(telegram.router)
app.include_router(users.router)
app.include_router(document.router)
app.include_router(chat_bot.router)
app.include_router(address.router)
app.mount("/files", StaticFiles(directory="documents"), name="files")

@app.on_event("startup")
def start_scheduler():
    print("scheduler start")
    scheduler.add_job(main_loop, 'interval', id='main_loop1', seconds=10)
    scheduler.start()


@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
    print('scheduler stop')


@app.get("/")
async def root():
    return {"message": "FastAPI Running"}
