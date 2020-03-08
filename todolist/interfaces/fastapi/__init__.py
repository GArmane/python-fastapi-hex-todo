from fastapi import FastAPI  # type: ignore


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
