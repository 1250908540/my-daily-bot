import requests
import os
import sys

# 从 GitHub Secrets 中读取敏感信息
BARK_KEY = os.getenv("BARK_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")

def push_bark(title, content):
    url = f"https://api.day.app/{BARK_KEY}/{title}/{content}?group=DailyBot"
    requests.get(url)

def get_data():
    # 1. 获取天气 (和风)
    weather_url = f"https://devapi.qweather.com/v7/weather/now?location=101010100&key={WEATHER_KEY}"
    w_data = requests.get(weather_url).json()['now']
    weather_text = f"天气：{w_data['text']}，温度：{w_data['temp']}度"

    # 2. 获取星座运势 (天行)
    star_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY}&astro=lion" # 以狮子座为例
    s_data = requests.get(star_url).json()['result']['content']

    # 3. 获取励志语录 (天行)
    quote_url = f"https://apis.tianapi.com/lzmy/index?key={TIAN_KEY}"
    q_data = requests.get(quote_url).json()['result']['saying']

    return weather_text, s_data, q_data

if __name__ == "__main__":
    # 接收运行参数：'morning' 表示早报，'random' 表示语录
    mode = sys.argv[1] if len(sys.argv) > 1 else 'morning'
    
    w, s, q = get_data()
    
    if mode == 'morning':
        content = f"{w}\n今日运势：{s}"
        push_bark("早安！今日份简报", content)
    else:
        push_bark("随机励志语录", q)
