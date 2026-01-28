import os
import datetime
import feedparser
import requests

# --- 配置 ---
# 建议在 GitHub Secrets 中设置这些，或者直接暂时填在这里测试
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WEATHER_API_KEY = "f7f9876543210fedcba9876543210" # 替换成你的 OpenWeatherMap Key
CITY = "Hollister"
NEWS_RSS = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

class DailyDashboard:
    def get_weather(self):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=imperial" # 改成了加州常用的华氏度
            data = requests.get(url).json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            return f"{desc}, {temp}°F"
        except:
            return "Weather unavailable (check your API key)"

    def get_top_news(self):
        feed = feedparser.parse(NEWS_RSS)
        headlines = [f"• {entry.title}" for entry in feed.entries[:3]]
        return "\n".join(headlines)

    def generate_report(self):
        weather = self.get_weather()
        news = self.get_top_news()
        
        # 组装最终发给手机的文本
        report = f"☕️ **Good Morning, Hollister!**\n"
        report += f"📅 {datetime.date.today().strftime('%A, %b %d')}\n\n"
        report += f"🌤 **Weather:** {weather}\n\n"
        report += f"📰 **Top Headlines:**\n{news}\n\n"
        report += f"✨ *Have a great day!*"
        return report

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    dashboard = DailyDashboard()
    briefing = dashboard.generate_report()
    
    # 如果有 Token 就发到手机，没有就打印出来
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        send_to_telegram(briefing)
        print("Briefing sent to Telegram!")
    else:
        print(briefing)
