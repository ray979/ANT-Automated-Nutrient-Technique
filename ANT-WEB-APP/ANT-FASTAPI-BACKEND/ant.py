#import statements
from fastapi import FastAPI
from routes.sensordata import ant_router
from fastapi.middleware.cors import CORSMiddleware

client_apps = ['http://localhost:3000'] #Our REACT app will be running on this IP and PORT


#create app
app = FastAPI()
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
