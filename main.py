def get_data():
    # 1. 获取天津详细天气 (天津 ID: 101030100)
    weather_info = "天气获取失败"
    try:
        # 使用你跑通的专属域名，location 改为天津 ID
        w_url = f"https://kt4d94dyn4.re.qweatherapi.com/v7/weather/now?location=101030100&key={WEATHER_KEY.strip()}"
        res = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
        
        if res.get('code') == '200':
            now = res['now']
            weather_info = (
                f"📍 天津当前天气：\n"
                f"【状况】{now['text']} \n"
                f"【气温】{now['temp']}°C (体感 {now['fl']}°C)\n"
                f"【风力】{now['windDir']} {now['windScale']}级\n"
                f"【湿度】{now['hum']}%  【降水】{now['precip']}mm"
            )
    except:
        weather_info = "天气接口访问异常"

    # 2. 获取狮子座运势
    star_info = "运势获取失败"
    try:
        # 确保已经在天行官网点击了“申请接口”
        s_url = f"https://apis.tianapi.com/star/index?key={TIAN_KEY.strip()}&astro=巨蟹座"
        s_res = requests.get(s_url).json()
        
        if s_res.get('code') == 200:
            # 优先获取今日概述
            star_info = s_res['result'].get('list', '今日暂无运势数据')
        else:
            star_info = f"运势报错：{s_res.get('msg')}(请确认官网已点申请接口)"
    except:
        star_info = "运势接口异常"

    return weather_info, star_info

if __name__ == "__main__":
    w, s = get_data()
    # 重新排版消息内容
    final_msg = f"{w}\n\n🦁 狮子座今日运势：\n{s}"
    
    # 推送
    requests.get(f"https://api.day.app/{BARK_KEY}/天津早安报/{final_msg}")
