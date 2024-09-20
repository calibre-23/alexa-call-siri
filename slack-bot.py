import warnings
from transformers import pipeline
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

# Initialize sentiment analysis pipeline
classifier = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

# Map star ratings to descriptive labels
star_to_label = {
    '1 star': 'Very Negative',
    '2 stars': 'Negative',
    '3 stars': 'Neutral',
    '4 stars': 'Positive',
    '5 stars': 'Very Positive'
}

# Initialize Slack client
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

def analyze_sentiment(text):
    result = classifier(text)
    label = result[0]['label']
    score = result[0]['score']
    return star_to_label[label], score

def fetch_messages(channel_id):
    try:
        response = client.conversations_history(channel=channel_id)
        messages = response['messages']
        return messages
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        return []
    
def fetch_username(user_id):
    try:
        response = client.users_info(user=user_id)
        return response['user']['name']
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
        return user_id  # Fallback to user ID if username cannot be fetched

def post_message(channel_id, text):
    try:
        response = client.chat_postMessage(channel=channel_id, text=text)
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")

def main():
    channel_id = "C07NCK4MNJG"
    messages = fetch_messages(channel_id)
    
    user_sentiments = {}
    
    for message in messages:
        user = message.get('user')
        text = message.get('text')
        if user and text:
            sentiment, score = analyze_sentiment(text)
            if user not in user_sentiments:
                user_sentiments[user] = []
            user_sentiments[user].append((sentiment, score))
    
    overall_sentiments = {user: max(sentiments, key=lambda x: x[1])[0] for user, sentiments in user_sentiments.items()}
    
    result_text = "Sentiment Analysis Results:\n"
    for user, sentiment in overall_sentiments.items():
        result_text += f"User {user}: {sentiment}\n"
    
    post_message(channel_id, result_text)

if __name__ == "__main__":
    main()