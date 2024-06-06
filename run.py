import uvicorn
from pyngrok import ngrok
import threading
import time
import nest_asyncio

from main import app

# Разрешение повторного запуска uvicorn
nest_asyncio.apply()

def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Запуск FastAPI в отдельном потоке
thread = threading.Thread(target=run_app)
thread.start()

# Дать время серверу для запуска
time.sleep(5)

# Запуск ngrok и получение URL
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Для тестирования через HTTP запросы
import requests

url = f'{public_url}/summarize/'
data = {'url': 'https://www.bbc.co.uk/'}
response = requests.post(url, json=data)

# Проверка кода ответа и вывод результата
if response.status_code == 200:
    print("Summary:", response.json())
else:
    print("Error:", response.status_code, response.text)