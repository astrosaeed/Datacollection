from apiclient.discovery import build
import psycopg2
import youtube
import sys
import json
import datetime, threading
from psycopg2.extras import execute_values
import time
import config 

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)


class Datacollection:

    def __init__(self):

        with open('channels_upload_id.json') as json_file:
            self.allchannelsdict = json.load(json_file)


        self.last_index =0


    def get_video_stats(self, videoID):


        result = youtube.videos().list(
            id = videoID,
            part = "statistics",
        ).execute()

        return result['items'][0]['statistics']


    def update_video_stats(self, videoID):


        result = youtube.videos().list(
            id = videoID,
            part = "snippet,statistics",
        ).execute()
        #print result['items'][0]['statistics']
        return result['items'][0]['statistics'],result['items'][0]['snippet']



    def get_upload_playlist(self, channelname, uploadID,num_page):

       # crawled_dict={}
        alloutput=[]
        only_vid=[]
        items =[]
        token =None
        playlist_response = youtube.playlistItems().list(playlistId=uploadID,
                                            part = "snippet",pageToken=token).execute()
        items.append(playlist_response)


        for video in  (items[0]['items']):

            stats = self.get_video_stats(video['snippet']['resourceId']['videoId'])
            if 'commentCount' not in stats.keys():
                stats['commentCount']=0
            if 'dislikeCount' not in stats.keys():
                stats['dislikeCount']=0
            if 'likeCount' not in stats.keys():
                stats['likeCount']=0
            if 'viewCount' not in stats.keys():
                stats['viewCount']=0


            only_vid.append((video['snippet']['resourceId']['videoId'], time.time()))

            alloutput.append((video['snippet']['resourceId']['videoId']+'/'+str(time.time()),video['snippet']['title'],video['snippet']['publishedAt'],video['snippet']['description'],video['snippet']['channelTitle'],stats['commentCount'],stats['dislikeCount'],stats['likeCount'],stats['viewCount'],time.time()))
            #crawled_dict[i + self.last_index] = tempdict

        return alloutput, only_vid


    def video_helper(self, videoIDlist):
        output =[]
        #print videoIDlist
        for vid in  videoIDlist:

            stats, snippet = self.update_video_stats(vid[0])
            if 'commentCount' not in stats.keys():
                stats['commentCount']=0
            if 'dislikeCount' not in stats.keys():
                stats['dislikeCount']=0
            if 'likeCount' not in stats.keys():
                stats['likeCount']=0
            if 'viewCount' not in stats.keys():
                stats['viewCount']=0
            output.append((vid[0]+'/'+ str(time.time()),snippet['publishedAt'],stats['commentCount'],stats['dislikeCount'],stats['likeCount'],stats['viewCount'],time.time()))

        return output

    def insert_table(self):

	try:

            allchannels_videos = []
            all_vid =[]
	    conn = None
	    # connect to the PostgreSQL database
	    conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
	    # create a new cursor
	    cur = conn.cursor()

            for channel in self.allchannelsdict:

                crawled_list, temp_only_vid = self.get_upload_playlist(channel,self.allchannelsdict[channel],1)
                allchannels_videos = allchannels_videos + crawled_list
                all_vid = all_vid + temp_only_vid
            print ('Got all videos')
	    sql_whole_data = """INSERT INTO youtube(id,title,publishedat,description,channeltitle,commentcount,dislikecount,likecount,viewcount,time)
		        	VALUES %s;"""
	    #sanity check
            for each in allchannels_videos:
                if len(each)<5:
                    allchannels_videos.remove(each)

            execute_values(cur,sql_whole_data,allchannels_videos)

	    sql_only_videoID = """INSERT INTO videoid3(id,time)
		        	VALUES %s;"""
	    #sanity check

            execute_values(cur,sql_only_videoID,all_vid)
	    conn.commit()
	    cur.close()
            print ('hooray')

	except (Exception, psycopg2.DatabaseError) as error:
	    print(error)

	finally:
	    if conn is not None:
		conn.close()


    def go_over_table(self):

	try:

	    conn = None
	    # connect to the PostgreSQL database
	    conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password )
	    # create a new cursor
	    cur = conn.cursor()
	    cur2 = conn.cursor()


            postgreSQL_select_Query = "select id from videoid3"

            cur.execute(postgreSQL_select_Query)

            while True:

                all_ids_so_far = cur.fetchmany(500)
                if not all_ids_so_far:
                    break
                allchannels_videos = self.video_helper(all_ids_so_far)


	        sql = """INSERT INTO youtube(id,title,commentcount,dislikecount,likecount,viewcount,time)
		        	VALUES %s;"""

                execute_values(cur2,sql,allchannels_videos)
                print ('last line')
	    conn.commit()
	    cur.close()
	    cur2.close()
            print ('hooray')

	except (Exception, psycopg2.DatabaseError) as error:
	    print(error)

	finally:
	    if conn is not None:
		conn.close()


    def remove_video_id(self):

        current_time = time.time()
        time_treshold = 20000

        try:

	    conn = None
	    # connect to the PostgreSQL database
	    conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
	# create a new cursor
	    cur = conn.cursor()

            postgreSQL_select_Query = "delete time from videoid"

            cur.execute(postgreSQL_select_Query)
            video_times = cur.fetchall()
            print video_times[:5]
	    cur.close()
            print ('hooray')

        except (Exception, psycopg2.DatabaseError) as error:
	    print(error)

        finally:
	    if conn is not None:
	        conn.close()

def Starter1():
    a= Datacollection()
    #a.insert_table()
    a.go_over_table()
    #a.remove_video_id()
    threading.Timer(60*60*6, Starter1).start()

def Starter2():
    b= Datacollection()
    #a.insert_table()
    b.insert_table()
    #a.remove_video_id()
    threading.Timer(60*60*8, Starter2).start()


b=Datacollection()
#a.insert_table()
b.insert_table()
Starter1()
Starter2()
