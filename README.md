import os
import datetime
import feedparser
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# --- CONFIG ---
WEATHER_API_KEY = "your_openweathermap_api_key"
CITY = "Hollister"
NEWS_RSS = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

class DailyDashboard:
    def get_weather(self):
        # Fetches real-time weather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        return f"{data['weather'][0]['description']}, {data['main']['temp']}°C"

    def get_top_news(self):
        # Pulls top 3 headlines
        feed = feedparser.parse(NEWS_RSS)
        return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:3]]

    def get_calendar(self):
        # Note: Requires credentials.json from Google Cloud Console
        # Cursor can help you set up the OAuth flow if you ask!
        return ["9:00 AM - Design Sprint", "2:00 PM - Gym", "6:00 PM - Dinner with AI"]

    def generate_prompt_for_ai(self):
        # This gathers everything to send to the LLM (Gemini/GPT-4)
        weather = self.get_weather()
        news = self.get_top_news()
        tasks = self.get_calendar()
        
        prompt = f"""
        Context for today ({datetime.date.today()}):
        Weather: {weather}
        Calendar: {tasks}
        News: {news}
        
        Task: Create a '10-minute morning vibe' summary. 
        Tone: Witty, concise, and motivating.
        Format: Markdown.
        """
        return prompt

# Run logic
if __name__ == "__main__":
    dashboard = DailyDashboard()
    print(dashboard.generate_prompt_for_ai())
