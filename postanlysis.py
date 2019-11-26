'''
Q1- What are the word frequencies overall?
concatenate all titles to create a single member list
'''
import psycopg2
import config 
import tfidf
import json

with open('channels.json') as json_file:
	allchannelsdict = json.load(json_file)


def all_titles_tfidf():

	try:
		print ('started')
		conn = None
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password )
		cur = conn.cursor()
		print ('connected')


        	postgreSQL_select_Query = "select title from youtube"

        	cur.execute(postgreSQL_select_Query)

        	all_titles = cur.fetchall()
             
		print (all_titles[0][0]) 
	    	conn.commit()
	    	cur.close()
	   
        	print ('hooray')

	except (Exception, psycopg2.DatabaseError) as error:
	    	print(error)

	finally:
	   	if conn is not None:
			conn.close()

	concat=" "
	for title in all_titles:
		concat+= title[0]

	print (len(concat))
	df = tfidf.tfidfsk([concat])
	print (df)

def channel_titles_tfidf():

	try:
		print ('started')
		conn = None
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password )
		cur = conn.cursor()
		print ('connected')
		all_channels=[]
		for channel in allchannelsdict.keys():

        		postgreSQL_select_Query = "select title from youtube where youtube.channeltitle="+"'"+channel+"'"
			print (channel)
        		output = cur.execute(postgreSQL_select_Query)
        		all_titles = cur.fetchall()
             		print ('got')
			print (all_titles[0][0])
			temp =""
			for each in all_titles:
 				temp += ' '+each[0]

			all_channels.append(temp)
	    	conn.commit()
	    	cur.close()
	   
        	print ('hooray')

	except (Exception, psycopg2.DatabaseError) as error:
		print ('got an error')
	    	print(error)

	finally:
	   	if conn is not None:
			print ('done')
			conn.close()

	

	#print (len(concat))
	df = tfidf.tfidfsk(all_channels)
	print (df)

def get_video_stats():

	try:
		print ('started')
		conn = None
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password )
		cur = conn.cursor()
		print ('connected')

        	postgreSQL_select_Query = "select onlyid from unionid"
        	cur.execute(postgreSQL_select_Query)
        	all_id = cur.fetchall()

		
	 	select_query= ("SELECT commentcount, dislikecount, likecount, viewcount, time, onlyid FROM public.youtube WHERE onlyid=%s ORDER BY time ASC;")

		for eachid in all_id:

			cur.execute(select_query,eachid)
			records = cur.fetchall()
			temp = records[-1]

			update_query=( "UPDATE unionid SET avecomment=%s,avedislike=%s,avelike=%s,aveview=%s WHERE onlyid=%s;")


			cur.execute(update_query,(temp[0],temp[1],temp[2],temp[3],temp[5]))
		#all_id[0][0]
		print (len(all_id))
	    	conn.commit()
	    	cur.close()
	   
        	print ('hooray')

	except (Exception, psycopg2.DatabaseError) as error:
		print ('got an error')
	    	print(error)

	finally:
	   	if conn is not None:
			print ('done')
			conn.close()
'''
SELECT title, commentcount, dislikecount, likecount, viewcount, "time", onlyid
	FROM public.youtube
	WHERE onlyid='bYQSgEyvyiM'
	ORDER BY
	time ASC;

'''

	
def get_channel_stats():

	try:
		print ('started')
		conn = None
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password )
		cur = conn.cursor()
		print ('connected')

        	select_Query = "select AVG(avecomment), stddev(avecomment), AVG(avedislike), stddev(avedislike), AVG(avelike), stddev(avelike),AVG(aveview), stddev(aveview)from unionid where channeltitle=%s"





		channel = ["CNN"]
        	cur.execute(select_Query,channel)
        	channel_stats = cur.fetchall()
		
		print len(channel_stats)

		update_query=( "UPDATE averesults SET channeltitle=%s,avecomment=%s, stdcomment=%s,avedislike=%s ,stddislike=%s,avelike=%s,stdlike=%s, aveview=%s,stdview=%s ;")

		values = ['CNN',channel_stats[0][0], channel_stats[0][1], channel_stats[0][2], channel_stats[0][3], channel_stats[0][4], channel_stats[0][5], channel_stats[0][6], channel_stats[0][7]] 
        	print len(values)
		cur.execute(update_query,values)

	    	conn.commit()
	    	cur.close()
	   
        	print ('hooray')

	except (Exception, psycopg2.DatabaseError) as error:
		print ('got an error')
	    	print(error)

	finally:
	   	if conn is not None:
			print ('done')
			conn.close()

'''
Q2- What are the word frequencies in 
'''
def main():

	#channel_titles_tfidf()
	get_channel_stats()
if __name__=="__main__":

	main()
