import requests
import os

# --- 配置区 ---
# 请在 GitHub Secrets 里增加一个 API_HOST，填入你后台看到的地址（比如 devapi.qweather.com）
API_HOST = os.getenv("API_HOST") 
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    weather_info = "天气获取中"
    try:
        # 手动拼接完整的 URL
        # 此时 URL 会变成 https://你的HOST/v7/weather/now?...
        url = f"https://{API_HOST.strip()}/v7/weather/now"
        params = {
            "location": "101010100", 
            "key": WEATHER_KEY.strip()
        }
        
        res = requests.get(url, params=params)
        data = res.json()
        
        # 调试核心：输出最终生成的完整 URL（隐藏 Key）
        print(f"DEBUG 请求域名: {API_HOST}")
        print(f"DEBUG 完整返回数据: {data}")

        if str(data.get('code')) == '200':
            now = data['now']
            weather_info = f"天气：{now['text']} {now['temp']}°C"
        else:
            weather_info = f"错误码：{data.get('code')} 内容：{data.get('msg', '无信息')}"
            
    except Exception as e:
        weather_info = f"请求崩溃：{str(e)[:30]}"
        
    return weather_info

if __name__ == "__main__":
    w = get_data()
    # 天行数据的星座部分保持你之前的申请状态
    # 这里我们先只测试天气是否打通
    requests.get(f"https://api.day.app/{BARK_KEY}/Host校准/{w}")
