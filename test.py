import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

# Import necessary libraries
from transformers import pipeline

# Load a different pre-trained sentiment-analysis model
classifier = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

# Define a sample text
text = "I hate you"

# Use the model to make predictions
result = classifier(text)

# Map star ratings to descriptive labels
star_to_label = {
    '1 star': 'Very Negative',
    '2 stars': 'Negative',
    '3 stars': 'Neutral',
    '4 stars': 'Positive',
    '5 stars': 'Very Positive'
}

# Get the label and score from the result
label = result[0]['label']
score = result[0]['score']

# Print the human-readable sentiment
print(f"The sentiment is: {star_to_label[label]} with a confidence score of {score:.2f}")