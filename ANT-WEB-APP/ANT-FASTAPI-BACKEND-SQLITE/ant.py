#import statements
from fastapi import FastAPI
from routes.routes import ant_router, client
import models.models as models
from config.database import engine
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

client_apps = ['http://localhost:3000'] #Our REACT app will be running on this IP and PORT


#create app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#register your router
app.include_router(ant_router)

#Register App with CORS middleware to allow resources sharing between different domains/origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=client_apps,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    client.loop_stop()

