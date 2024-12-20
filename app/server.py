from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from lifespan import lifespan
from models import Session, Advert, User
from dependency import SessionDependency
import crud
from constants import STATUS_DELETED
from schema import (GetAdvertisementResponse,
CreateAdvertisementResponse,
CreateAdvertisementRequest,
UpdateAdvertisementRequest, 
UpdateAdvertisementResponse,
DeleteAdvertisementResponse,
CreateUserResponse,
CreateUserRequest)




app = FastAPI(
    title="Advertisement API",
    version="0.1.0",
    description="API for advertisement",
    lifespan=lifespan)




@app.post("/api/v1/advertisement", response_model=CreateAdvertisementResponse, tags=["advertisements"])
async def create_advertisement(advert_request: CreateAdvertisementRequest, session: SessionDependency):
    advertisement_obj = Advert(
        title=advert_request.title, 
        description=advert_request.description, 
        price=advert_request.price, 
        author_id=advert_request.author_id
    )
    await crud.add_advert(session, advertisement_obj)
    return advertisement_obj.id_dict
    


@app.patch("/api/v1/advertisement{advertisement_id}", response_model=UpdateAdvertisementResponse, tags=["advertisements"])
async def update_advertisement(
    advertisement_id: int, advertisement_request: UpdateAdvertisementRequest, session: SessionDependency):

    advertisement_json = advertisement_request.dict(exclude_unset=True)
    advertisement = await crud.get_advert_by_id(session, Advert, advertisement_id)
    for field, value in advertisement_json.items():
        setattr(advertisement, field, value)

    await crud.add_advert(session, advertisement)
    return advertisement.id_dict

    
@app.delete("/api/v1/advertisement/{advertisement_id}", response_model=DeleteAdvertisementResponse, tags=["advertisements"])
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement = await crud.get_advert_by_id(session, Advert, advertisement_id)
    await crud.delete_advert(advertisement, session)
    return STATUS_DELETED

@app.get("/api/v1/advertisement/{advertisement_id}", 
         response_model=GetAdvertisementResponse, tags=["advertisements"])
async def get_advertisement(session: SessionDependency, advertisement_id: int):
    advertisement_obj = await crud.get_advert_by_id(session, Advert, advertisement_id)
    return advertisement_obj.dict


# @app.get("/api/v1/advertisement?{query_string}", tags=["advertisements"])
# async def get_advertisement_by_qs(query_string: str):
#     return {"message": "Some advertisement"}

@app.post("/api/v1/user", response_model=CreateUserResponse, tags=["users"])
async def create_user(user_request: CreateUserRequest, session: SessionDependency):
    user_obj = User(
        email=user_request.email, 
        password=user_request.password
    )
    await crud.add_user(session, user_obj)
    return user_obj.id_dict

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)