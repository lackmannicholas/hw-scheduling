from fastapi import FastAPI
from routers.router1 import router as router1
from routers.router2 import router as router2
import uvicorn

app = FastAPI(title="HW Scheduling API", description="Scheduling API for HW that provides scheduling and availability features.", version="1.0.0")

# List of routers to attach
routers = [router1, router2]

# Attach each router to the application
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
