import requests
import os

# 从 GitHub Secrets 读取
WEATHER_KEY = os.getenv("WEATHER_KEY")
TIAN_KEY = os.getenv("TIAN_KEY")
BARK_KEY = os.getenv("BARK_KEY")

def get_data():
    # 1. 获取天津详细天气 (天津 ID: 101030100)
    weather_info = "天气获取失败"
    try:
        # 使用你跑通的专属域名
        w_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now?location=101030100&key={WEATHER_KEY.strip()}"
        res = requests.get(w_url, timeout=10).json()
        
        if res.get('code') == '200':
            now = res['now']
            # 整合风向、降水、体感温度、湿度等
            weather_info = (
                f"📍 天津实时天气报：\n"
                f"【数据观测时间】 {now['obsTime']}\n"
                f"【状况】{now['text']} | 体感 {now['feelsLike']}°C\n"
                f"【气温】当前 {now['temp']}°C\n"
                f"【风向】{now['windDir']} {now['windScale']}级\n"
                f"【降水】{now['precip']}mm | 湿度 {now['humidity']}%"
            )
    except Exception as e:
        weather_info = f"天气接口异常: {str(e)[:20]}"

    # 2. 获取狮子座运势 (适配天行新版 list 结构)
    star_info = "运势内容解析失败"
    try:
        s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY.strip()}&astro=狮子座"
        s_res = requests.get(s_url, timeout=10).json()
        
        if s_res.get('code') == 200:
            # 这里的逻辑是：遍历 list，把所有的指数和描述拼接起来
            star_list = s_res['result'].get('list', [])
            if star_list:
                formatted_star = []
                for item in star_list:
                    # 每一项包含 type(标题) 和 content(内容)
                    formatted_star.append(f"· {item['type']}: {item['content']}")
                star_info = "\n".join(formatted_star)
            else:
                star_info = "今日暂无具体运势明细"
        else:
            star_info = f"运势接口报错：{s_res.get('msg')}"
    except Exception as e:
        star_info = f"运势解析异常: {str(e)[:20]}"

    return weather_info, star_info

if __name__ == "__main__":
    w, s = get_data()
    # 组合最终消息
    final_msg = f"{w}\n\n🦁 狮子座今日运势：\n{s}"
    
    # 推送到手机
    requests.get(f"https://api.day.app/{BARK_KEY}/{final_msg}")
