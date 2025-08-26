from pydantic import BaseModel


class Page(BaseModel):
    status: int
    text: str
