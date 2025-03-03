from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from openfeature import api
from openfeature.contrib.provider.flagd import FlagdProvider

app = FastAPI()

api.set_provider(FlagdProvider())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = api.get_client()
FLAG_STR="welcome-message"

@app.get("/api/buy-now")
def root():
    show_welcome_message = client.get_boolean_value(FLAG_STR, True)

    if show_welcome_message:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Payment successful"},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Not authorized"},
        )
