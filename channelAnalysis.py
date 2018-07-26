#!/usr/bin/python
# -*- coding: utf-8 -*-

# https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCelk6aHijZq-GJBBB9YpReA&maxResults=50&type=video&key=AIzaSyDzypKlAZrU1KbfMHxNpkDJBb2AIEsULgI
# https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id=T_PXMQJAkgU&key=AIzaSyDzypKlAZrU1KbfMHxNpkDJBb2AIEsULgI

import urllib
import urllib2
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDzypKlAZrU1KbfMHxNpkDJBb2AIEsULgI"
CHANNEL_ID = "UCelk6aHijZq-GJBBB9YpReA"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_RESULT = "50"


views = []
likes = []
dislikes = []
fav = []
comm = []
xVal = []
df = pd.DataFrame()


def get_platList():
    playListsUrl = "https://www.googleapis.com/youtube/v3/playlists?part="\
                    +"snippet%2CcontentDetails&channelId="\
                    +CHANNEL_ID+"&maxResults="+MAX_RESULT+"&key="+DEVELOPER_KEY
    playListResponse = urllib2.urlopen(playListsUrl)
    playListINFO = json.load(playListResponse)
    print "NO. Playlists: " ,len(playListINFO)
    for info in playListINFO['items']:
        print info['snippet']['localized']['title']
        print "NO. videos/playlist: ", info['contentDetails']['itemCount'], '\n'

def get_comments(video_id):
    try:
        url = "https://www.googleapis.com/youtube/v3/commentThreads?part="\
                +"snippet%2Creplies&videoId="+video_id+"&key="+DEVELOPER_KEY
        response = urllib2.urlopen(url)
        commentINFO = json.load(response)
        for item in commentINFO['items']:
            if len(commentINFO['items']) > 0:
                comment = item['snippet']['topLevelComment']
                author = comment['snippet']['authorDisplayName']
                text = comment['snippet']['textDisplay']
                likeCount = comment['snippet']['likeCount']
                print "Comment by %s: %s -- NO. likes: %s" % (author, text, likeCount)
    except urllib2.HTTPError as e:
        print("Error: ", e)
  # return results["items"]

def videos_list():
    videoMetadata = []
    videoTitle = []
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="\
            +CHANNEL_ID+"&maxResults="+MAX_RESULT+"&type=video&key="+DEVELOPER_KEY
    videosResponse = urllib2.urlopen(url)
    videos = json.load(videosResponse)

    for video in videos['items']:
      if video['id']['kind'] == 'youtube#video':
          videoMetadata.append(video['id']['videoId'])
          videoTitle.append(video['snippet']['title'])
    return videoMetadata, videoTitle


# def get_statistics():
metadata, title = videos_list()
for index, val in enumerate(metadata):
    # print videoTitle[index]
    xVal.append(title[index])
    # print "https://www.youtube.com/watch?v="+val
    # print videoTags
    videoID = val
    videoUrl = "https://www.googleapis.com/youtube/v3/videos?part="\
                +"snippet%2CcontentDetails%2Cstatistics&id="+videoID\
                +"&key="+DEVELOPER_KEY
    response = urllib2.urlopen(videoUrl)
    videoINFO = json.load(response)

    for info in videoINFO['items']:
      if info['kind'] == 'youtube#video':
          # if info['snippet'].has_key('publishedAt'):
              # print "Upload date:        "+info['snippet']['publishedAt']
          if info['statistics'].has_key('viewCount'):
              views.append(int(info['statistics']['viewCount']))
              # print "Number of views:    "+info['statistics']['viewCount']
          if info['statistics'].has_key('likeCount'):
              likes.append(int(info['statistics']['likeCount']))
              # print "Number of likes:    "+info['statistics']['likeCount']
          else:
              likes.append(-1)
              # print "Number of likes: Disabled"
          if info['statistics'].has_key('dislikeCount'):
              dislikes.append(int(info['statistics']['dislikeCount']))
              # print "Number of dislikes: "+info['statistics']['dislikeCount']
          else:
              dislikes.append(-1)
              # print "Number of Dislikes: Disabled"
          if info['statistics'].has_key('favoriteCount'):
              fav.append(int(info['statistics']['favoriteCount']))
              # print "Number of favorites:"+info['statistics']['favoriteCount']
          if info['statistics'].has_key('commentCount'):
              comm.append(int(info['statistics']['commentCount']))
              # print "Number of comments: "+info['statistics']['commentCount']
          else:
              comm.append(-1)
              # print "Number of comments: Disabled"
    # get_comments(videoID)
    # print "________________________________________________________________"

df['Title'] = xVal
df['Views'] = views
df['Likes'] = likes
# df['Dislikes'] = dislikes
df['Comments'] = comm
maxLikes = df['Likes'].max()
maxViews = df['Views'].max()
maxComm = df['Comments'].max()

print df[df['Likes'] == maxLikes]
print df[df['Views'] == maxViews]
print df[df['Comments'] == maxComm]
# print df


x = np.arange(1,int(MAX_RESULT)+1,1)
y = views
width = 0.35
_xticks = xVal
p1 = plt.figure(1)
plt.xticks(x,_xticks,rotation='vertical')
plt.xlabel('Video Title')
plt.ylabel('Number of Views/Video')
plt.title('Views Distribution')
plt.bar(x, y, width, align='center')
p1.show()

p2 = plt.figure(2)
plt.bar(x, likes, width, color='g', label='Likes', align='center')
plt.bar(x + width, dislikes, width, color='r', label='Dislikes', align='center')
plt.xlabel('Video Title')
plt.ylabel('Like & Dislikes')
plt.title('Like Engagement')
plt.xticks(x,_xticks,rotation='vertical')
p2.show()

raw_input()
