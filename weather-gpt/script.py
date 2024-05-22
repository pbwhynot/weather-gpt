import requests
import random
import time
from datetime import datetime
import pytz

#API_KEY = Your key here
#GPT_API_KEY = your key here

BASE_URL = 'http://api.weatherbit.io/v2.0/current'
GPT_URL = 'https://api.openai.com/v1/chat/completions'

CALLS_MADE = 0
MAX_CALLS_PER_DAY = 50

cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Berlin", "Moscow", "Toronto", "Beijing", "Mumbai"]

def get_weather_and_ask_chatgpt():
    global CALLS_MADE
    if CALLS_MADE >= MAX_CALLS_PER_DAY:
        return  
    city_name = random.choice(cities)
    complete_url = f"{BASE_URL}?key={API_KEY}&city={city_name}"
    response = requests.get(complete_url).json()

    clouds = response['data'][0]['clouds']
    if clouds <= 50:
        atlantic_zone = pytz.timezone('America/Moncton')
        current_datetime = datetime.now(atlantic_zone).strftime("%Y-%m-%d %H:%M:%S")  
        ask_chatgpt(f"Please tell me a funny joke. The current date and time is {current_datetime}.")

    CALLS_MADE += 1

def ask_chatgpt(question):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    }
    
    response = requests.post(GPT_URL, headers=headers, json=data)
    if response.status_code == 200:
        chatgpt_response = response.json()['choices'][0]['message']['content']
    else:
        chatgpt_response = f"Error: Unable to get response from ChatGPT - {response.text}"
    
    log_message(question + "\n--- Response ---\n" + chatgpt_response + "\n\n")

def log_message(message):
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

def run_scheduled_calls():
    get_weather_and_ask_chatgpt()

    while CALLS_MADE < MAX_CALLS_PER_DAY:
        time_to_wait = random.randint(60, 1728)
        time.sleep(time_to_wait)
        get_weather_and_ask_chatgpt()

run_scheduled_calls()








