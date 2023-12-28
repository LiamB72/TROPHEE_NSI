import mysql.connector


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


selData("SELECT distinct Sport, count(Sport) FROM goldonlydb GROUP BY Sport HAVING count(Team);")
