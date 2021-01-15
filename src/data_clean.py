import pandas as pd

# 迁出数据
filenames = ["NCP_EmigrRatioD{}.xlsx".format(i) for i in ["","1","2","3","4"]]

data = dict()

for filename in filenames:
    data[filename] = pd.read_excel(filename)
    data[filename].columns =["统计日期","迁出地区","迁出地区代码","隶属省份","迁出目的地","迁出目的地代码","迁出人口比例"]
    data[filename].drop([0,1],inplace=True)
    data[filename].drop(columns=['迁出地区代码','隶属省份','迁出目的地代码'],inplace=True)
    data[filename]['统计日期'] = pd.to_datetime(data[filename]['统计日期'])
    data[filename]['统计日期'] = data[filename]['统计日期'].dt.date
    data[filename].sort_values(['统计日期','迁出地区','迁出人口比例'],ascending=[True,True,False],inplace=True)
    data[filename] = data[filename][~data[filename]['迁出目的地'].str.contains("省")]
    data[filename] = data[filename].groupby(['统计日期','迁出地区']).head(5)
    print(filename + " done")

result = pd.concat(data.values())
result.to_json("cleaned/emigrate.json",index=False)
print("succeed!")


# 迁入数据
filenames = ["NCP_ImmigrRatioD{}.xlsx".format(i) for i in ["","1","2","3","4","5"]]

data = dict()

for filename in filenames:
    data[filename] = pd.read_excel(filename)
    data[filename].columns =["统计日期","迁入地区","迁入地区代码","隶属省份","迁入来源地","迁入来源地代码","迁入来源地隶属省份","迁入人口比例"]
    data[filename].drop([0,1],inplace=True)
    data[filename].drop(columns=['迁入地区代码','隶属省份','迁入来源地代码',"迁入来源地隶属省份"],inplace=True)
    data[filename]['统计日期'] = pd.to_datetime(data[filename]['统计日期'])
    data[filename]['统计日期'] = data[filename]['统计日期'].dt.date
    data[filename].sort_values(['统计日期','迁入地区','迁入人口比例'],ascending=[True,True,False],inplace=True)
    data[filename] = data[filename][~data[filename]['迁入来源地'].str.contains("省")]
    data[filename] = data[filename].groupby(['统计日期','迁入地区']).head(5)
    print(filename + " done")

result = pd.concat(data.values())
result.to_excel("cleaned/immigrate.json",index=False)
result.reset_index(inplace=True)
result.to_json("cleaned/emigrate.json")
print("succeed!")

# 医院数据
data = pd.read_excel("NCP_RegMedHosSta.xlsx")
data.drop(columns = "AreaCode",inplace=True)
data.columns = ['name','value']
data.drop(index=[0,1],inplace=True)
data['name'] = data['name'].str.rstrip('市') 
data.to_json("hospital.json",orient="table",index=False)


# 产业数据
data = pd.read_excel("NCP_ProvincialGDP.xlsx")
data.drop(index=[0,1],inplace=True)
data.columns = ['年度标识', '省份编码', '省份名称', '地区生产总值-第一产业', '地区生产总值-第二产业', '地区生产总值-第三产业']
data.drop(columns=['省份编码'],inplace=True)
data.columns = ['year','province','one','two','three']
data.reindex(columns=['one','two','three','province','year']) 
data = data[data['province'] != '中国']
data.to_json('provinceGDP.json',orient='table',index=False)
file = read('provinceGDP.json')
data = file.read()
c = eval(data)
years = [i for i in range(1952,2020)]
series_data = [[] for i in range(len(years))]
for i,year in enumerate(years):
    for j in c:
        j['year'] = int(j['year'])
        if j['year'] == year:
            series_data[i].append(list(j.values()))
d = open('test3.txt',mode='x',encoding='utf-8')
d.write(str(series_data))