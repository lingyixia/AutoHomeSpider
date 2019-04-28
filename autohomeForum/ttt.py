import csv, pymongo, pymysql, json

# MongoDB configuration
MONGODB_HOST = '172.20.206.28'
# MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'forum'
MONGODB_DOCNAME = 'autohome'


def getContents(modelName):
    client = pymongo.MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
    tdb = client[MONGODB_DBNAME]
    post = tdb[MONGODB_DOCNAME]
    datas = post.find({'carId': '4871'})
    dataSave = list()
    for data in datas:
        try:
            dataSave.append([modelName, data['contents'][0][0]])
            d = data['contents']
            for i in range(1, len(d)):
                if i==0:
                    dataSave.append([modelName, d[i][0]])
                else:
                    dataSave.append([modelName, d[i][1]])
        except Exception as e:
            print(e)
    datas.close()
    client.close()
    save(dataSave)


def save(datas):
    with open('1.csv', 'w', newline='',errors='ignore') as writer:
        writer = csv.writer(writer, delimiter='\t')
        writer.writerows(datas)


if __name__ == '__main__':
    getContents('一汽-大众奥迪-奥迪Q2L')
