import pandas as pd

df = pd.read_csv('../data/result_kw_plurals_3.csv')
# dff = pd.read_csv('../data/keyword_label_plurals.csv')

# dff["Freq"] = df["Value"]
# dff.to_csv('../data/plurals_demo.csv',index=False,encoding='utf-8')

print(df.shape)
# print(dff.shape)
# exit()

label = list(df['Label'])
dLabel = {}
for i in label:
    dLabel[i] = 0

for i,row in df.iterrows():
    l = row["Label"]
    pre_freq = dLabel[l]
    freq = pre_freq + row["Freq"]
    dLabel[l] = freq
freqs = []
for k,v in dLabel.items():
    print('Key : %d - Value: %d ' %(k,v))
    freqs.append(v)
    # print(v)

df = df.loc[df["Root"] == 1]
df = df.drop(['Label','Root'],axis=1)
df["Freq"] = freqs
print(df.shape)
df.to_csv('../data/kw_plurals_freq_3.csv',index=False,encoding='utf-8')
# df['Freq'] = dLabel

# print(dLabel)