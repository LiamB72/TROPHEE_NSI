# https://www.w3schools.com/python/python_mysql_getstarted.asp
import mysql.connector
from mysql.connector import FieldType


def connectBD():
    db = mysql.connector.connect(user='root', password='',
                                 host='127.0.0.1',
                                 database='olympicsDB')
    return db


def selData(request):
    print(request, "\n")
    db = connectBD()
    requestExecutor = db.cursor()
    requestExecutor.execute(request)
    valuesList = requestExecutor.fetchall()

    for columnTitle in requestExecutor.description:
        print(f"{columnTitle[0]:60}", end="")
    print("\n")

    for rows in valuesList:
        for val in rows:
            print(f"{val:60}", end='')
        print()

    requestExecutor.close()
    db.close()


selData("SELECT Name, NOC, Sport FROM goldonlydb WHERE Games='1972 Summer' ORDER BY Sport;")
