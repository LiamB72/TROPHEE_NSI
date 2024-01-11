import sqlite3


def connectBD():
    db = sqlite3.connect(database='./data/database/olympicsDB.db')
    return db


def selData(request):
    print(request, "\n")
    db = connectBD()
    requestExecutor = db.cursor()
    requestExecutor.execute(request)
    valuesList = requestExecutor.fetchall()

    for columnTitle in requestExecutor.description:
        print(f"{columnTitle[0]:40}", end="")
    print("\n")

    for rows in valuesList:
        for val in rows:
            print(f"{val:40}", end='')
        print()

    requestExecutor.close()
    db.close()


selData('''
SELECT Games
FROM olympicsdb
WHERE Games > "1990%"
AND Games < "2004%"
AND Sport="Athletics"
ORDER BY Games DESC;
''')
