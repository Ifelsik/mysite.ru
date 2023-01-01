import sqlite3
import os

DATABASE_PATH = f"{os.getcwd()}/data/mysite.db"

db = sqlite3.connect(DATABASE_PATH)
cur = db.cursor()

photos = cur.execute("SELECT image FROM books;")

for photo in photos:
    print(type(photo))
    with open("2.jpg", "wb") as file:
        file.write(photo[0])

db.commit()
cur.close()
db.close()
print("OK")
