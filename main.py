from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Инициализация модели для генерации сводки
summarization_model = pipeline("summarization")

class UrlRequest(BaseModel):
    url: str

@app.post("/summarize/")
def summarize_news(url_request: UrlRequest):
    news_site = url_request.url
    # Получение текста новостей с выбранного сайта
    response = requests.get(news_site)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_text = ""
    articles = soup.find_all('article')
    for article in articles:
        news_text += article.get_text() + "\n"

    # Генерация сводки на основе извлеченных новостей
    summary = summarization_model(news_text, max_length=100, min_length=20, do_sample=False)

    # Возвращение сводки
    return {"summary": summary[0]['summary_text']}