# Import necessary libraries
from transformers import pipeline

# Load a pre-trained sentiment-analysis model
classifier = pipeline('sentiment-analysis')

# Define a sample text
text = "I like using Hugging Face transformers library!"

# Use the model to make predictions
result = classifier(text)

# Print the result
print(result)
