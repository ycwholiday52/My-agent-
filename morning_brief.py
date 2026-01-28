import random

# A list of things to start your day right
messages = [
    "☀️ Good morning! Today is a fresh start. Go get 'em!",
    "☕ Coffee is brewing and the world is waiting. You got this.",
    "🚀 Reminder: You're building an AI agent. That's pretty cool.",
    "🌈 Make today so awesome yesterday gets jealous!"
]

if __name__ == "__main__":
    # This picks one at random and prints it for Telegram to see
    print(random.choice(messages))
