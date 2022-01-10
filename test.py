from sqlite3 import connect

sql = connect("database.sqlite")

sql_querry = ("SELECT * FROM product_stocks")


cursor = sql.cursor()
result = cursor.execute(sql_querry)

for idx, row in enumerate(result):
    print(f"{idx}: {row}")
