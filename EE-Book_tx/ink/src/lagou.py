# -*-coding:utf-8-*-
import csv
import json
import requests
import sys

#解决编码问题
reload(sys)
sys.setdefaultencoding('utf-8')

#获取json数据
def get_json_data(city,position,page):
    #请求拉勾的职位查询接口，返回的是json格式数据
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'.format(city)
    data = {
        'first':'false',
        'pn':page,
        'kd':position
    }
    # header 里面加cookie就可以防止被ban
    headers = {
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Cookie':'JSESSIONID=15A9FE2A6A2CC09A2FB61021BF8E8086; '
                 'user_trace_token=20170501124201-1adf364d88864075b61dde9bdd5871ea; '
                 'LGUID=20170501124202-850be946-2e28-11e7-b43c-5254005c3644; '
                 'index_location_city=%E5%8C%97%E4%BA%AC; TG-TRACK-CODE=index_search;'
                 ' SEARCH_ID=0a596428cb014d3bab7284f879e214f0; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1493613734;'
                 ' Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1493622592;'
                 ' LGRID=20170501150939-247d4c29-2e3d-11e7-8a78-525400f775ce;'
                 ' _ga=GA1.2.1933438823.1493613734'
    }
    response = requests.post(url,headers=headers,data=data)
    return response.text

#获取最大页数
def get_max_pageNumber(city,position):
    # 请求职位查询接口，用总条数除以每页的条数15，得到总页数
    result = get_json_data(city,position,'1')
    pageNumber = int(json.loads(result)['content']['positionResult']['totalCount']/15)
    return pageNumber

#从json数据里面获取想要的字段
def get_positon_results(json_data):
    data = json.loads(json_data)
    #状态是成功的再处理
    if data['success'] == True:
        position_results = []
        positions = data['content']['positionResult']['result']
        for item in positions:
            companyShortName = item['companyShortName']
            companyFullName = item['companyFullName']
            companySize = item['companySize']
            positionName = item['positionName']
            workYear = item['workYear']
            salary = item['salary']
            industryField = item['industryField']
            financeStage = item['financeStage']
            createTime = item['createTime']
            education = item['education']
            district = item['district']
            positionId = item['positionId']
            jobNature = item['jobNature']
            positionAdvantage = item['positionAdvantage']
            positionUrl = 'https://www.lagou.com/jobs/' + str(positionId) + '.html'


            position_results.append([companyFullName,positionName,workYear,salary,industryField,financeStage,
                                     companyShortName,companySize,createTime,education,district,jobNature,
                                     positionAdvantage,positionId,positionUrl])
        return position_results
    else:
        print '数据出错了...'

def writeCSV(file,data_list):
    with open(file,'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['公司名称','职位名称','工作年限','薪资范围','行业','融资情况',
                         '公司简称','公司规模','发布时间','学历要求','地区','工作性质','职位优势','职位ID','职位链接'])
        for data in data_list:
            for row in data:
                writer.writerow(row)


def main():
    # city = raw_input('请输入城市').strip()
    # position = raw_input('请输入职位名称').strip()
    # fileName = raw_input('请输入文件名(无需后缀)')
    city = "深圳"
    position ="iOS"
    fileName ="iDev"
    filePath = '/Users/liyan/Documents/' + fileName + '.csv'
    pageNumber = get_max_pageNumber(city,position)
    positions = []
    for i in range(1,pageNumber + 1):
        print '开始爬第{}页...'.format(i)
        page_data = get_json_data(city,position,str(i))
        page_result = get_positon_results(page_data)
        positions.append(page_result)

    writeCSV(filePath,positions)

if __name__ == '__main__':
    main()