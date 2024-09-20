from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from transformers import pipeline

# Hugging Face sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

# Slack bot token (replace with your own bot token)
client = WebClient(token='')

# Function to process sentiment analysis
def analyze_message(text):
    result = sentiment_pipeline(text)
    return f"Sentiment: {result[0]['label']} with score: {result[0]['score']:.2f}"

# Send a response to a Slack channel
def send_message(channel, text):
    try:
        response = client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

# Handle incoming messages and respond with sentiment analysis
def handle_event(event_data):
    text = event_data['event']['text']
    channel = event_data['event']['channel']
    sentiment_result = analyze_message(text)
    send_message(channel, sentiment_result)