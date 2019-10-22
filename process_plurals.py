
keywords = []

with open('../data/keywords.txt','r',encoding='utf-8') as f:
    s = f.readlines()
    # print(len(s))
    s = list(map(lambda  x: x.replace(" \n","\n"),s))
    s = list(map(lambda  x: x.replace("\n",""),s))
    for kw in s:
        kw = kw.split(' ')
        for w in kw:
            if (w[len(w)-1] != 'y') or (w[len(w)-1] != 's')
        # print(k)
        db.Keywords.insert_one({"Keyword":k})