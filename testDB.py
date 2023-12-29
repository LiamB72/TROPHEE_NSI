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
        print(f"{columnTitle[0]:35}", end="")
    print("\n")

    for rows in valuesList:
        for val in rows:
            print(f"{val:35}", end='')
        print()

    requestExecutor.close()
    db.close()


selData('''
SELECT Sport, Team, Games, MAX(MedalCount) as MaxMedals
    FROM (
        SELECT Sport, Team, Games, COUNT(*) as MedalCount
        FROM goldonlydb
        GROUP BY Sport, Team
    )
    GROUP BY Sport
    ORDER BY Games DESC;
''')
