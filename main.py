import requests
import os

# --- 配置区 ---
# 请在 GitHub Secrets 里增加一个 API_HOST，填入你后台看到的地址（比如 devapi.qweather.com）
API_HOST = os.getenv("API_HOST") 
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    weather_info = "校准中"
    try:
        # 直接把参数写在 params 字典里，由 Python 自动拼 URL，这样最稳！
        url = "https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now"
        params = {
            "location": "101010100",  # 北京的 ID
            "key": WEATHER_KEY.strip()
        }
        res = requests.get(url, params=params)
        data = res.json()
        
        # 打印出来在 Actions 日志里看一眼，这叫“自救式日志”
        print(f"DEBUG 返回的全部内容: {data}")
        
        # 兼容性判断
        if str(data.get('code')) == '200':
            now = data['now']
            weather_info = f"北京:{now['text']} {now['temp']}°C"
        else:
            # 如果拿不到 code，就把整个 data 变成字符串发给你
            weather_info = f"异常内容:{str(data)[:50]}"
            
    except Exception as e:
        weather_info = f"请求崩溃:{str(e)[:20]}"
        
    return weather_info
