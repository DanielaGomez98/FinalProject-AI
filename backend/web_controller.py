import requests
from db.db import get_db
from fastapi import Depends
from pydantic import BaseModel
from db.label_schema import Label
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from model_loader import ModelLoader
from starlette.requests import Request
from db.crud_label import label as crud_label
from fastapi_utils.inferring_router import InferringRouter

from bs4 import BeautifulSoup
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

# the functions that my API will have are defined in the routers.
router = InferringRouter()


class WebModelEntry(BaseModel):
    url: str

    def to_list(self):
        return [
            self.url,
        ]


async def get_model(req: Request):
    return req.app.state.model


# all the routes included in the web router are defined to do different HTTP methods
# the API interacts with the database, in this case the Label table.
@cbv(router)
class WebController:
    # load the model
    model: ModelLoader = Depends(get_model)
    # dependency injection to access the connection to the database.
    db: Session = Depends(get_db)

    @router.get("/")
    # diagnostic function
    def welcome(self):
        return {"message": "Welcome to the Web Classifier API"}

    @router.get("/info")
    def model_info(self):
        """Return model information, version, how to call"""
        return {"name": self.model.name, "version": self.model.version}

    @router.get("/health")
    def service_health(self):
        """Return service health"""
        return "ok"

    @router.post("/predict")
    async def predict(self, request: Request):
        # json with the URL to be classified
        request_body = await request.json()
        # get only the URL
        website_url = request_body[0]["url"]
        # make the prediction
        predictions = self.model([website_url])
        # get only the URL category
        website_category = predictions[0]
        lbl = Label(url=website_url, label=website_category)
        # create a new record in the database
        crud_label.create(self.db, entity=lbl)
        # return json with prediction
        return {"label": predictions.tolist()}

    @router.get("/labels")
    def get_labels(self):
        """
        Get all labels from the database
        :return:
        """
        return crud_label.fetch_all(self.db)

    @router.post("/content")
    async def website_content(self, request: Request):
        # json with the URL to be classified
        request_body = await request.json()
        for x in request_body:
            print(x)
        # get only the URL
        inputs = x["url"]
        response = requests.get(inputs)
        soup = BeautifulSoup(response.text, 'html.parser')
        # get the website title
        title = soup.title.string
        paragraphs = [p.text for p in soup.find_all('p')]
        text = '\n'.join(paragraphs)
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        # get the website summary
        summary = summarizer(parser.document, sentences_count=8)
        sentences = []
        for sentence in summary:
            sentences.append(str(sentence))
        summary_text = ' '.join(sentences)
        return title, summary_text
