import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import re
import preprocess
import matplotlib.pyplot as plt
import ast
import clean
import seaborn as sns

# Initialize session state for 'page' if it is not set
if 'page' not in st.session_state:
    st.session_state.page = 'input'  # Default to input page when app starts


def center_content():
    st.markdown(
         """
        <style>
        
        .circle-image {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            margin-bottom: 20px;  /* Space below the image */
        }
        
        </style>
        """, unsafe_allow_html=True
    )

# Main processing function
@st.cache_resource  
def process_comments(df):
    # Clean the comments
    df['comment'] = df['comment'].apply(clean.clean_comment)


    # Analyze sentiment for each comment
    print('df:',df)
    df['sentiment_scores'] = df['comment'].apply(
        lambda comment: clean.analyze_sentiments([comment])
    )
    print('commentdf',df)

    # Initialize sentiment counters
    total_sentiment = {"positive": 0, "neutral": 0, "negative": 0}

    # Aggregate sentiment scores
    for sentiment in df['sentiment_scores']:
        total_sentiment["positive"] += sentiment["positive"]
        total_sentiment["neutral"] += sentiment["neutral"]
        total_sentiment["negative"] += sentiment["negative"]

    print(' total_comments:', total_sentiment)
    # Calculate percentages
    total_comments = sum(total_sentiment.values())
    if total_comments > 0:
        positive_percent = (total_sentiment["positive"] / total_comments) * 100
        neutral_percent = (total_sentiment["neutral"] / total_comments) * 100
        negative_percent = (total_sentiment["negative"] / total_comments) * 100
        
    print('pos:',positive_percent,'neg:',negative_percent,'neu:', neutral_percent)

    return positive_percent, neutral_percent, negative_percent,df,total_sentiment
# Streamlit App UI
def main():
    # Check the current page in session state
    #st.write(f"Current Page: {st.session_state.page}")  # Debugging line

    # Page 1: Channel URL Input
    if st.session_state.page == 'input':
        st.title("Enter YouTube Channel URL")
        url = st.text_input("Enter YouTube Channel URL", "")
        
        if st.button("Submit"):
            try:

                channel_id = preprocess.get_channel_id_from_url(url)
                st.session_state.channel_url = url
                st.session_state.channel_id = channel_id
                st.session_state.page = "results"  # Switch to the results page
                st.experimental_rerun()  # Refresh and rerun the app
            except Exception as e:
                st.error(f"Error: {e}")

    # Page 2: Results Page
    elif st.session_state.page == "results":
        st.title("YouTube Channel Insights")
        
        # Add a check to see if channel details are fetched
        try:
            channel_details = preprocess.get_channel_details(st.session_state.channel_id)
            videoid = preprocess.video_ids( channel_details['playlistId'])
            df=preprocess.get_comments_in_videos(videoid)  
            # preproceesing videodetais dataframe
            
            video_details=preprocess.get_video_details(videoid)
            numeric_cols=['viewCount','likeCount','commentCount']
            video_details [numeric_cols] = video_details[numeric_cols].apply(pd.to_numeric, errors = 'coerce', axis = 1)
            video_details['publishedAt'] = pd.to_datetime(video_details['publishedAt'])
            video_details['pushblishDayName'] = video_details['publishedAt'].dt.day_name()
            video_details['publishedAt']=video_details['publishedAt'].dt.date
            # Add tag count
            video_details['tagCount'] = video_details['tags'].apply(lambda x: 0 if x is None else len(x))
            # Convert the 'duration' column to a timedelta object
            video_details['durationMinutes'] = pd.to_timedelta(video_details['duration'])

            # Convert the timedelta to total minutes
            video_details['durationMinutes'] = video_details['durationMinutes'].dt.total_seconds() / 60

            # Apply CSS for centering content
            center_content()

            # Display channel image in circle
            st.markdown(f'<img class="circle-image" src="{channel_details["profile_pic"]}">', unsafe_allow_html=True)

            
            st.header(channel_details['name'])
            st.write(channel_details['description'])
            #statistics
            col1,col2,col3,col4=st.columns(4)
            with col1:
                st.subheader('Subscribers')
                subscribers=channel_details['subscribers']
                st.markdown(f"<h2 style='font-size: 30px;'>{subscribers:,}</h2>", unsafe_allow_html=True)
            with col2:
                st.subheader('Total Views')
                Total_views=channel_details['views']
                st.markdown(f"<h2 style='font-size: 30px;'>{Total_views:,}</h2>", unsafe_allow_html=True)
            with col3:
                st.subheader('Total Videos')
                total_videos=channel_details['total_videos']
                st.markdown(f"<h2 style='font-size: 30px;'>{total_videos}</h2>", unsafe_allow_html=True)
          
            positive_percent,negative_percent,neutral_percent,comment_df,total_sentiment= process_comments(df)

            video_ids = comment_df['video_id'].unique()  # Assuming 'video_id' column exists
            total_comments = len(df)  # Total comments in the comment_df
            total_videos = len(video_ids)  # Total videos in video_df
    
            avg_comments = total_comments / total_videos
            print(avg_comments)

            with col4:
                st.subheader('Avg Comments')
                total_videos=channel_details['total_videos']
                st.markdown(f"<h2 style='font-size: 30px;'>{avg_comments:.2f}</h2>", unsafe_allow_html=True)

            # Save sentiment analysis results to a CSV
            def save_to_csv(data, filename="sentiment_results.csv"):
                df = pd.DataFrame(data)
                df.to_csv(filename, index=False)
                print(f"Sentiment results saved to {filename}")

            saved=save_to_csv(comment_df)
          
           


            col1,col2=st.columns(2)
            with col1:
            # Highlight Videos
                st.subheader("Top Viewed Videos")
                top_video = video_details.sort_values(by="viewCount", ascending=False).iloc[0]
                # Embed the YouTube video using iframe
                st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; width: 100%; border: 2px solid #ccc; border-radius: 10px; padding: 10px;">
                        <h3>{top_video['title']}</h3>
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/{top_video['video_id']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.subheader("Lowest Viewed Videos")
                lowest_video = video_details.sort_values(by="viewCount", ascending=True).iloc[0]
                st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; width: 100%; border: 2px solid #ccc; border-radius: 10px; padding: 10px;">
                        <h3>{lowest_video['title']}</h3>
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/{lowest_video['video_id']}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                """, unsafe_allow_html=True)
            
            # sentiment analysis
            st.header('Overall Sentiment Analysis')
            col1,col2,col3=st.columns(3)

            with col1:
                st.header('Postive Comments')
                st.subheader(f"{positive_percent:.2f}%") 
            print(positive_percent)

            with col2:
                st.header('Negative Comments')
                st.subheader(f"{negative_percent:.2f}%") 
            print(negative_percent)

            with col3:
                st.header('Neutral Comments')
                st.subheader(f"{neutral_percent:.2f}%") 
            print(neutral_percent) 
            
           # Create a DataFrame
            sent_df = pd.DataFrame({
                "Sentiment": total_sentiment.keys(),
                "Count": total_sentiment.values()
            })

            # Display Bar Chart
            st.header("Sentiment Analysis Results")
         
            
            # Sentiment plot
            fig, ax = plt.subplots(figsize=(8, 5))
            # Sentiment plot with Matplotlib

            ax.bar(sent_df["Sentiment"], sent_df["Count"], color=['#AEC6CF', '#77DD77', '#FFB347'])
            ax.set_xlabel('Sentiment')
            st.pyplot(fig)

            # Plotting the growth over time
            st.header('Growth Over Time ')
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(video_details['publishedAt'],video_details['viewCount'] , label='Views', color='#AEC6CF')
            ax.plot(video_details['publishedAt'],video_details['likeCount'], label='like', color='#77DD77')
            ax.plot(video_details['publishedAt'], video_details['commentCount'], label='comment', color='#FFB347')
            
            ax.set_xlabel('Date')
            ax.set_ylabel('Count')
            ax.set_title('Growth Over Time')
            ax.legend()
            st.pyplot(fig)


            col1,col2=st.columns(2)
            with col1:
                st.header('ViewCount Plot')
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.violinplot( video_details['viewCount'], color='#ee8c8c')
                st.pyplot(fig)
               

            with col2:
                st.header('Video Publishing Frequency by Day of the Week')
                fig, ax = plt.subplots(figsize=(10, 6))
                day_df = video_details['pushblishDayName'].value_counts()
                weekdays = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_df = day_df.reindex(weekdays)
                day_df.plot(kind='bar',x='pushblishDayName',y='count',color='#bb5567')
                # Set labels and title
                ax.set_xlabel('Day of the Week')
                ax.set_ylabel('Number of Videos')
                st.pyplot(fig)

            st.header('Video Duration Analysis')
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(video_details['durationMinutes'], bins=30, ax=ax, color='#db9a9a')

            st.pyplot(fig)


        except Exception as e:
            st.error(f"Error fetching channel details: {e}")

if __name__ == "__main__":
    main()
