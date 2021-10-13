from celery import Celery
from tasks import get_faculty
import os
import time
import mysql.connector

def connect_to_mysql():
    mydb = mysql.connector.connect(
        host="localhost",
        user="juefeic2",
        password="0202141208",
        database="juefeic2_educationtoday"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

mydb, mycursor = connect_to_mysql()
while True:
    n = os.popen('../../Celery_Test/redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery').read()
    if int(n) >= 2:
        time.sleep(1)
        continue
    mycursor.execute('select University_ID, Department_Name from Faculty_Tasks where Priority > -2147483648 order by Priority asc, University_ID asc, Department_Name asc;')
    r = mycursor.fetchall()
    for i in range(6):
        mycursor.execute('select University_Name from University where University_ID = {}'.format(r[i][0]))
        university = mycursor.fetchone()[0]
        print(university, r[i][1])
        mycursor.execute('update Faculty_Tasks set Priority = -2147483648 where University_ID = {} and Department_Name = "{}"'.format(r[i][0], r[i][1]))
        get_faculty.delay(university, r[i][1])

    mydb.commit()
    time.sleep(1)
