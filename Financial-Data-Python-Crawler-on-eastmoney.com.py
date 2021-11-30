
import requests
from bs4 import BeautifulSoup
import pprint
from selenium import  webdriver
import time
import warnings
import datetime
from prettytable import PrettyTable

warnings.filterwarnings('ignore')

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

def getCode():
             print('plzz tell me the stock code: (for HK and A stock and ETF only)')
             stock_code=input()
             if len(stock_code)==5:
                          url='http://quote.eastmoney.com/hk/{}.html'.format(stock_code)
             elif len(stock_code)==6:
                          url='http://quote.eastmoney.com/{}.html'.format(stock_code)
             else:
                          print('This is an invalid code. Input again:')
                          stock_code=input()
             return url

def getNSoup():  #normal soup
             try:
                          r=requests.get(url, headers=headers)
                          r.raise_for_status
                          soup=BeautifulSoup(r.text, 'html.parser')
                          return soup
             except:
                          print('找不到这只股票，请重新输入mmmmmm')

def getSSoup(url):  #active html selenium soup
             try:
                          driver=webdriver.PhantomJS()
                          driver.get(url)
                          time.sleep(3)
                          page=driver.page_source
                          driver.close()
                          soup=BeautifulSoup(page, 'html.parser')
                          return soup
             except:
                          print('找不到这只股票，请重新输入')
                          
def getName():
             if '/hk/' in url:
                          name=soup1.find('span', {'class': 'quote_title_0'}).get('title')
             elif url[-11]=='6' or url[-11]=='3' or url[-11]=='0':
                          name=soup2.find('h2', {'class': 'header-title-h2 fl'}).getText()
             elif url[-11]=='1' or url[-11]=='5':
                          name=soup2.find('span', {'class': 'quote_title_0 wryh'}).getText()
             return name

def getTable_HK():
             #***************************公司简介********************************************************************
             try:
                          t=PrettyTable(['公司简介'])
                          t.align='l'
                          t.add_row([soup2.find('dl', {'class':'companyIntroduce'}).find('h2').get('title').strip()])
                          t.add_row([soup2.find('dl', {'class':'companyIntroduce'}).findAll('dd')[0].getText()])
                          t.add_row([soup2.find('dl', {'class':'companyIntroduce'}).findAll('dd')[-2].getText()])
                          t.add_row([soup2.find('dl', {'class':'companyIntroduce'}).findAll('dd')[-1].get('title')])
                          print(t)
             except:
                          print('暂无公司简介')
             #***************************基本面数据*****************************************************************
             try:
                          print('|  基本面数据  |')
                          namelist=[]
                          numlist=[]
                          li1=[]
                          namelist.extend(['最新', '涨跌', '涨幅'])
                          for items in soup1.select('.brief_info li'):
                                       namelist.append(items.getText()[ :-4])  #基本面数据
                          for item in soup2.select('i'):
                                       numlist.append(item.getText())  #基本面数据
                          numlist=numlist[ :23]
                          for i in range(len(numlist)):
                                       li1.append([namelist[i]+numlist[i]])
                          li1.extend(['None'])
                          x=PrettyTable()
                          x.align='l'
                          x.add_row(li1[ :6])
                          x.add_row(li1[6:12])
                          x.add_row(li1[12:18])
                          x.add_row(li1[18: ])
                          print(x)
             except:
                          print('暂无基本面数据')
             #***************************相对恒指涨跌幅************************************************************
             try:
                          y=PrettyTable([soup1.find('p', {'class': 'brief_topP brief_side_title'}).getText().strip()])
                          y.align='l'
                          li6=[]
                          for items in soup2.find('div', {'id':'ABH_HengSengIndex'}).findAll('p'):
                                       li6.append(items.getText())
                          li6=[i for i in li6 if i !='']
                          for i in range(3):
                                       y.add_row([li6[i]])
                          print(y)
             except:    #如果同时在内地和香港上市，板块内容会变成相对A股的数据
                          print('此股票是同时在内地和香港上市的股票')
                          y=PrettyTable(['{}  A股行情'.format(getName())])
                          y.align='l'
                          y.add_row(['A股市场价格&涨幅'])
                          y.add_row([soup2.find('div', {'class': 'hqcrt'}).find('p', {'class': 'brief_botP'}).getText().strip()])
                          y.add_row([soup2.find('div', {'class': 'brief_side_f18'}).getText().strip()])
                          y.add_row([soup2.find('div', {'class': 'brief_side_f12'}).getText().strip()])
                          print(y)
             #***************************财务数据分析***************************************************************
             try:
                          namelist1=[]
                          numlist1=[]
                          li2=[]
                          for items in soup1.find('table', {'id':'financial_analysis'}).findAll('th'):
                                       namelist1.append(items.getText())
                          del namelist1[0]
                          for items in soup2.find('table', {'id':'financial_analysis'}).findAll('td'):
                                       numlist1.append(items.getText())
                          del numlist1[0]
                          del numlist1[10]
                          numlist1=numlist1[ :20]
                          for i in range(len(namelist1)):
                                       li2.append((namelist1[i], numlist1[i], numlist1[i+10]))
                          z=PrettyTable(['财务数据分析', '行业排名'])
                          z.align='l'
                          z.add_row(li2[ :2])
                          z.add_row(li2[2:4])
                          z.add_row(li2[4:6])
                          z.add_row(li2[6: 8])
                          z.add_row(li2[8:  ])
                          print(z)
             except:
                          print('暂无行业财务数据排名')
             #***************************机构评级********************************************************************
             try:
                          namelist2=[]
                          li3=[]
                          u=PrettyTable(['投行&评级&目标价'])
                          u.align='l'
                          for items in soup2.find('tbody', {'id':'jgpj_table'}).findAll('td'):
                                       namelist2.append(items.getText())
                          for i in range(int(len(namelist2)/3)):
                                       li3.append((namelist2[i*3], namelist2[i*3+1], namelist2[i*3+2]))
                                       u.add_row([li3[i]])
                          print(u)
             except:
                          print('暂无机构评级数据')
             #***************************机构增减持******************************************************************
             try:
                          numlist2=[]
                          li4=[]
                          v=PrettyTable(['机构(个人)名称&变动方向&变动股份数'])
                          v.align='l'
                          for items in soup2.find('tbody', {'id':'jgzjc_table'}).findAll('td'):
                                       numlist2.append(items.getText())
                          for i in range(int(len(numlist2)/3)):
                                       li4.append((numlist2[i*3], numlist2[i*3+1], numlist2[i*3+2]))
                                       v.add_row([li4[i]])
                          print(v)
             except:
                          print('暂无机构增减持数据')
             #***************************个股资讯*********************************************************************
             try:
                          numlist3=[]
                          li5=[]
                          w=PrettyTable(['个股资讯&链接'])
                          w.align='l'
                          for items in soup2.find('ul', {'class':'article_list nlist'}).findAll('a'):  #建立一个筛选机制显示完整标题
                                       if '...' not in items.getText().strip():
                                                    numlist3.append(items.getText().strip())
                                       else:
                                                    numlist3.append(items.find('span').get('title').strip())
                                       numlist3.append(items.get('href'))
                          for i in range(int(len(numlist3)/2)):
                                       li5.append((numlist3[i*2], numlist3[i*2+1]))
                                       w.add_row([li5[i]])
                          print(w)
             except:
                          print('暂无个股资讯')
                          
################################################################################

def getTable_A():
             #***************************基本面数据*****************************************************************
             try:
                          print('|  基本面数据  |')
                          namelist=[]
                          numlist=[]
                          li1=[]
                          namelist.extend(['最新', '涨跌', '涨幅'])
                          namelist.insert(1, soup2.find('div', {'id': 'arrowud'}).find('strong', {'data-bind': '43'}).getText())
                          namelist.insert(3, soup2.find('b', {'data-bind': 'change'}).getText())
                          namelist.insert(5, soup2.find('b', {'data-bind': 'changePercent'}).getText())
                          for items in soup2.select('.data-middle td'):
                                       namelist.append(items.getText().strip())#基本面数据
                          namelist[16]=namelist[16][ :5]+namelist[16][-1]
                          for i in range(int(len(namelist)/2)):
                                       li1.append([namelist[i*2]+namelist[i*2+1]])
                          li1.extend(['None'])
                          x=PrettyTable()
                          x.align='l'
                          x.add_row(li1[ :6])
                          x.add_row(li1[6:12])
                          x.add_row(li1[12: ])
                          print(x)
             except:
                          print('暂无基本面数据')
             #***************************最新财务指标***************************************************************
             code=url[-11:-5]
             url1='http://data.eastmoney.com/stockdata/{}.html'.format(code)
             soup3=getSSoup(url1)
             try:
                          namelist1=[]
                          li2=[]
                          y=PrettyTable(['指标名称&最新数据'])
                          y.align='l'
                          for items in soup3.find('div', {'id': 'm_zxzb'}).find('table', {'class': 'tab1'}).findAll('td'):
                                       namelist1.append(items.getText())
                          for i in range(int(len(namelist1)/2)):
                                       li2.append([namelist1[i*2]+'：'+namelist1[i*2+1]])
                                       y.add_row([li2[i]])
                          print(y)
             except:
                          print('暂无最新财务指标')
             #***************************主要业务构成***************************************************************
             try:
                          numlist1=[]
                          li3=[]
                          z=PrettyTable(['主营构成&主营收入&主营成本&主营利润'])
                          z.align='l'
                          for items in soup3.find('div', {'id': 'm_ywgc'}).find('table', {'class': 'tab1'}).findAll('td'):
                                       numlist1.append(items.getText())
                          for i in range(int(len(numlist1)/4)):
                                       li3.append([numlist1[i*4]+'：'+numlist1[i*4+1]+'   '+numlist1[i*4+2]+'   '+numlist1[i*4+3]])
                                       z.add_row([li3[i]])
                          print(z)
             except:
                          print('暂无主要业务构成数据')
             #***************************财务数据摘要***************************************************************
             try:
                          print('财务摘要：财务指标&时间（季度）')
                          namelist2=[]
                          numlist2=[]
                          for items in soup3.find('div', {'id': 'm_cwzy'}).find('table', {'class': 'tab1'}).findAll('th'):
                                       namelist2.append(items.getText())
                          u=PrettyTable(namelist2)
                          u.align='l'
                          for items in soup3.find('div', {'id': 'm_cwzy'}).find('table', {'class': 'tab1'}).findAll('td'):
                                       numlist2.append(items.getText())
                          numlist2.remove('利润表(元)')
                          numlist2.remove('\xa0')
                          numlist2.remove('资产负债表(元)')
                          numlist2.remove('\xa0')
                          numlist2.remove('现金流量表(元)')
                          numlist2.remove('\xa0')
                          aa=len(namelist2)
                          for i in range(0,7):
                                       u.add_row([numlist2[i*aa], numlist2[i*aa+1], numlist2[i*aa+2], numlist2[i*aa+3], numlist2[i*aa+4], numlist2[i*aa+5]])
                          u.add_row(['利润表(元)', ' ', ' ', ' ', '  ', ' '])
                          for i in range(7,10):
                                       u.add_row([numlist2[i*aa], numlist2[i*aa+1], numlist2[i*aa+2], numlist2[i*aa+3], numlist2[i*aa+4], numlist2[i*aa+5]])
                          u.add_row(['资产负债表(元)', '  ', ' ', ' ', ' ', ' '])
                          for i in range(10,13):
                                       u.add_row([numlist2[i*aa], numlist2[i*aa+1], numlist2[i*aa+2], numlist2[i*aa+3], numlist2[i*aa+4], numlist2[i*aa+5]])
                          u.add_row(['现金流量表(元)', ' ', ' ', ' ', '  ', ' '])
                          for i in range(13, 17):
                                       u.add_row([numlist2[i*aa], numlist2[i*aa+1], numlist2[i*aa+2], numlist2[i*aa+3], numlist2[i*aa+4], numlist2[i*aa+5]])
                          print(u)
             except:
                          print('暂无财务数据摘要')
             #***************************四分位财务数据分析***************************************************************
             try:
                          namelist3=[]
                          namelist4=[]
                          li4=[]
                          v=PrettyTable(['核心财务数据&行业平均&行业排名'])
                          v.align='l'
                          for items in soup2.find('div', {'class':'cwzb'}).find('table').findAll('th'):
                                       namelist3.append(items.getText())
                          del namelist3[0]
                          for items in soup2.find('div', {'class':'cwzb'}).find('table').findAll('td'):
                                       namelist4.append(items.getText())
                          del namelist4[0]
                          del namelist4[8]
                          del namelist4[16]
                          namelist4=namelist4[ : 24]
                          for i in range(len(namelist3)):
                                       li4.append((namelist3[i], namelist4[i], namelist4[i+8], namelist4[i+16]))
                                       v.add_row([li4[i]])
                          print(v)
             except:
                          print('暂无行业财务数据排名')
             #***************************个股资讯*********************************************************************
             try:
                          numlist3=[]
                          li5=[]
                          w=PrettyTable(['个股资讯&链接'])
                          w.align='l'
                          for items in soup2.find('div', {'id':'cggy1'}).findAll('a'):
                                       numlist3.append(items.get('title'))
                                       numlist3.append(items.get('href'))
                          for i in range(int(len(numlist3)/2)):
                                       li5.append((numlist3[i*2], numlist3[i*2+1]))
                                       w.add_row([li5[i]])
                          print(w)
             except:
                          print('暂无个股资讯')
             #***************************个股研报*********************************************************************
             try:
                          numlist4=[]
                          li6=[]
                          t=PrettyTable(['个股研报&评级&链接'])
                          t.align='l'
                          aaaa=soup2.find('table', {'id':'ggybTable'}).findAll('tr')
                          for i in range(int(len(aaaa)-1)):
                                       numlist4.append(aaaa[i+1].findAll('td')[0].find('a').get('title'))
                                       try:
                                                    numlist4.append(aaaa[i+1].findAll('td')[1].find('span').get('title'))
                                       except:
                                                    numlist4.append('---')
                                       numlist4.append(aaaa[i+1].findAll('td')[2].find('a').get('title'))
                                       numlist4.append(aaaa[i+1].findAll('td')[2].find('a').get('href'))
                          for i in range(int(len(numlist4)/4)): 
                                       li6.append((numlist4[i*4], numlist4[i*4+1], numlist4[i*4+2], numlist4[i*4+3]))
                                       t.add_row([li6[i]])
                          print(t)
             except:
                          print('暂无个股研报')

##############################################################################

def getTable_ETF():
             #***************************基本面数据*****************************************************************
             try:
                          print('|  基本面数据  |')
                          namelist=[]
                          li1=[]
                          namelist.extend(['最新', '涨跌', '涨幅'])
                          namelist.insert(1, soup2.find('div', {'id': 'arrowud'}).getText().strip())
                          namelist.insert(3, soup2.find('span', {'class': 'xp34'}).find('b').getText())
                          namelist.insert(5, soup2.find('span', {'class': 'xp34'}).findAll('b')[1].getText())
                          for items in soup2.find('div', {'class': 'data-middle fr'}).findAll('span'):
                                       namelist.append(items.getText().strip())#基本面数据
                          for i in range(int(len(namelist)/2)):
                                       li1.append([namelist[i*2]+namelist[i*2+1]])
                          li1.extend(['None'])
                          x=PrettyTable()
                          x.align='l'
                          x.add_row(li1[ :6])
                          x.add_row(li1[6:12])
                          x.add_row(li1[12: ])
                          print(x)
             except:
                          print('暂无基本面数据')
             #***************************基本概况********************************************************************
             code=url[-11:-5]
             url1='http://fund.eastmoney.com/f10/jbgk_{}.html'.format(code)
             soup3=getSSoup(url1)
             try:
                          namelist1=[]
                          li2=[]
                          y=PrettyTable(['基金基本概况'])
                          y.align='l'
                          for items in soup3.find('table', {'class': 'info w790'}).findAll('th'):
                                       namelist1.append(items.getText())
                          for items in soup3.find('table', {'class': 'info w790'}).findAll('td'):
                                       namelist1.append(items.getText())
                          for i in range(int(len(namelist1)/2)):
                                       li2.append([namelist1[i]+'：'+namelist1[i+20]])
                                       y.add_row([li2[i]])
                          print(y)
             except:
                          print('暂无基金基本概况')
             #***************************持仓明细********************************************************************
             try:
                          print('该基金股票持仓明细')
                          numlist1=[]
                          li3=[]
                          z=PrettyTable(['股票名称&持仓占比&个股涨跌幅'])
                          z.align='l'
                          for items in soup2.find('table', {'id': 'gpchc'}).findAll('td'):
                                       numlist1.append(items.getText().strip())
                          for i in range(int(len(numlist1)/3)):
                                       li3.append([numlist1[i*3]+'    '+numlist1[i*3+1]+'   '+numlist1[i*3+2]])
                                       z.add_row([li3[i]])
                          z.add_row([soup2.find('p', {'class': 'top10_p'}).getText().strip()])
                          print(z)
             except:
                          print('暂无该基金股票持仓明细数据')
             #***************************阶段涨幅明细***************************************************************
             code=url[-11:-5]
             url2='http://fund.eastmoney.com/f10/jdzf_{}.html'.format(code)
             soup4=getSSoup(url2)
             try:
                          print('阶段涨幅明细')
                          namelist3=[]
                          namelist4=[]
                          li4=[]
                          v=PrettyTable(['时间&涨幅&同类平均&沪深300&同类排名'])
                          v.align='l'
                          for items in soup4.find('div', {'class':'jdzfnew'}).findAll('ul')[1:-1]:
                                       for i in items.findAll('li')[ :5]:
                                                    namelist3.append(i.getText())
                          for i in range(int(len(namelist3)/5)):
                                       li4.append([namelist3[i*5]+'：'+namelist3[i*5+1]+'     '+namelist3[i*5+2]+'     '+namelist3[i*5+3]+'     '+namelist3[i*5+4]])
                                       v.add_row([li4[i]])
                          print(v)
             except:
                          print('暂无阶段涨幅明细数据')
             #***************************基金资讯********************************************************************
             try:
                          numlist3=[]
                          li5=[]
                          w=PrettyTable(['基金资讯&链接'])
                          w.align='l'
                          for items in soup2.find('div', {'class':'news_list fl'}).find('ul', {'id': 'stocknews'}).findAll('a'):
                                       numlist3.append(items.get('title'))
                                       numlist3.append(items.get('href'))
                          for i in range(int(len(numlist3)/2)):
                                       li5.append((numlist3[i*2], numlist3[i*2+1]))
                                       w.add_row([li5[i]])
                          print(w)
             except:
                          print('暂无基金资讯')

#################################################################################

def getTable():
             if '/hk/' in url:
                          getTable_HK()
             elif url[-11]=='6' or url[-11]=='3' or url[-11]=='0':
                          getTable_A()
             elif url[-11]=='1' or url[-11]=='5':
                          getTable_ETF()
                          

while True:
             url=getCode()
             startTime=time.time()
             soup1=getNSoup()
             soup2=getSSoup(url)
             name=getName()
             print('这是{}的基本数据：'.format(name))
             print('时间：{}'.format(datetime.datetime.now()))
             getTable()
             endTime=time.time()
             print('用时：{}'.format(str(round(endTime-startTime,4))))
             print('if u want to exit, press enter. Press any other keys to continue.')
             bb=input()
             if bb=='\n':
                          break
             
             
#明天继续优化，加入A股 简化程序 还有挺多可以优化的,继续debug
#加入美股A股
