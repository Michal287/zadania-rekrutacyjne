from sqlite3 import connect
from requests import request
import json
import csv
from task2 import product_save


def get_token():
    f = open('credentials.json')
    data = json.load(f)
    return "Bearer " + data['token']


def get_request(request_data, token):
    try:
        DOMAIN = "https://recruitment.developers.emako.pl"

        HTTP_HEADERS = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token
        }

        return request("GET", f"{DOMAIN}/products", headers=HTTP_HEADERS, data=request_data).json()

    except:
        print('Cannot get data from server')


def read_ids(filename):
    try:
        file = open(filename)

        csvreader = csv.reader(file)

        ids = [i[0] for i in csvreader]

        return json.dumps({"ids": ids})

    except:
        print('Cannot import ids from file')


class Task1:
    def __init__(self, ids=None, filename=None):
        if ids is not None:
            self.ids = ids
        elif filename is not None:
            self.ids = read_ids(filename)
        else:
            raise ValueError('ids is not set')

        self.token = get_token()

    def get_products(self):
        try:
            db = connect("database.sqlite")
            products = get_request(self.ids, self.token)

            for product in products['result']:
                product_save(db, product)

            db.close()

            return 'Status: 200'

        except:
            return f'Status: 500'


if __name__ == '__main__':
    task = Task1(filename='ids.csv')
    print(task.get_products())



