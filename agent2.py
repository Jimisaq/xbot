import requests

# Replace this with your actual Bearer Token from Twitter Developer Portal
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAALBt2wEAAAAAk1DBdJIDaJXd15%2BUoaJZBBhrJ68%3DL4hKVwFFJR0AbWXYnF6lw9HcNvnXSUNiRag1QIz9KL2bPs2Bmi"

# Set up authentication header
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# Function to fetch recent tweets for a given hashtag
def get_trending_tweets(query="#Uganda", max_results=20):
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "public_metrics,created_at",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}, {response.text}")
        return []

    tweets = response.json().get("data", [])

    # Sort tweets by like count in descending order
    tweets.sort(key=lambda t: t['public_metrics']['like_count'], reverse=True)

    return tweets

# Main function
def show_most_trending_tweet():
    print("🔍 Fetching trending tweets in Uganda...")
    tweets = get_trending_tweets("#Uganda", max_results=20)

    if not tweets:
        print("⚠️ No tweets found or request failed.")
        return

    top = tweets[0]
    print("\n🔥 Most Trending Tweet in Uganda:")
    print(f"📅 Date: {top['created_at']}")
    print(f"💬 Tweet: {top['text']}")
    print(f"❤️ Likes: {top['public_metrics']['like_count']}")
    print(f"🔁 Retweets: {top['public_metrics']['retweet_count']}")
    print(f"💬 Replies: {top['public_metrics']['reply_count']}")
    print(f"📌 Quote Tweets: {top['public_metrics']['quote_count']}")

if __name__ == "__main__":
    show_most_trending_tweet()
