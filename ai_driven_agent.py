import tweepy
import logging
import datetime
import time
import schedule

# API credentials
API_KEY = 'GqFRkE0i74LAK2Kr2PDEs78MF'
API_SECRET = 'aZI5nfGEJXsN7fe28kDeHw8A7hPZUm7ktBycJ4MJSOIKNGJr4p'
ACCESS_TOKEN = '1940400565542162433-a3wpE6Y2oCEc7hHEFuIYn5frnq9JOn'
ACCESS_SECRET = 'ciyj5XYOOUZzKrmoJODjBDrDDAGMWWohxWd9QFfY5vkJK'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize Tweepy Client for API v2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Daily Python tips
post_ideas = [
    "💡 Did you know? Python is named after the British comedy group Monty Python!",
    "⚡ Tip: Use list comprehensions for cleaner and more efficient code in Python.",
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
    start_date = datetime.date(2025, 6, 30)
    index = (today - start_date).days % len(post_ideas)

    message = post_ideas[index]
    try:
        client.create_tweet(text=message)
        logging.info(f"Posted: {message}")
    except Exception as e:
        logging.error(f"Failed to post: {e}")

# Schedule to run daily at a specific time
schedule.every().day.at("17:18").do(post_today_message)

if __name__ == "__main__":
    logging.info("Starting post agent...")
    while True:
        schedule.run_pending()
        time.sleep(60)
