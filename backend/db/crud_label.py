from .label_model import Label as models
from .label_schema import Label, LabelCreate, LabelUpdate
from .singleton import Singleton
from .crud_base import CrudBase

"""
This class is a CRUD class for the predictions table.
"""


class LabelCRUD(
    CrudBase[Label, LabelCreate, LabelUpdate],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models)


# Create a singleton instance of the LabelCRUD class
label = LabelCRUD()
