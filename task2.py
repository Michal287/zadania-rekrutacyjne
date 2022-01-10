import datetime
from json import *
from sqlite3 import connect, Error
from requests import request, exceptions


def json_export(product):
    try:
        file = open("tmp.txt", "w")
        dump(product, file)
        file.close()

    except:
        print('Cannot export json to file.')


def product_request(id):
    try:
        response = request(
            "GET", "https://recruitment.developers.emako.pl/products/example?id=" + str(id)
        )

        print(f"data downloaded from server {len(response.content)}")
        product = response.json()
        json_export(product)

        return product

    except exceptions.HTTPError as e:
        print(e)

    except:
        print('Unknown request error.')


def product_stocks_push(db, values):
    try:
        sql_querry = ("INSERT INTO product_stocks " \
                      "(time, product_id, variant_id, stock_id, supply) " \
                      "VALUES (?, ?, ?, ?, ?)")

        cursor = db.cursor()
        cursor.execute(sql_querry, values)
        db.commit()

    except:
        print('Sql querry error.')


def product_save(db, product):
    try:

        if product["type"] != "bundle":
            print("product loaded")

            for supply in product["details"]["supply"]:
                for stock in supply["stock_data"]:
                    values = (str(datetime.datetime.now())[:19],
                              product["id"],
                              supply["variant_id"],
                              stock["stock_id"],
                              stock["quantity"]
                              )

                    product_stocks_push(db, values)

        else:
            print("bundle loaded")

            products_ids = []
            for product in product["bundle_items"]:
                products_ids.append(product["id"])

            print("products " + str(len(products_ids)))

            for product_id in products_ids:
                product = product_request(product_id)
                stock_sum = {}

                for s in product["details"]["supply"]:
                    for stock in s["stock_data"]:
                        key = stock["stock_id"]

                        if key in stock_sum:
                            stock_sum[key] += stock["quantity"]
                        else:
                            stock_sum[key] = stock["quantity"]

                for key, value in stock_sum.items():
                    values = (str(datetime.datetime.now())[:19],
                              product["id"],
                              "NULL",
                              key,
                              value
                              )

                    product_stocks_push(db, values)

    except:
        print('Logical error')


def create_product(db_name, products_ids):
    try:
        db = connect(db_name)

        for target in products_ids:
            try:

                product = product_request(target)
                product_save(db, product)

            except Exception as e:
                return f'Error: {e}'

        db.close()

    except Error as e:
        return f'Database error: {e}'

    return "Status: Ok"


if __name__ == '__main__':
    status = create_product("database.sqlite", [-2, -3])
    print(status)

