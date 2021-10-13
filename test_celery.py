from tasks import get_faculty
from celery import Celery
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
mycursor.execute('SELECT University_Name FROM University;')
r = mycursor.fetchall()
university = []
for i in r:
    university.append(i[0])
university = university[::-1]
mycursor.close()
mydb.close()


for i in range(50):
    u = university.pop()
    result = get_faculty.delay(u, 'computer science')
    print(result)

n = os.popen('../../Celery_Test/redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery').read()
print(n)

while university:
    n = os.popen('../../Celery_Test/redis/redis-stable/src/redis-cli -h localhost -p 6379 -n 0 llen celery').read()
    if int(n) < 50:
        i = 0
        while i < 50 and university:
            u = university.pop()
            result = get_faculty.delay(u, 'computer science')
            i += 1
            print(result)
    time.sleep(8)

