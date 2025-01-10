import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st
import os

import re


# Load the pre-trained BERT model for sentiment analysis
model_name="nlptown/bert-base-multilingual-uncased-sentiment" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name) 

@st.cache_resource
# Clean comment function
def clean_comment(comment):
    # Remove emojis
    comment = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+', '', comment)
    
    # Remove URLs
    comment = re.sub(r'http\S+|www\S+|https\S+', '', comment, flags=re.MULTILINE)
    
    # Remove non-standard characters like backslashes, escaped quotes, etc.
    comment = re.sub(r'[\\\'\"]', '', comment)  # Remove backslashes, quotes
    
    # Remove non-alphanumeric characters except spaces and commas
    comment = re.sub(r'[^\w\s,]', '', comment)
    
    # Remove extra whitespace
    comment = comment.strip()

    # Debugging line to check the cleaned comment
    print(f"Cleaned comment: {comment}")
    
    return comment

@st.cache_resource
# Analyze Sentiments for a List of Comments
def analyze_sentiments(comments):
    sentiment_scores = {"positive": 0, "neutral": 0, "negative": 0}
    for comment in comments:
        if isinstance(comment, str):  
            inputs = tokenizer(comment, return_tensors="pt", truncation=True, padding=True)
            outputs = model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1).squeeze()
            
            # Classify sentiment based on the highest score
            sentiment = torch.argmax(scores).item()  # 0: Negative, 2: Neutral, 4: Positive
            if sentiment == 4:
                sentiment_scores["positive"] += 1
            elif sentiment == 0:
                sentiment_scores["negative"] += 1
            else:
                sentiment_scores["neutral"] += 1
        else:
            print("No comments found for sentiment analysis.")
            
    return sentiment_scores



