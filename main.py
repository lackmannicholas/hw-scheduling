import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_level="info", reload=True)
