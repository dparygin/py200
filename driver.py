import json, csv
import os, sqlite3

class IStructureDriver:
    db_name = I
    def write(self, d, _):
        pass


class to_csv(IStructureDriver):
    def __init__(self, filename):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM books")
            with open(filename, 'x', newline='') as file:
                print(file)
                writer = csv.writer(file, delimiter=';')
                writer.writerow([i[0] for i in cursor.description])
                for result in cursor:
                    writer.writerow(result)
            conn.close()
            print('CSV-файл успешно сохранен')
        except FileExistsError:
            print('Файл с таким названием уже существует\n')

class to_json(IStructureDriver):
    def __init__(self, filename):
        self.filename = filename
        if len(self.filename) == 0:
            filename = 'output.json'
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM books")
            result = cursor.fetchall()
            with open(filename, 'x', newline='') as file:
                json.dump(result, file)
            conn.close()
            print('JSON-файл успешно сохранен')
        except FileExistsError:
            print('Файл с таким названием уже существует\n')
