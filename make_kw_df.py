import pandas as pd

keywords = []

with open('../data/keywords.txt','r',encoding='utf-8') as f:
    s = f.readlines()
    s = list(map(lambda  x: x.replace(" \n","\n"),s))
    s = list(map(lambda  x: x.replace("\n",""),s))
    for k in s:
        keywords.append(k)

d = {'Keyword':keywords}
df = pd.DataFrame(d)
df.to_csv('../data/keyword_df.csv',index=False,encoding='utf-8')