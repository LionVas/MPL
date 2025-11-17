import csv
import math
import random
from concurrent.futures.thread import ThreadPoolExecutor
class Tool:
    CHAR_LIST = ('А', 'Б', 'В', 'Г', 'Д')

    @staticmethod
    def generate():
        for i in range(1, 6):
            filename = "generated" + str(i) + ".csv"
            with open(filename, "w", newline="", encoding="UTF-8") as file:
                writer = csv.writer(file);
                for j in range(0, 100):
                    x = Tool.CHAR_LIST[random.randint(0, 4)]
                    y = random.random()
                    writer.writerow([x, y])

    @staticmethod
    def med(x):
        x.sort()
        if len(x) % 2 == 0:
            return x[int(len(x) / 2)]
        else:
            return x[int(len(x) / 2) - 1]

    @staticmethod
    def standart_dev(x):
        mid = 0
        for i in x:
            mid += i
        mid /= len(x)
        dev = 0
        for i in x:
            dev += (i - mid) ** 2
        return math.sqrt(dev / len(x))

    @staticmethod
    def worker(i):
        mapa = {
            "А": [],
            "Б": [],
            "В": [],
            "Г": [],
            "Д": []
        }
        filename = "generated" + str(i) + ".csv"
        with open(filename, "r", newline="", encoding="UTF-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if (len(row) != 2):
                    continue
                k = row[0].strip()
                if k in mapa:
                    mapa[k].append(float(row[1].strip()))
                else:
                    print("Ключ не в мапе", k)
        result_filename = "result" + str(i) + ".csv"
        with open(result_filename, "w", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file);
            for k, v in mapa.items():
                writer.writerow([k, Tool.med(v), Tool.standart_dev(v)])
        for k, v in mapa.items():
            v = [[Tool.med(v)], [Tool.standart_dev(v)]]
        return mapa

    @staticmethod
    def add_map(map1, map2):
        for k, v in map2.items():
            map1[k][0].append(v[0])
            map1[k][1].append(v[1])
        return map1

    @staticmethod
    def find_median():
        indexes = (1, 2, 3, 4, 5)
        mapa = {
            "А": [[], []],
            "Б": [[], []],
            "В": [[], []],
            "Г": [[], []],
            "Д": [[], []]
        }
        with ThreadPoolExecutor(max_workers=5) as executor:
            maps = list(executor.map(Tool.worker, indexes))
        for m in maps:
            mapa = Tool.add_map(mapa, m)
        with open("final.csv", "w", newline="", encoding="UTF-8") as file:
            writer = csv.writer(file);
            for k, v in mapa.items():
                a = mapa[k][0]
                b = mapa[k][1]
                writer.writerow([k, Tool.med(a), Tool.standart_dev(b)])
