import warnings
from transformers import pipeline
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Suppress specific warnings from the transformers library
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

# Initialize sentiment analysis pipeline with a specific model
classifier = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

# Map star ratings to descriptive labels
star_to_label = {
    '1 star': 'Very Negative',
    '2 stars': 'Negative',
    '3 stars': 'Neutral',
    '4 stars': 'Positive',
    '5 stars': 'Very Positive'
}

# Initialize Slack client with the token from environment variables
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

# Function to analyze sentiment of a given text
def analyze_sentiment(text):
    result = classifier(text)
    label = result[0]['label']
    score = result[0]['score']
    return star_to_label[label], score

# Function to fetch messages from a specific Slack channel
def fetch_messages(channel_id):
    try:
        response = client.conversations_history(channel=channel_id)
        messages = response['messages']
        return messages
    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        return []

# Function to fetch username from user ID
def fetch_username(user_id):
    try:
        response = client.users_info(user=user_id)
        return response['user']['name']
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")
        return user_id  # Fallback to user ID if username cannot be fetched

# Function to post a message to a specific Slack channel
def post_message(channel_id, text):
    try:
        response = client.chat_postMessage(channel=channel_id, text=text)
    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")

# Main function to fetch messages, analyze sentiment, and post results
def main():
    channel_id = "C07N80P6S77"  # Replace with your actual channel ID
    messages = fetch_messages(channel_id)
    
    user_sentiments = {}
    
    # Analyze sentiment for each message and aggregate by user
    for message in messages:
        user = message.get('user')
        text = message.get('text')
        if user and text:
            sentiment, score = analyze_sentiment(text)
            if user not in user_sentiments:
                user_sentiments[user] = []
            user_sentiments[user].append((sentiment, score))
    
    # Determine overall sentiment and average confidence score for each user
    overall_sentiments = {}
    for user, sentiments in user_sentiments.items():
        max_sentiment = max(sentiments, key=lambda x: x[1])[0]
        avg_score = sum(score for _, score in sentiments) / len(sentiments)
        overall_sentiments[user] = (max_sentiment, avg_score)
    
    # Prepare result text
    result_text = "Sentiment Analysis Results:\n"
    for user, (sentiment, avg_score) in overall_sentiments.items():
        username = fetch_username(user)
        result_text += f"User {username}: {sentiment} (Confidence: {avg_score:.2f})\n"
    
    # Post the result text to the Slack channel
    post_message(channel_id, result_text)

# Entry point of the script
if __name__ == "__main__":
    main()