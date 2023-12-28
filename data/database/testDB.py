import sqlite3


def connectBD():
    db = sqlite3.connect(database='olympicsDB.db')
    return db


def selData(request):
    text = ""
    nb = ""
    print(request, "\n")
    cValue = ""
    db = connectBD()
    cursor = db.cursor()
    cursor.execute(request)

    '''for columnTitle in cursor.description:
        print(f"{columnTitle[0]:60}", end="")
    print("\n")'''

    for row in cursor:
        text += f"{str(row[0])};"
        nb += f"{str(row[1])} "

    cursor.close()
    db.close()

    return text, nb


rawData = selData('''
SELECT distinct Sport, count(Team) 
FROM goldonlydb 
GROUP BY Sport HAVING COUNT(Team)
ORDER BY COUNT(Team) DESC
LIMIT 10;
''')

rawCategories = str(rawData[0])
categories = ""

for i in range(len(rawCategories)):
    if rawCategories[i] != ';' and rawCategories[i] != " ":
        categories += rawCategories[i]
    elif rawCategories[i] == ';':
        categories += " "
    if rawCategories[i] == " ":
        categories += ""

categories = categories.split()

print(categories)
