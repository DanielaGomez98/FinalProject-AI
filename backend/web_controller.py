import requests
from fastapi import Depends
from bs4 import BeautifulSoup
from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from model_loader import ModelLoader
from starlette.requests import Request
from fastapi_utils.inferring_router import InferringRouter
from db.crud_label import label as crud_label
from db.label_schema import Label
from db.db import get_db
from sqlalchemy.orm import Session
import nltk
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

nltk.download('punkt')

router = InferringRouter()


class WebModelEntry(BaseModel):
    url: str

    def to_list(self):
        return [
            self.url,
        ]


async def get_model(req: Request):
    return req.app.state.model


@cbv(router)
class WebController:
    # injection dependecy pattern
    model: ModelLoader = Depends(get_model)
    db: Session = Depends(get_db)

    @router.get("/")
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
        request_body = await request.json()
        for x in request_body:
            print(x)
        inputs = [
            x["url"]
        ]
        predictions = self.model(inputs)
        print(predictions)
        lbl = Label(
            url = x["url"],
            label = "12"
        )
        crud_label.create(self.db, entity=lbl)
        return {"label": predictions.tolist()}

    # @router.get("/predict")
    # def get_labels(self):
    #     """
    #     Get all labels
    #     :return:
    #     """
    #     return label.fetch_all(self.db)

    @router.post("/content")
    async def website_content(self, request: Request):
        request_body = await request.json()
        for x in request_body:
            print(x)
        inputs = x["url"]
        response = requests.get(inputs)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        paragraphs = [p.text for p in soup.find_all('p')]
        text = '\n'.join(paragraphs)
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentences_count=8)
        sentences = []
        for sentence in summary:
            sentences.append(str(sentence))
        summary_text = ' '.join(sentences)
        return title, summary_text
