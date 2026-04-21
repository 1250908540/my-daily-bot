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
        # 1. 尝试获取天气 - 加上 headers 模拟浏览器，防止被拦截
        w_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now?location=101010100&key={WEATHER_KEY.strip()}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(w_url, headers=headers)
        
        # 关键：先打印出前100个字符，看看返回的是不是 <html>
        print(f"DEBUG 原始返回内容: {res.text[:100]}")
        
        try:
            data = res.json()
            if data.get('code') == '200':
                weather_info = f"天气：{data['now']['text']} {data['now']['temp']}°C"
            else:
                weather_info = f"和风报错码：{data.get('code')}"
        except:
            # 如果不是 JSON，说明返回了 HTML 报错页
            if "Invalid Host" in res.text:
                weather_info = "域名/Key不匹配(请检查是否为devapi)"
            elif "403" in res.text:
                weather_info = "和风403拒绝访问(请确认后台无IP限制)"
            else:
                weather_info = "API返回了非JSON格式数据"
                
    except Exception as e:
        weather_info = f"网络请求异常"
        
    return weather_info

if __name__ == "__main__":
    w = get_data()
    # 把详细错误推送到手机
    requests.get(f"https://api.day.app/{BARK_KEY}/最终定位/{w}")
