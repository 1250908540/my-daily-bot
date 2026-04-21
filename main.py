import requests
import os
import sys

# 从 GitHub Secrets 中读取
BARK_KEY = os.getenv("BARK_KEY")
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")

def get_data():
    # 1. 天气 (和风)
    weather_info = "天气获取失败"
    try:
        w_url = f"https://devapi.qweather.com/v7/weather/now?location=101010100&key={WEATHER_KEY}"
        w_res = requests.get(w_url).json()
        if w_res.get('code') == '200':
            w = w_res['now']
            weather_info = f"天气：{w['text']}，{w['temp']}°C"
        else:
            weather_info = f"天气报错: {w_res.get('code')}"
    except Exception as e:
        weather_info = f"天气程序异常: {str(e)[:20]}"

    # 2. 星座 (天行)
    star_info = "运势获取失败"
    try:
        s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY}&astro=lion"
        s_res = requests.get(s_url).json()
        # 更加安全的读取方式
        if s_res.get('code') == 200 and 'result' in s_res:
            star_info = s_res['result'].get('content', '暂无内容')
        else:
            star_info = f"运势报错: {s_res.get('msg', 'Key可能未激活')}"
    except Exception as e:
        star_info = f"运势程序异常: {str(e)[:20]}"

    # 3. 语录 (天行)
    quote_info = "语录获取失败"
    try:
        q_url = f"https://apis.tianapi.com/lzmy/index?key={TIAN_KEY}"
        q_res = requests.get(q_url).json()
        if q_res.get('code') == 200 and 'result' in q_res:
            quote_info = q_res['result'].get('saying', '暂无语录')
        else:
            quote_info = "语录Key未激活或已达上限"
    except:
        pass

    return weather_info, star_info, quote_info

def push_bark(title, content):
    # 对内容进行简单的 URL 编码处理，防止特殊字符导致推送失败
    url = f"https://api.day.app/{BARK_KEY}/{title}/{content}?group=DailyBot"
    requests.get(url)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'morning'
    w, s, q = get_data()
    
    if mode == 'morning':
        msg = f"{w}\n\n运势：{s}"
        push_bark("早安简报", msg)
    else:
        push_bark("每日励志", q)
