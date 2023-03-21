import os
from db import label_router
from fastapi import FastAPI
from decouple import config
from db.session import create_db, drop_db
from model_loader import ModelLoader
from web_controller import router as web_router
from fastapi.middleware.cors import CORSMiddleware
from users_controllers import router as users_router


def initialize_env_vars():
    """
    Initialize environment variables
    :return:
    """
    env_variables = [
        "DATABASE_URL",
    ]
    for env_var in env_variables:
        if not os.getenv(env_var):
            os.environ[env_var] = config(env_var)


initialize_env_vars()
app = FastAPI()


@app.on_event("startup")
def load_model():
    app.state.model = ModelLoader(
        path="models/sklearn/web_classifier_model.sav", name="web_classifier", backend="sklearn"
    )


def startup_event():
    """
    Drop the database
    :return:
    """
    create_db()


@app.on_event("shutdown")
def shutdown_event():
    """
    Drop the database
    :return:
    """
    drop_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(
    web_router,
    prefix="/website",
    tags=["website"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    label_router.router,
    prefix="/labels",
    tags=["labels"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@app.get("/hi")
def root():
    return {"message": "Hello World from FastAPI and Docker Deployment course"}
