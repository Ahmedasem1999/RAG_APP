from fastapi import FastAPI
app = FastAPI()

@app.get("/Welcome")
def welcome_message():
    return "Welcome to the FastAPI application!"

