# coding: utf-8
import requests
import json
import hashlib

##账号
zh = ''
##密码
mm = ''
###登陆请求的'authdata'参数，必填！！！（我也不知道这是啥加密，有知道的大佬请指教一下）
authdata = ''
##server酱，不需要或者不知道是什么可以不填
server_key = ''


##登录
def logo(zh,mm):
    m = hashlib.md5()
    b = mm.encode(encoding='utf-8')
    m.update(b)
    mm_md5 = m.hexdigest()
    url = 'https://base.hjq.komect.com/base/user/passwdLogin'
    headers = {
        'User-Agent':'UniApp',
        'Content-Type':'application/json; charset=UTF-8',
        'Content-Length':'473',
        'Host':'base.hjq.komect.com'
    }
    data = '{"image":{"path":"token"},"deviceUuid":"b746cdd9d870d117","os":"android","wifiSsid":"","imsi":"","devMac":"00:0C:A0:D6:0A:60","phoneNumber":"'+ zh +'","isWifi":true,"virtualAuthdata":"'+ mm_md5 +'","userAccount":"'+ zh +'","authdata":"'+ authdata +'","appid":"01010811","imei":"","deviceflag":"dami","wifiMac":"02:00:00:00:00:00","authType":"10","channelId":"6","timestamp":"1616415977532"}'
    u = requests.post(url=url,headers=headers,data=data)
    list = []
    if json.loads(u.text)['code'] == "2202042": 
        list.append(1)
        list.append("authdata参数填写错误！！！")
    else:
        if json.loads(u.text)['code'] == "1000000":
            ###校检密码
            host2 = 'https://base.hjq.komect.com/activity-hjq/activitycommon/drawChance'
            headers2 = {
                'Host':'base.hjq.komect.com',
                'Content-Length':'64',
                'Accept':'application/json, text/plain, */*',
                'User-Agent':'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36;UniApp',
                'Content-Type':'application/json',
                'Origin':'https://base.hjq.komect.com',
                'cookie':'JSESSIONID='+ requests.utils.dict_from_cookiejar(u.cookies)['JSESSIONID']
                }
            data2 = '{"passId":"'+ json.loads(u.text)['data']['passId'] +'","code":"SCdraw0204","jobCode":"J020"}'
            mi = requests.post(url=host2,headers=headers2,data=data2)
            if json.loads(mi.text)['code'] == "5200000":##这里貌似有点问题，懒得搞了！运行不出问题就行
                list.append(1)
                list.append("密码错误！！！")
            else:
                if json.loads(mi.text)['code'] == "1000000":
                    ###确定需要的参数
                    cookie = requests.utils.dict_from_cookiejar(u.cookies)['JSESSIONID']
                    id = json.loads(u.text)['data']['passId']
                    ##创建列表   
                    list.append(id)
                    list.append(cookie)
                else:
                    list.append(1)
                    list.append("authdata正确，密码其他错误！！")      
        else:
            list.append(1)
            list.append("其他错误")
    return list

######签到####
def a(id):
    host = 'http://base.hjq.komect.com/signin/doJob/' + id
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
    host = 'http://base.hjq.komect.com/signin/record/info/' + id
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

###尝试签到部分的抽奖
def c(id):
    host = 'http://base.hjq.komect.com/signin/draw/' + id
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 18; Redmi Note 7 Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36;UniApp',
        'Content-Type':'application/json'
    }
    data = '{"rewardId":420127}'
    r = requests.post(url=host,headers=headers,data=data).text
    json1 = json.loads(r)
    if json1['code'] == 1000000:
        pc = "本次抽奖抽到了 " + json1['data']['reward']['productName'] + " "
        return pc
    else:
        if json1['code'] == 200006:
            return("机会用完")
        else:
            return("其他错误")

###商城每天两次的抽奖##
def d(id,cookie):
    ###每天一次的分享###
    host = 'https://base.hjq.komect.com/activity-hjq/activitycommon/drawChance'
    headers = {
        'Host':'base.hjq.komect.com',
        'Content-Length':'64',
        'Accept':'application/json, text/plain, */*',
        'User-Agent':'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36;UniApp',
        'Content-Type':'application/json',
        'Origin':'https://base.hjq.komect.com',
        'cookie':'JSESSIONID='+ cookie
    }
    data = '{"passId":"'+ id +'","code":"SCdraw0204","jobCode":"J020"}'
    u = requests.post(url=host,headers=headers,data=data)
    ####抽奖##
    host2 = 'https://base.hjq.komect.com/activity-hjq/activitycommon/draw'
    headers2 = {
        'Host':'base.hjq.komect.com',
        'Content-Length':'47',
        'Accept':'application/json, text/plain, */*',
        'User-Agent':'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Build/QKQ1.190910.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36;UniApp',
        'Content-Type':'application/json',
        'Cookie':'JSESSIONID='+ cookie
    }
    data2 = '{"passId":"'+ id +'","code":"SCdraw0204"}'
    ###第一次
    u1 = requests.post(url=host2,headers=headers2,data=data2)
    code = json.loads(u1.text)['code']
    if code == "1000000":
        print("签到成功")
        a1 = "成功，抽到了 "+ json.loads(u1.text)['data']['productName']
    else:
        if code == "5200000":
            a1 = "失败，登录已经失效"
        if code == "5222052":
            a1 = "失败，你今天已经签到过了"
        else:
            a2 = "失败，其他错误（这个一般是程序问题请联系作者修复bug、）"
    ###第二次
    u2 = requests.post(url=host2,headers=headers2,data=data2)
    code2 = json.loads(u2.text)['code']
    if code2 == "1000000":
        a2 = "成功，抽到了 "+ json.loads(u2.text)['data']['productName']
    else:
        if code2 == "5200000":
            a2 = "失败，登录已经失效"
        if code2 == "5222052":
            a2 = "失败，你今天已经签到过了"
        else:
            a2 = "失败，其他错误（这个一般是程序问题请联系作者修复bug、）"
    list = []
    list.append(a1)
    list.append(a2)
    return list


##### sever酱 #######
def server(server_key,msg): 
    r = requests.post(url='http://sc.ftqq.com/'+ server_key +'.send', data={"text": "和家亲签到", "desp": msg})
    return r.text

#####执行函数####
def main_handler(event, context):
    main = logo(zh,mm)
    if main[0] == 1:
        return main[1]
    else:
        id = main[0]
        cookie = main[1]
        a_ = a(id)  
        b_ = b(id) 
        c_ = c(id)  
        d_ = d(id,cookie)
        msg = "####**签到状态**\n\n"+ a_ +"\n\n####**签到信息**\n\n"+ b_ +"\n\n####**抽奖情况**\n\n#####签到抽奖\n\n###### - "+ c_ +"\n\n#####两次抽奖\n\n###### - "+ d_[0] +"\n\n###### - "+ d_[1]
        if server_key == '':
            print(msg)
        else:
            al= server(server_key,msg)
            print(al)
