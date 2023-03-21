from pydantic import BaseModel


class LabelSchema(BaseModel):
    url: str
    label: str


class LabelCreate(LabelSchema):
    pass


class LabelUpdate(LabelSchema):
    pass


class Label(LabelSchema):
    url_id: int = None

    class Config:
        orm_mode = True
