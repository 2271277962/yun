import requests
import json
#######################        
id = '12345678900'   ##        #
server_key = ''      ##      ########## 配置填写
#######################        #


#说明：
#   id通过抓取签到请求https://base.hjq.komect.com/signin/doJob/链接后面的数字获取


######签到####
def a(id):
    host = 'https://base.hjq.komect.com/signin/doJob/' + id
    data = '{"ruleId":31}'
    headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 18; Redmi Note 7 Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36;UniApp',
    'Content-Type':'application/json'
    }
    r = requests.post(url=host,headers=headers,data=data).text
    json1 = json.loads(r)
    if json1['code'] == 1000000:
        return json1['message'] ###签到成功
    else:
        if json1['code'] == 300008:
            return json1['message']####当日已签到过了
        else:
            return json1['message']####其他原因
##签到信息###
def b(id):
    host = 'https://base.hjq.komect.com/signin/record/info/' + id
    headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 18; Redmi Note 7 Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36;UniApp',
    'Content-Type':'application/json'
    }
    data = '{"activityId":"signin","date":"2021-03-15 11:11:11"}'
    r = requests.post(url=host,headers=headers,data=data).text
    json1 = json.loads(r)
    if json1['code'] == 1000000:
        yqd = str(json1['data']['signedDay'])#已签到多少天
        hsq = str(json1['data']['needDay'])#还剩多少天抽什么什么奖励
        jl = json1['data']['prizeName']#奖励
        zh = "已经累计签到"+ yqd + "天,再签到"+ hsq +"天可抽取 "+ jl +" 。"
        return zh
    else:
        return json1['message']####失败

##### sever酱 #######
def server(server_key,msg): 
    url = 'http://sc.ftqq.com/'+ server_key +'.send?text=合家亲签到&desp='+ msg
    r = requests.get(url).text
    return r
#####执行函数####
def main_handler(event, context):
    if server_key == '':
        #不使用
        msg = a(id) + "\n" +b(id)
        print(msg)
    else:
        ###使用server酱#####
        msg = a(id) + "\n" +b(id)
        server(server_key,msg)
