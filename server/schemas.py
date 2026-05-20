from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=50)


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
