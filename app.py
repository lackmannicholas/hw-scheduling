from fastapi import FastAPI
from routers.scheduling import router


app = FastAPI(title="HW Scheduling API", description="Scheduling API for HW that provides scheduling and availability features.", version="1.0.0")
app.include_router(router)
