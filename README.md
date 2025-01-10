# YouTube Channel Insights and Sentiment Analysis Using BERT

This repository provides tools to analyze YouTube channel insights and perform sentiment analysis on video comments using the BERT model. The project offers valuable metrics and sentiment insights to understand audience engagement better.

### Sentiment Analysis
https://github.com/user-attachments/assets/40beedff-8245-4571-a3ae-35176ea37e4b

## Features
- Extract video and channel details such as views, likes, comments, total subscribers, and average comments.
- Generate video detail and comment DataFrames for detailed analysis.
- Perform sentiment analysis (positive, negative, neutral) on YouTube comments using BERT.
- Visualize data through:
  - Video duration vs. view count plot.
  - Video publishing frequency by day of the week.
  - Growth trends over time.
  - Top and least-watched videos.
- Display summary statistics such as total views, total subscribers, and average comments.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-channel-insights.git
   cd youtube-channel-insights
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

The main libraries used in this project are:
- `transformers`: For using the BERT model for sentiment analysis.
- `google-api-python-client`: For accessing YouTube Data API.
- `streamlit`: For creating the user interface.
- `matplotlib` and `seaborn`: For visualizations.
- `pandas` and `numpy`: For data manipulation.

## Setup

1. **Get a YouTube Data API Key:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the YouTube Data API v3.
   - Generate an API key and add it to the environment variable or configuration file.

2. **Add API Key to Configuration:**
   Update the API key in the `config.py` or set it as an environment variable.

## Code Structure

- `app.py`: Main Streamlit app for running the analysis and visualizations.
- `clean.py`: Script for cleaning and preprocessing the comments DataFrame for sentiment analysis and doing sentiment analysis.
- `preprocess.py`: Handles fetching channel details, video details, and generating DataFrames for analysis.

### `requirements.txt`
```plaintext
transformers
google-api-python-client
streamlit
matplotlib
seaborn
pandas
numpy
```

## Usage

1. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

2. **Web Interface:**
   - Open your browser and navigate to the provided Streamlit URL.
   - Enter the YouTube channel or video URL.
   - View insights, sentiment analysis, and visualizations.

## What Happens When You Input a YouTube Link:
1. **Fetch Data:**
   - Extracts channel details (name, total views, total subscribers, etc.).
   - Fetches video details (titles, durations, view counts, publish dates, etc.).
   - Generates DataFrames for video and comment analysis.

2. **Process Comments:**
   - Cleans and preprocesses the comments for analysis.
   - Performs sentiment analysis using the BERT model.

3. **Display Insights:**
   - **Summary Statistics:** Total views, total subscribers, average comments.
   - **Top and Least-Watched Videos:** Key metrics for the most and least popular videos.
   - **Sentiment Analysis:** Bar chart displaying the proportion of positive, neutral, and negative comments.
   - **Visualizations:**
     - Video duration 
     - view count plot.
     - Video publishing frequency by day of the week.
     - Channel growth trends over time.

## Key Visualizations
- **Sentiment Analysis:** Bar chart displaying the proportion of positive, neutral, and negative comments.
- **Video Duration:** bar plot shows how video duration impacts views.
- **View Count:** dist plot showing how view count changes.
- **Video Publishing Frequency:** Heatmap showing publishing trends by the day of the week.
- **Channel Growth Over Time:** Line chart visualizing growth trends.
- **Top and Least-Watched Videos:** Lists displaying key metrics for the most and least popular videos.

## Future Enhancements
- Add support for multilingual sentiment analysis.
- Deploy the app on a cloud platform like Streamlit Sharing or AWS.
- Include additional visualizations and metrics.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to contribute by submitting issues or pull requests!
