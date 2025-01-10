import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
import re

# Initialize the YouTube API client
@st.cache_resource
def youtube_client():
    api_key = "YOUR_API_KEY"
    return build('youtube', 'v3', developerKey=api_key)

# Function to extract channel ID from URL
@st.cache_resource
def get_channel_id_from_url(url):
    youtube = youtube_client()
    if '/@' in url:
        username = re.search(r'/@([\w\d\-_.]+)', url).group(1)
        request = youtube.search().list(part="snippet", q=username,type='channel', maxResults=1)
        response = request.execute()
        return response['items'][0]['snippet']['channelId']
    elif '/channel/' in url:
        return re.search(r'/channel/([\w\d\-_.]+)', url).group(1)
    else:
        raise ValueError("Invalid YouTube URL format.")

# Function to get channel details from YouTube API
@st.cache_resource
def get_channel_details(channel_id):
     
    youtube = youtube_client()
    request = youtube.channels().list(part="snippet,statistics,contentDetails", id=channel_id)
    response = request.execute()
    data = response['items'][0]
    return {
        "name": data['snippet']['title'],
        "description": data['snippet']['description'],
        "profile_pic": data['snippet']['thumbnails']['default']['url'],
        "subscribers": int(data['statistics']['subscriberCount']),
        "views": int(data['statistics']['viewCount']),
        "total_videos": int(data['statistics']['videoCount']),
        "playlistId":data['contentDetails']['relatedPlaylists']['uploads'] 
    }
@st.cache_resource
def video_ids(playlist_id):

    video_ids=[]
    youtube = youtube_client()
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
    next_page_token=response.get('nextPageToken')
    
    while next_page_token is not None:
        request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50,
        pageToken=next_page_token)
        response = request.execute()
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
            next_page_token=response.get('nextPageToken')
        
    return video_ids

@st.cache_resource
def get_video_details(video_ids):
    
    youtube = youtube_client() 
    all_video_info = []

    for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_ids[i:i+50]
            )
            response = request.execute() 
    
            for video in response['items']:
                stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                                 'statistics': ['viewCount', 'likeCount','commentCount','dislikeCount'],
                                 'contentDetails': ['duration', 'definition', 'caption']
                                }
                video_info = {}
                video_info['video_id'] = video['id']
    
                for k in stats_to_keep.keys():
                    for v in stats_to_keep[k]:
                        try:
                            video_info[v] = video[k][v]
                        except:
                            video_info[v] = None
    
                all_video_info.append(video_info)
    return pd.DataFrame(all_video_info)

@st.cache_resource
def get_comments_in_videos(video_ids):

    youtube = youtube_client()
    all_comments = []
    
    for video_id in video_ids:
        try:   
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id
            )
            response = request.execute()

             # Check if response has comments
            if 'items' not in response or not response['items']:
                print(f"No comments available for video {video_id}")
                continue
        
            # Extract comments and create individual rows for each comment
            for comment in response['items'][:10]:  # Limit to first 10 comments
                comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
                all_comments.append({'video_id': video_id, 'comment': comment_text})
            
        except: 
            # When error occurs - most likely because comments are disabled on a video
            print('Could not get comments for video ' + video_id)
             
    return pd.DataFrame(all_comments) 
