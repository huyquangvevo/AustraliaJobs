import pandas as pd

keywords = []
label = []
root = []

with open('../data/keywords.txt','r',encoding='utf-8') as f:
    s = f.readlines()
    # print(len(s))
    s = list(map(lambda  x: x.replace(" \n","\n"),s))
    s = list(map(lambda  x: x.replace("\n",""),s))
    for i,kw in enumerate(s):
        keywords.append(kw)
        label.append(i)
        root.append(1)
        kw = kw.split(' ')
        for id,w in enumerate(kw):
            w_old = w
            if (w[len(w)-1] != 'y') and (w[len(w)-1] != 's'):
                w = w + 's'
            elif (w[len(w)-1] == 'y'):
                w = w[:-1] + 'ies'
            elif (w[len(w)-1] == 's'):
                w = w + 'es'
            kw[id] = w
            keyword = ' '.join(kw)
            keywords.append(keyword)
            label.append(i)
            root.append(0)
            kw[id] = w_old
        if len(kw) > 1:
            for id,w in enumerate(kw):
                w = w + 's'
                kw[id] = w
            keyword = ' '.join(kw)
            keywords.append(keyword)
            label.append(i)
            root.append(0)


        # print(k)

print(keywords)
print(len(keywords))
print(label)
print(len(label))

d = {'Keyword':keywords,'Label':label,'Root':root}
df = pd.DataFrame(d)
df.to_csv('../data/keyword_label_plurals_2.csv',index=False,encoding='utf-8')