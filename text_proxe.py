import requests

proxy = "http://158.255.77.169:80"  # Пример прокси
try:
    response = requests.get('http://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=5)
    print(response.json())  # Если прокси работает, вы увидите IP-адрес
except Exception as e:
    print(f"Ошибка: {e}")