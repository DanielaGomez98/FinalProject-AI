import requests
from fastapi import Depends
from bs4 import BeautifulSoup
from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from model_loader import ModelLoader
from starlette.requests import Request
from fastapi_utils.inferring_router import InferringRouter


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
        return {"label": predictions.tolist()}

    @router.post("/content")
    async def website_content(self, request: Request):
        request_body = await request.json()
        for x in request_body:
            print(x)
        inputs = x["url"]
        response = requests.get(inputs)
        soup = BeautifulSoup(response.text, 'html.parser')
        # paragraphs = [p.text for p in soup.find_all('p')]
        # text = '\n'.join(paragraphs)
        title = soup.title.string
        print(title)
        return title

        # poetry add sumy numpy spacy en_core_web_sm
        # import sumy
        # from sumy.parsers.plaintext import PlaintextParser
        # from sumy.nlp.tokenizers import Tokenizer
        # from sumy.summarizers.lex_rank import LexRankSummarizer
        # text = "text"
        # parser = PlaintextParser.from_string(text, Tokenizer("english"))
        # summarizer = LexRankSummarizer()
        # summary = summarizer(parser.document, num_sentences=3)
        # for sentence in summary:
        #   print(sentence)

        #     # Extract the text from all of the <p> tags
        #     paragraphs = [p.text for p in soup.find_all('p')]
        #     text = '\n'.join(paragraphs)
        #     # Summarize the text
        #     #summary = summarize(text, ratio=0.1)
        #     return summary
