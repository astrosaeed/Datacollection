from apiclient.discovery import build
import sys
import json
import datetime
import config

# arguments to be passed to build function
DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)


def get_upload_playlist(channelname, uploadID,num_page, last_index):
    
    crawled_dict={}
    items =[]
    token =None
    counter =0
    while counter <num_page:
        counter+=1
        playlist_response = youtube.playlistItems().list(playlistId=uploadID,
                                            part = "snippet",pageToken=token).execute()
        items.append(playlist_response)

        try:
            token = playlist_response['nextPageToken']
        except:
            print 'no next token'
            break

    for i,video in enumerate (items[0]['items']):
        tempdict={}
        tempdict['id'] = video['id']
        tempdict['title'] = video['snippet']['title']
        tempdict['publishedAt'] = video['snippet']['publishedAt']
        tempdict['description'] = video['snippet']['description']
        tempdict['channelTitle'] = video['snippet']['channelTitle']



        #print video['id']
        #print video['snippet']['title']
        #print video['snippet']['publishedAt']
        #print video['snippet']['description']
       # print video['snippet']['channelTitle']

        crawled_dict[i + last_index] = tempdict
    return crawled_dict
   # save_json(items,channelname)
        


def get_ratings():


    request = youtube.videos().rate(rating='like',id="L-WSksUKWDA")
    response = request.execute()

    print(response)


def get_comments(ID, token = None):

    items =[]
    while token!='last_page':
        request = youtube.commentThreads().list(
            part="snippet",
            videoId= ID,
            pageToken=token
        )
        response = request.execute()
        #print response['nextPageToken']
        try:
            items.append(response)
            print response['nextPageToken']
            token = response['nextPageToken']
        except:
            print 'DONE'
            break


    save_json(items,'comments_ID:'+ID)
    #print(response)



def save_json(data, filename):


    with open(filename+'_'+str(datetime.datetime.now()).split('.')[0]+'.json', 'w') as json_file:
        #json.dump(data, filename+str(datetime.datetime.now()).split('.')[0])
        json.dump(data, json_file)


if __name__ == "__main__":

    with open('channels_upload_id.json') as json_file:
        allchannelsdict = json.load(json_file)


    for channel in allchannelsdict:


        print get_upload_playlist(channel,allchannelsdict[channel],1,0)


    #result = get_upload_playlist('CNN')
    #print("items:", result['items'])
    #get_ratings()
    #get_comments("L-WSksUKWDA")
