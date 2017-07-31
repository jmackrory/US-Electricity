# Goal is to convert ELEC.txt into a SQL database for easier querying.
# (Whole JSON file does not fit into memory).
# Used "split" to slit ELEC.txt into chunks with 10000 lines each.
# Each of those will be read in as a pandas dataframe.
# Will then check if each column in the dataframe exists in the SQL table.
# If not, use psycopg to create that column.
# Note

#Read in JSON Data.
#Read in Electric System Bulk Operating Data
#Export whole data frame to SQL database.   
import pandas as pd
import numpy as np
import sqlalchemy as sa
import json,os
import psycopg2
from psycopg2 import sql

# #Borrowed from Introducing Python pg 180.
database_name='US-ELEC'
engine=sqlalchemy.create_engine("postgresql+psycopg2://localhost/"+fname)

# #make a new table.  

#Make new database by logging into 
def create_new_database(database_name)
	conn=psycopg2.connect(dbname='jonathan',host='localhost')
	#need elevated permissions in order to create a new database from within python, to automatically
	#commit changes.
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  #automatically commit changes
	cur = conn.cursor()
	table_name="testdata"
	#create table
	t1 = sql.Identifier(database_name)
	q0 = sql.SQL("CREATE DATABASE {0}").format(t1)

	try:
		cur.execute(q0)
	except:
		print('Creating database: '+database_name+' failed.')

	cur.close()
	conn.close()
	return None


def create_fresh_table(database_name, table_name,df):
	conn=psycopg2.connect(dbname=database_name,host='localhost')
	conn.set_session(autocommit=True)
	cur = conn.cursor()
	t1 = sql.Identifier(table_name)

	#Drop Table to start from scratch.
	try:
		q_drop = sql.SQL("DROP TABLE {0}").format(t1)
		cur.execute(q_drop)
		conn.commit()
		print('DROPPED '+table_name)
	except:
		print('Could not DROP '+table_name)

	#Create Blank table with first column given by first column of data.
	try:
		c1 = sql.Identifier(df.columns[0])
		q_create = sql.SQL("CREATE TABLE {0} ({1} TEXT)").format(t1,c1)
		cur.execute(q_create)
		conn.commit()
		print('CREATED '+table_name)
	except:
		print('Could not CREATE TABLE '+table_name)

	return conn,cur

#Make sure required columns are present.
def check_and_create_columns(table_name,cur,df):

	for column_name in df.columns:
		t1 = sql.Identifier(table_name)
		c1 = sql.Identifier(column_name)
		try:
			#just check if there is a column with the right name.
			#allow no records since might have to start with empty table.
			q2 = sql.SQL("SELECT {1} FROM {0} LIMIT 0").format(t1,c1)
			cur.execute(q2)
			print('Success in retrieving column: '+column_name)
		except:
			print('Trying to read from column: '+column_name+' failed.')
			print('Trying to Add column: '+column_name)
			#if not then create that column.  
			q3 = sql.SQL("ALTER TABLE {0} ADD COLUMN {1} TEXT").format(t1,c1)
			cur.execute(q3)
	return None

conn,cur=create_fresh_table(database_name,

nfile=2;
for i in range(0,nfile):
	fname_split='data/split_dat/'+fname+str("%02d"%(i));
	print(fname_split)
	df=pd.read_json(fname_split,lines=True);
	#use str() to protect with quotes, to just store the whole string in SQL, (which otherwise
	#gets confused by brackets and commas in data and childseries).
	df['data']=df['data'].astype('str')
	if 'childseries' in df.columns:	
		print('childseries in columns')
		df['childseries']=df['childseries'].astype('str')
		
	for column_name in df.columns():
		t1 = sql.Identifier(table_name)
		c1 = sql.Identifier(column_name)
		try:
			#check if column is there
			q2 = sql.SQL("SELECT {1} FROM {0} LIMIT 0").format(t1,c1)
			cur.execute(q2)
		except:
			print('Column '+column_name+' not found.  Adding to Database.')
			q2 = sql.SQL("ALTER TABLE {0} ADD COLUMN {1} TEXT").format(t1,c1)
			cur.execute(q2)

	
	df.to_sql(fname,engine,index=False,if_exists='append');
