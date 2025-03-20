import json
import urllib.request
from wsgiref.simple_server import make_server


def fetch_exchange_rate(currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read())
                return data
            else:
                return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def application(environ, start_response):
    # Получаем запрашиваемый URL
    path = environ.get('PATH_INFO', '/')

    # Извлекаем валюту из URL, например: /USD
    currency = path.strip('/').upper()

    # Получаем данные по валюте
    exchange_data = fetch_exchange_rate(currency)

    if exchange_data:
        response_body = json.dumps(exchange_data).encode('utf-8')
        status = '200 OK'
    else:
        response_body = json.dumps({'error': 'Currency not found or API error'}).encode('utf-8')
        status = '404 Not Found'

    headers = [('Content-Type', 'application/json')]
    start_response(status, headers)

    return [response_body]


if __name__ == '__main__':
    # Запускаем WSGI сервер
    httpd = make_server('', 8000, application)
    print("App_currency is running on port 8000...")
    httpd.serve_forever()
