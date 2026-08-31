from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str
    password: str
    email: str


class ReadUser(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class ReadProduct(BaseModel):
    id: int
    name: str
    price: float
    discount: float
    short_description: str
    full_description: str
    image_url: str

    class Config:
        from_attributes = True


class ReadTag(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
