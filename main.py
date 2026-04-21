import requests
import os

# 从 GitHub Secrets 中读取
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    # 1. 获取天气 (使用你刚才调通的专属 Host)
    weather_info = "天气获取失败"
    try:
        # 这里直接用你测试成功的那个专属域名
        w_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now?location=101010100&key={WEATHER_KEY.strip()}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(w_url, headers=headers)
        data = res.json()
        if data.get('code') == '200':
            w = data['now']
            weather_info = f"北京天气：{w['text']} {w['temp']}°C"
    except:
        weather_info = "天气接口异常"

    # 2. 获取星座运势 (天行数据)
    star_info = "运势获取失败"
    try:
        # 这里用的是狮子座，确保你点过“申请接口”
        s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY.strip()}&astro=狮子座"
        s_res = requests.get(s_url).json()
        if s_res.get('code') == 200:
            star_info = s_res['result'].get('content', '今日暂无运势数据')
        else:
            star_info = f"运势报错：{s_res.get('msg')}"
    except:
        star_info = "运势接口异常"

    return weather_info, star_info

if __name__ == "__main__":
    w, s = get_data()
    # 拼接最终消息
    final_msg = f"{w}\n\n🦁 狮子座运势：\n{s}"
    
    # 推送到 Bark
    push_url = f"https://api.day.app/{BARK_KEY}/早安简报/{final_msg}"
    requests.get(push_url)
    print("推送任务已完成！")
