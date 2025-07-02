import tweepy
import random
import logging
import datetime
import time

# Tweepy authentication
API_KEY = '8cX1q5YZIfsUrnMrauUS7XnjD'
API_SECRET = '6pzffkZGkzqUyWXO0PLnoV71VcwuTnM0k8XtGL6MHAdJZxmZKN'
ACCESS_TOKEN = '1939963629522034688-3wrhImORGAif3vZ1eTWcgBWStpWQMR'
ACCESS_SECRET = 'jrW7g7ZUfguu1pB7grZmVmQ4ecBpbZMMlpho3XTjciJXB'

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Posts - 30 engaging Python tips and facts for daily posting
post_ideas = [
    "💡 Did you know? Python is named after the British comedy group Monty Python!",
    "⚡ Tip: Use list comprehensions for cleaner and more efficient code in Python.",
    "📚 Python's Zen: 'Readability counts.' Always write code that is easy to read and understand.",
    "🎉 Fun fact: Python was created by Guido van Rossum and first released in 1991.",
    "🔄 Python supports multiple programming paradigms: procedural, object-oriented, and functional programming.",
    "💬 Did you know? Python has a built-in function called 'help()' that provides documentation for any object or module.",
    "📖 Python's standard library is vast and includes modules for everything from web development to data analysis.",
    "🌐 Tip: Use virtual environments to manage dependencies for different Python projects.",
    "🧘 Python's 'import this' command reveals the Zen of Python - guiding principles for writing computer programs.",
    "🚀 Python is widely used in data science, machine learning, web development, automation, and many other fields.",
    "👥 Python has a large and active community that contributes to its growth and development worldwide.",
    "🐍 Python's syntax is designed to be readable and straightforward, making it perfect for beginners.",
    "⚙️ Python is interpreted, not compiled, which makes development and testing faster.",
    "🔧 Use f-strings for string formatting: f'Hello {name}!' - cleaner than .format() or % formatting.",
    "📊 Python excels in data visualization with libraries like Matplotlib, Plotly, and Seaborn.",
    "🤖 Machine learning in Python is powered by libraries like scikit-learn, TensorFlow, and PyTorch.",
    "🌍 Python runs on virtually every operating system: Windows, macOS, Linux, and more.",
    "💾 Python's garbage collection automatically manages memory, reducing memory leaks.",
    "🔍 Use enumerate() when you need both index and value in loops: for i, item in enumerate(list):",
    "📦 pip is Python's package installer - use 'pip install package_name' to add new libraries.",
    "🎯 Python follows the principle 'There should be one obvious way to do it' (from Zen of Python).",
    "🔒 Python supports multiple inheritance, but be careful - it can make code complex!",
    "⏰ Use time.sleep() to pause execution, but consider asyncio for better performance in async code.",
    "📝 Python's docstrings help document your functions: use triple quotes for multi-line descriptions.",
    "🔄 List slicing is powerful: my_list[start:end:step] gives you flexible data extraction.",
    "🧮 Python handles big integers automatically - no overflow errors like in other languages!",
    "🎨 Code formatting matters: Use tools like Black or autopep8 to maintain consistent style.",
    "🔧 Python's lambda functions are perfect for short, one-line functions in functional programming.",
    "📈 Python's popularity continues to grow - it's consistently ranked as one of the top programming languages.",
    "🎓 Whether you're a beginner or expert, Python's simplicity and power make it an excellent choice for any project!"
]

def post_today_message():
    today = datetime.date.today()
    start_date = datetime.date(2025, 6, 30)  # Set your starting date
    index = (today - start_date).days % len(post_ideas)

    message = post_ideas[index]
    try:
        api.update_status(message)
        logging.info(f"Posted: {message}")
    except Exception as e:
        logging.error(f"Failed to post: {e}")

# Scheduler (once per day at a fixed time)
import schedule

schedule.every().day.at("11:57").do(post_today_message)

if __name__ == "__main__":
    logging.info("Starting post agent...")
    while True:
        schedule.run_pending()
        time.sleep(60)
