from pydantic import BaseModel


class CreateShortURLRequestSchema(BaseModel):
    long_url: str


class CreateShortURLResponseSchema(BaseModel):
    short_url: str


class GetLongURLResponseSchema(BaseModel):
    long_url: str
