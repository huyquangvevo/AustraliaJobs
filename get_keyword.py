from pymongo import MongoClient

client = MongoClient('localhost', 27017) 
db = client.australia_jobs

with open('../data/keywords.txt','r',encoding='utf-8') as f:
    s = f.readlines()
    # print(len(s))
    s = list(map(lambda  x: x.replace(" \n","\n"),s))
    s = list(map(lambda  x: x.replace("\n",""),s))
    for k in s:
        # print(k)
        db.Keywords.insert_one({"Keyword":k})
    # print(s[0])
    # print(s[1])
    # print(s[len(s)-1])


    
