from sqlalchemy import DDL
from sqlalchemy import event
from .orm_base import OrmBaseModel
from sqlalchemy import Column, Integer, String


"""
ORM class to interact with the image_records table in the database
"""


class Label(OrmBaseModel):
    url_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String(3000), nullable=False, unique=True)
    label = Column(String(15), nullable=False)


restart_seq = DDL("ALTER SEQUENCE %(table)s_url_id_seq RESTART WITH 1;")

event.listen(
    Label.__table__, "after_create", restart_seq.execute_if(dialect="postgresql")
)
