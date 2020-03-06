# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
import requests
from lxml import etree
import json,datetime,time
import scraperwiki
from datetime import datetime
import pytz

#爬取美国确诊人数
confirmxpath='//*[@id="stat"]/div/div[1]/div/dl[1]/dd/text()'
recoverxpath='//*[@id="stat"]/div/div[1]/div/dl[2]/dd/text()'
deathxpath='//*[@id="stat"]/div/div[1]/div/dl[3]/dd/text()'

url='https://coronavirus.1point3acres.com/zh'
content = etree.HTML(requests.get(url,verify=False).text)
usa_con=content.xpath(confirmxpath)[0]
usa_rec=content.xpath(recoverxpath)[0]
usa_dea=content.xpath(deathxpath)[0]

result_pop=[{'confirm':usa_con,"recover":usa_rec,"death":usa_dea}]
with open('result_pop.json','w') as file_obj:
    json.dump(result_pop,file_obj)

nowdays=datetime.datetime.now().strftime('%d-%m-%Y')
yesterday = (datetime.date.today() + datetime.timedelta(-1)).strftime('%m-%d-%Y')

time.sleep(0)#休息一定的时间，做定时脚本
url='https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/'+yesterday+'.csv'
resp=requests.get(url,verify=False).text
print(url)
xpath_con='//table[contains(@class,"js-csv-data")]/tbody/tr'
content = etree.HTML(resp)

vir={}
death={}
recover={}

all=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Mississippi', 'Missouri', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode island', 'South Carolina', 'South Dakota', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New jersey', 'New Mexico', 'New York', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Virginia', 'Wyoming']
low=['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'KYE', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'MS', 'MO', 'NC', 'ND', 'OH', 'OKS', 'OR', 'PA', 'RI', 'SC', 'SD', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'VA', 'WY']
for i in all:
    vir[i]=0#初始化数据
    death[i]=0
    recover[i]=0

for p in content.xpath(xpath_con):
    if p.xpath('./td[3]/text()')[0]=='US':
        area = p.xpath('./td[2]/text()')[0]
        confirm = p.xpath('./td[5]/text()')[0]
        deaths=p.xpath('./td[6]/text()')[0]
        recovered=p.xpath('./td[7]/text()')[0]
        # 这些数据暂时用不到
        for j in low:
            if (', '+j) in area:
                index=low.index(j)
                Full_name=all[index]#输出了全称
                vir[Full_name]=vir[Full_name]+int(confirm)
                death[Full_name] = death[Full_name] + int(deaths)
                recover[Full_name] = recover[Full_name] + int(recovered)
print(vir)

result1=[]
result2=[]
result3=[]
for k,v in vir.items():
    s={}
    s['name']=k
    s['value']=v
    result1.append(s)
for k,v in death.items():
    s={}
    s['name']=k
    s['value']=v
    result2.append(s)
for k,v in recover.items():
    s={}
    s['name']=k
    s['value']=v
    result3.append(s)

# hkt = pytz.timezone('Asia/Hong_Kong')
# dt = datetime.now().replace(tzinfo=hkt).date()
# # data = {titles[i]: values[i] for i in range(0, 4)}
# data['date'] = dt
# scraperwiki.sqlite.save(unique_keys=['date'], data=result1)
# scraperwiki.sqlite.save(unique_keys=['date'], data=result2)
# scraperwiki.sqlite.save(unique_keys=['date'], data=result3)

with open('virus.json','w') as file_obj:
    json.dump(result1,file_obj)
with open('death.json','w') as file_obj:
    json.dump(result2,file_obj)
with open('recover.json','w') as file_obj:
    json.dump(result3,file_obj)
