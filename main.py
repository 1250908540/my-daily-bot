import requests
import os

# 配置区 (建议直接在这里写死 Key 测试，成功后再改回 os.getenv)
WEATHER_KEY = "440e0c69838e4fb997475d59f20a3f85"  # 填入你那个以 440e 开头的字符串
TIAN_KEY = "c61886baf3e1feba3955bc4807e8e0eb"    # 填入天行数据后台看到的 APIKEY
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    weather_info = "校准中"
    try:
        # 1. 尝试获取天气 - 加上 headers 模拟浏览器，防止被拦截
        w_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now?location=101010100&key={WEATHER_KEY.strip()}"
        # https://your_api_host/v7/weather/now?location=101010100
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
