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
    
    title = "定时简报"
    weather_info, star_info, english_info = "", "", ""

    # --- 1. 获取每日英语 (早中晚都发) ---
    try:
        e_url = f"https://apis.tianapi.com/everyday/index?key={TIAN_KEY.strip()}"
        e_res = requests.get(e_url, timeout=10).json()
        if e_res.get('code') == 200:
            res = e_res['result']
            english_info = f"📖 每日英语：\n{res['content']}\n{res['note']}"
        else:
            english_info = f"每日英语获取失败"
    except:
        english_info = "每日英语接口异常"

    # --- 2. 早上时段 (06-10点): 实时天气 + 运势 ---
    if 6 <= hour <= 10:
        title = "🌅 早安天津"
        try:
            # 实时天气
            w_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now?location=101030100&key={WEATHER_KEY.strip()}"
            w_res = requests.get(w_url, timeout=10).json()
            if w_res.get('code') == '200':
                now = w_res['now']
                weather_info = (
                    f"📍 天津实时天气：\n"
                    f"【状况】{now['text']} | 体感 {now['feelsLike']}°C\n"
                    f"【风力】{now['windDir']} {now['windScale']}级\n\n"
                )
            # 运势
            s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY.strip()}&astro=狮子座"
            s_res = requests.get(s_url, timeout=10).json()
            if s_res.get('code') == 200:
                star_list = s_res['result'].get('list', [])
                star_info = "🦁 狮子座今日运势：\n" + "\n".join([f"· {i['type']}: {i['content']}" for i in star_list]) + "\n\n"
        except:
            pass

    # --- 3. 晚上时段 (19-23点): 预报明天天气 ---
    elif 19 <= hour <= 23:
        title = "🌙 晚安天津"
        try:
            # 获取未来3天天气预报
            # 注意：此处同样使用你跑通的专属域名
            forecast_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/3d?location=101030100&key={WEATHER_KEY.strip()}"
            f_res = requests.get(forecast_url, timeout=10).json()
            if f_res.get('code') == '200':
                # daily[1] 代表明天
                tomorrow = f_res['daily'][1]
                weather_info = (
                    f"📅 明日天气预报 ({tomorrow['fxDate']})：\n"
                    f"【状况】白昼 {tomorrow['textDay']} | 夜间 {tomorrow['textNight']}\n"
                    f"【气温】{tomorrow['tempMin']}°C ~ {tomorrow['tempMax']}°C\n"
                    f"【风向】{tomorrow['windDirDay']} {tomorrow['windScaleDay']}级\n"
                    f"【紫外线】指数 {tomorrow['uvIndex']}\n\n"
                )
        except:
            weather_info = "明日预报获取失败\n\n"

    # --- 4. 中午时段 ---
    elif 11 <= hour <= 15:
        title = "🍴 午间英语"

    final_msg = f"{weather_info}{star_info}{english_info}"
    return title, final_msg

if __name__ == "__main__":
    t, b = get_data()
    params = {"title": t, "body": b, "group": "DailyLife"}
    requests.post(f"https://api.day.app/{BARK_KEY}", data=params)
