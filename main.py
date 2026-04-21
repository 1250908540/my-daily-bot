import requests
import os
import sys

# 从 GitHub Secrets 中读取
BARK_KEY = os.getenv("BARK_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")

def get_data():
    # 1. 天气 (默认使用 devapi 域名，适配免费版)
    weather_url = f"https://devapi.qweather.com/v7/weather/now?location=101010100&key={WEATHER_KEY}"
    w_res = requests.get(weather_url).json()
    if w_res.get('code') == '200':
        w = w_res['now']
        weather_info = f"天气：{w['text']}，{w['temp']}度"
    else:
        weather_info = f"天气获取失败(错误码:{w_res.get('code')})"

    # 2. 星座 (天行数据)
    star_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY}&astro=cancer"
    s_res = requests.get(star_url).json()
    star_info = s_res['result']['content'] if s_res.get('code') == 200 else "星座运势获取失败"

    # 3. 语录 (天行数据)
    quote_url = f"https://apis.tianapi.com/lzmy/index?key={TIAN_KEY}"
    q_res = requests.get(quote_url).json()
    quote_info = q_res['result']['saying'] if q_res.get('code') == 200 else "语录获取失败"

    return weather_info, star_info, quote_info

def push_bark(title, content):
    url = f"https://api.day.app/{BARK_KEY}/{title}/{content}?group=DailyBot"
    requests.get(url)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'morning'
    w, s, q = get_data()
    
    if mode == 'morning':
        push_bark("早安！今日简报", f"{w}\n\n运势：{s}")
    else:
        push_bark("每日励志", q)
