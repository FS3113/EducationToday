# celery -A tasks worker --pool=solo --loglevel=info
# celery -A tasks worker --pool=prefork --concurrency=1 --loglevel=info
# src/redis-server --protected-mode no

# redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery

from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import time
from algorithm import find
import json
import mysql.connector

def connect_to_mysql():
    mydb = mysql.connector.connect(
        host="owl2.cs.illinois.edu",
        user="juefeic2",
        password="0202141208",
        database="juefeic2_educationtoday"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

# Redis broker URL
# BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = 'redis://juefeic2@172.22.224.119:6379/0'

celery_app = Celery('Restaurant', broker=BROKER_URL)

@celery_app.task(soft_time_limit=300)
def get_faculty(university, department):
    mydb, mycursor = connect_to_mysql()
    try:
        data, url = find(university, department)
        print(data, url)
        mycursor.execute('select University_ID from University where University_Name = "{}"'.format(university))
        university_id = int(mycursor.fetchone()[0])
        mycursor.execute('update Faculty_Tasks set Priority = 2147483647 where University_ID = {} and Department_Name = "{}"'.format(university_id, department))
        mydb.commit()
        # with open('cs_data/' + university, 'w') as outfile:
        #     json.dump(data, outfile, indent=4)
    except SoftTimeLimitExceeded:
        print('time limit...')
        # with open('cs_data/' + university, 'w') as outfile:
        #     json.dump(['time limit exceded'])
    finally:
        mycursor.close()
        mydb.close()
    