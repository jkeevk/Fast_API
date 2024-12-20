from pydantic import BaseModel
import datetime
from typing import Literal


class IdResponseBase(BaseModel):
    id: int


class StatusResponse(BaseModel):
    status: Literal["deleted"]


class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    created_at: datetime.datetime
    author_id: int
    author_email: str


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int
    author_id: int


class CreateAdvertisementResponse(IdResponseBase):
    pass


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None 
    description: str | None = None 
    price: int | None = None 


class UpdateAdvertisementResponse(IdResponseBase):
    pass


class DeleteAdvertisementResponse(StatusResponse):
    pass



class CreateUserRequest(BaseModel):
    email: str
    password: str


class CreateUserResponse(IdResponseBase):
    pass