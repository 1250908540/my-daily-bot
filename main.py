import requests
import os

# 配置区 (建议直接在这里写死 Key 测试，成功后再改回 os.getenv)
WEATHER_KEY = "440e0c69838e4fb997475d59f20a3f85"  # 填入你那个以 440e 开头的字符串
TIAN_KEY = "c61886baf3e1feba3955bc4807e8e0eb"    # 填入天行数据后台看到的 APIKEY
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    weather_info = "天气待校准"
    try:
        # 使用 strip() 确保没有空格，使用 devapi 确保是免费版
        w_url = f"https://devapi.qweather.com/v7/weather/now?location=101010100&key={WEATHER_KEY.strip()}"
        res = requests.get(w_url)
        data = res.json()
        
        if data.get('code') == '200':
            weather_info = f"天气：{data['now']['text']} {data['now']['temp']}°C"
        else:
            # 如果失败，直接把 API 给的错误信息发出来
            weather_info = f"天气API反馈: {data.get('code', '无状态码')}"
            print(f"DEBUG 天气原始数据: {data}")
    except Exception as e:
        weather_info = f"程序解析异常: {str(e)[:20]}"

    return weather_info

if __name__ == "__main__":
    w = get_data()
    # 推送到手机查看原始报错
    requests.get(f"https://api.day.app/{BARK_KEY}/天气校准/{w}")
