import requests
import os

# 配置区 (建议直接在这里写死 Key 测试，成功后再改回 os.getenv)
WEATHER_KEY = "440e0c69838e4fb997475d59f20a3f85"  # 填入你那个以 440e 开头的字符串
TIAN_KEY = "c61886baf3e1feba3955bc4807e8e0eb"    # 填入天行数据后台看到的 APIKEY
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    # 1. 获取天气
    w_info = "天气获取失败"
    try:
        # 强制使用免费版 devapi 域名
        url = f"https://devapi.qweather.com/v7/weather/now?location=101010100&key={WEATHER_KEY.strip()}"
        res = requests.get(url).json()
        if res.get('code') == '200':
            w_info = f"北京天气：{res['now']['text']} {res['now']['temp']}°C"
        else:
            w_info = f"天气报错:{res.get('code')}"
    except:
        w_info = "天气网络异常"

    # 2. 获取运势 (尝试狮子座)
    s_info = "运势获取失败"
    try:
        # 这里尝试用中文名，记得去后台点“申请接口”按钮
        s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY.strip()}&astro=狮子座"
        res = requests.get(s_url).json()
        if res.get('code') == 200:
            s_info = res['result'].get('content', '今日暂无运势数据')
        else:
            s_info = f"运势报错:{res.get('msg')}"
    except:
        s_info = "运势网络异常"

    return w_info, s_info

if __name__ == "__main__":
    w, s = get_data()
    msg = f"{w}\n\n运势：{s}"
    # 最终推送
    requests.get(f"https://api.day.app/{BARK_KEY}/早安校准/{msg}")
