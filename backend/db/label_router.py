from .crud_label import label
from .db import get_db
from fastapi import Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter()


@cbv(router)
class LabelRouter:
    # dependency injection
    db: Session = Depends(get_db)

    @router.get("/home")
    def home(self):
        """
        status endpoint
        :return:
        """
        return "LabelRouter ready"

    @router.get("/")
    def get_labels(self):
        """
        Get all labels
        :return:
        """
        return label.fetch_all(self.db)
