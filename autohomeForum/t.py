import csv, pymongo, pymysql, json

# mysql相关
MYSQL_HOST = '172.20.206.28'
MYSQL_DBNAME = 'autohomespider'
MYSQL_USER = 'nanwei'
MYSQL_PASSWD = 'nanwei'
MYSQL_PORT = 3306

# MongoDB configuration
MONGODB_HOST = '172.20.206.28'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'koubei'
MONGODB_DOCNAME = 'autohome'


def getSecifids(modelId):
    specificIds = list()
    db = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                         password=MYSQL_PASSWD, db=MYSQL_DBNAME,
                         port=MYSQL_PORT)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM specificids where modelId= %s', (modelId,))
    rows = cursor.fetchall()
    for row in rows:
        for item in json.loads(row[2]):
            specificIds.append(item['SpecId'])
    cursor.close()
    db.close()
    return specificIds


def getContents(modelName, specificId):
    client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
    tdb = client[MONGODB_DBNAME]
    post = tdb[MONGODB_DOCNAME]
    datas = post.find({'specId': str(specificId)})
    dataSave = list()
    for data in datas:
        try:
            dataSave.append([modelName, data['contents']['contentsText'].replace('\n', '')])
        except Exception as e:
            print(e)
    datas.close()
    client.close()
    save(dataSave)


def save(datas):
    with open('1.csv', 'wa', newline='') as writer:
        writer = csv.writer(writer, delimiter='\t')
        writer.writerows(datas)


if __name__ == '__main__':
    specificIds = getSecifids(3862)
    for specificId in specificIds:
        getContents('奔驰GLC', specificId)
