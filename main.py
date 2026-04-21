import requests
import os
from datetime import datetime, timedelta

# 从 GitHub Secrets 读取
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    # 获取当前北京时间 (UTC+8)
    bj_time = datetime.utcnow() + timedelta(hours=8)
    hour = bj_time.hour
    
    title = "早安简报"
    weather_info, star_info, english_info = "", "", ""

    # --- 1. 获取每日英语 (早中晚都发) ---
    try:
        e_url = f"https://apis.tianapi.com/everyday/index?key={TIAN_KEY.strip()}"
        e_res = requests.get(e_url, timeout=10).json()
        if e_res.get('code') == 200:
            res = e_res['result']
            # 对应你截图中的 content 和 note
            english_info = f"📖 每日英语：\n{res['content']}\n{res['note']}"
        else:
            english_info = f"每日英语获取失败: {e_res.get('msg')}"
    except:
        english_info = "每日英语接口异常"

    # --- 2. 早上时段 (6点-10点) 额外获取天气和运势 ---
    if 6 <= hour <= 10:
        title = "🌅 早安天津"
        # 天气
        try:
            w_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now?location=101030100&key={WEATHER_KEY.strip()}"
            w_res = requests.get(w_url, timeout=10).json()
            if w_res.get('code') == '200':
                now = w_res['now']
                weather_info = (
                    f"📍 天津实时天气：\n"
                    f"【状况】{now['text']} | 体感 {now['feelsLike']}°C\n"
                    f"【气温】{now['temp']}°C | 湿度 {now['humidity']}%\n"
                    f"【风力】{now['windDir']} {now['windScale']}级\n\n"
                )
        except:
            weather_info = "天气获取异常\n\n"

        # 运势
        try:
            s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY.strip()}&astro=狮子座"
            s_res = requests.get(s_url, timeout=10).json()
            if s_res.get('code') == 200:
                star_list = s_res['result'].get('list', [])
                star_info = "🦁 狮子座今日运势：\n" + "\n".join([f"· {i['type']}: {i['content']}" for i in star_list]) + "\n\n"
        except:
            star_info = "运势获取异常\n\n"
            
    elif 11 <= hour <= 15:
        title = "🍴 午间英语"
    else:
        title = "🌙 晚间英语"

    # 组合最终消息内容
    # 如果是早晨，会包含天气+运势+英语；如果是中晚，只显示英语
    final_msg = f"{weather_info}{star_info}{english_info}"
    return title, final_msg

if __name__ == "__main__":
    t, b = get_data()
    
    # 推送给 Bark
    params = {
        "title": t,
        "body": b,
        "group": "DailyLife",
        "icon": "https://img.icons8.com/clouds/100/000000/sun.png"
    }
    requests.post(f"https://api.day.app/{BARK_KEY}", data=params)
    print(f"DONE: {t} 已推送")
