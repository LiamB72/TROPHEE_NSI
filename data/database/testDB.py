import sqlite3


def connectBD():
    db = sqlite3.connect(database='goldonlydb.sql')
    return db


def selData(request):
    print(request, "\n")
    cValue = ""
    db = connectBD()
    cursor = db.cursor()
    cursor.execute(request)

    '''for columnTitle in cursor.description:
        print(f"{columnTitle[0]:60}", end="")
    print("\n")'''

    for row in cursor:
        text = str(row[0]) + str(row[1]) + "\n"

    cursor.close()
    db.close()


selData("SELECT distinct Sport, count(Sport) FROM goldonlydb GROUP BY Sport HAVING count(Team);")
