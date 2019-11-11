import psycopg2
import config

def create_main_table():
	""" create tables in the PostgreSQL database"""
	commands = (
		"""
		CREATE TABLE youtube (
			id VARCHAR(500),
			title TEXT ,
			publishedAt VARCHAR(500) ,
			description TEXT ,
			channelTitle TEXT,
			commentcount BIGINT NOT NULL,
			dislikecount BIGINT NOT NULL,
			likecount BIGINT NOT NULL,
			viewcount BIGINT NOT NULL,
                        time BIGINT
		)
		""",
		""" CREATE TABLE dummy1 (
				part_id SERIAL PRIMARY KEY
				)
		"""
			)
	conn = None
	try:
	  
		# connect to the PostgreSQL server
		
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')


		cur = conn.cursor()
		# create table one by one
		
		for command in commands:
			print (command)
			cur.execute(command)

		print ('executed')
		# close communication with the PostgreSQL database server
		cur.close()
		# commit the changes
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.close()
			print ('Hooray')


def create_videoID_table():
	""" create tables in the PostgreSQL database"""
	commands = (
		"""
		CREATE TABLE videoID3 (
			id VARCHAR(500),
			time INT NOT NULL
		)
		""",
		""" CREATE TABLE dummy2 (
				part_id SERIAL PRIMARY KEY
				)
		"""
			)
	conn = None
	try:
	  
		# connect to the PostgreSQL server
		
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')


		cur = conn.cursor()
		# create table one by one
		
		for command in commands:
			print (command)
			cur.execute(command)

		print ('executed')
		# close communication with the PostgreSQL database server
		cur.close()
		# commit the changes
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.close()
			print ('Hooray')

def create_OldvideoID_table():
	""" create tables in the PostgreSQL database"""
	commands = (
		"""
		CREATE TABLE oldvideoID (
			id VARCHAR(500),
			time INT NOT NULL
		)
		""",
		""" CREATE TABLE dummy3 (
				part_id SERIAL PRIMARY KEY
				)
		"""
			)
	conn = None
	try:
	  
		# connect to the PostgreSQL server
		
		conn = psycopg2.connect("dbname="+config.dbname+" user="+config.user+" host="+config.host+" password="+config.password)
		print ('connected')


		cur = conn.cursor()
		# create table one by one
		
		for command in commands:
			print (command)
			cur.execute(command)

		print ('executed')
		# close communication with the PostgreSQL database server
		cur.close()
		# commit the changes
		conn.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

	finally:
		if conn is not None:
			conn.close()
			print ('Hooray')
if __name__ == '__main__':
	#create_main_table()
	create_videoID_table()
	#create_OldvideoID_table()
