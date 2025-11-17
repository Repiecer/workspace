import pymysql
db = pymysql.connect(host='localhost',user='root',passwd='123456',port=3306)
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
cursor.execute("CREATE DATABASE spider DEFAULT CHARACTER SET utf8")
print("Database version : %s " % data)
cursor.close()
db.close()