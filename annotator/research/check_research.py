import mysql.connector
import string
import pathlib

abs_path = str(pathlib.Path(__file__).parent.absolute()) + '/'

def connect_to_mysql():
    mydb = mysql.connector.connect(
        host="owl2.cs.illinois.edu",
        user="juefeic2",
        password="0202141208",
        database="juefeic2_educationtoday"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

mydb, mycursor = connect_to_mysql()
# mycursor.execute('SELECT Research FROM Faculty where Task_ID like "%Computer%";')
mycursor.execute('SELECT distinct(Department_Name) FROM Department;')
r = mycursor.fetchall()
department = set()
for i in r:
    t = i[0].translate(str.maketrans('', '', string.punctuation))
    for j in t.split():
        department.add(j.lower())
print(len(department))

f = open(abs_path + 'act_majors.txt')
act_majors = set()
for i in f.readlines():
    t = i[:-1].replace('/', ' ').translate(str.maketrans('', '', string.punctuation)).lower().split()
    act_majors = act_majors.union(set(t))
print(act_majors)
print(len(act_majors))