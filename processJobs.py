from pymongo import MongoClient
import pandas as pd
import re

client = MongoClient('localhost', 27017) 
db = client.australia_jobs

kws = db.Keywords.find({})
keywords = []
dictKw = {}
### get keywords from database
# for kw in kws:
#     keywords.append(kw["Keyword"])
#     dictKw[kw["Keyword"]] = 0

### get keywords from file
with open('../data/k_plurals.txt','r',encoding='utf-8') as f:
    s = f.readlines()
    # print(len(s))
    s = list(map(lambda  x: x.replace(" \n","\n"),s))
    s = list(map(lambda  x: x.replace("\n",""),s))
    for k in s:
        keywords.append(k)
        dictKw[k] = 0


### end kw

fDs = db.Jobs.find({})
def cleanHTML(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = re.sub(' +', ' ', cleantext)
    cleantext  = cleantext.replace('&nbsp','')
    cleantext = re.sub("[^a-zA-Z]+", " ",cleantext)
    # cleantext = cleantext.split(' ')
    return ' ' + cleantext.lower() + ' '

# exit()
# t = cleanHTML(fDs[0]["FullDescription"])
# print(t.find(' ' + 'these'+ ' '))
# exit()
c = 0
for des in fDs:
    c += 1
    try:
        d = des["FullDescription"]
        d = cleanHTML(d)
        for k in keywords:
            if k.find('and') != -1 :
                print(k)
                inDoc = False
                kl = k.lower()
                kl = kl.split(' ')
                del kl[1]
                t1 = ' ' + kl[0] + ' '  #' food '
                t2 = ' ' + kl[1] + ' ' + kl[2] + ' ' #' beverage manager '
                t3 = ' ' + kl[0] + ' ' + kl[2] + ' ' #' food manager '
                t4 = ' ' + kl[1] + ' ' + kl[2] + ' ' #' beverage manager '
                t5 = ' ' + kl[1] + ' ' #' beverage '
                t6 = ' ' + kl[2] + ' ' #' manager '
                if (d.find(t1) * d.find(t2) > 0) and (d.find(t1) < d.find(t2)):
                    inDoc = True
                elif (d.find(t3) * d.find(t4) > 0) and (d.find(t3) < d.find(t4)):
                    inDoc = True
                elif (d.find(t1) * d.find(t5) * d.find(t6) > 0) and (((d.find(t3) < d.find(t5) and d.find(t5) < d.find(t6)) or (d.find(t5) < d.find(t3) and d.find(t3) < d.find(t6)))):
                    inDoc = True
                if inDoc:
                    freq = dictKw[k]
                    freq = freq + 1
                    dictKw[k] = freq
            else:
                kspace = ' ' + k.lower() + ' '
                if d.find(kspace) != -1:
                # if k in d:
                    freq = dictKw[k]
                    freq += 1
                    dictKw[k] = freq
    except:
        print(c)

# print(len(fullD))
# with open('result_kw.txt','w',encoding='utf-8') as f:
    # for k,v in dictKw.items():
        # f.write(k)
K = []
V = []
for k,v in dictKw.items():
    K.append(k)
    V.append(v)
    print('K: %s - V: %d ' %(k,v))

d = {"Keyword":K,"Value":V}
df = pd.DataFrame(d)
df.to_csv('../data/result_kw_plurals_1.csv',index=False,encoding='utf-8')