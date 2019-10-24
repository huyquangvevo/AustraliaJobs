from pymongo import MongoClient
import pandas as pd
import re
from nltk.stem.wordnet import WordNetLemmatizer
from bson.json_util import dumps, loads


client = MongoClient('localhost', 27017) 
db = client.australia_jobs

wordNet = WordNetLemmatizer()
fullJob = None

def cleanHTML(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = re.sub(' +', ' ', cleantext)
    cleantext  = cleantext.replace('&nbsp','')
    cleantext = re.sub("[^a-zA-Z]+", " ",cleantext)
    return ' ' + cleantext.lower() + ' '

def lemmatize(doc):
    doc = doc.split(' ')
    doc = list(map(lambda  x: wordNet.lemmatize(x,pos='n'),doc))
    doc = ' '.join(doc)
    return ' ' + doc + ' '


def filterByKeyword(k):
    count = 0
    errorId = 0
    jobK = []
    for job in fullJob:
        errorId += 1
        try:
            d = job["FullDescription"]
            d = cleanHTML(d)
            d = lemmatize(d)
            hasKeyword = False
            if k.find('and') != -1 :
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
                    hasKeyword = True
            else:
                kspace = ' ' + k.lower() + ' '
                if d.find(kspace) != -1:
                    hasKeyword = True
            if hasKeyword:
                jb = job
                jb["FullDescription"] = d
                jobK.append(loads(dumps(jb)))
                count += 1
        except Exception as e:
            # print(str(e))
            print(errorId)
    print('Total job for keyword %s : %d ' % (k,count))
    return jobK

if __name__ == '__main__':
    fullJob = db.Jobs.find({},{'_id':0,'Date':0,'DetailDate':0})
    client.close()
    kw = "Market"
    jobs = filterByKeyword(kw)
    df = pd.DataFrame(jobs)
    df.to_csv('../data/job_kw_' + kw + '.csv',index=False,encoding='utf-8')


