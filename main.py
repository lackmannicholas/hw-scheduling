from fastapi import FastAPI
from routers.scheduling import router
import uvicorn


app = FastAPI(title="HW Scheduling API", description="Scheduling API for HW that provides scheduling and availability features.", version="1.0.0")
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
