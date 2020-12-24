import requests
headers = {
        'user-agent':'Mozilla/5.0 (Linux; Android 10; Redmi K30 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.127 Mobile Safari/537.36',
        ##    下面填抓包来的参数########
        'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2NsYWltcyI6eyJzYWx0IjoxMDAsIm51bWJlciI6NTYyMDk1Njk5LCJ0aW1lc3RhbXAiOjE2MDQ0OTE3ODV9LCJpZGVudGl0eSI6IjVkZTIxMWIyZmZhMDNjMGZkNTA4MjRiMSIsImp0aSI6IjkzMTA5NWViLWVkNzctNGJhMC1iMjdjLWY1YjUxNTQwOTYwNCIsImlhdCI6MTYwNDQ5MTc4NSwibmJmIjoxNjA0NDkxNzg1LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.hvacTOwTmXWiNiKMJ_O66x-ujEtj6mhTC2R1aZ1ronE'
        }
#####Server酱的sckey填这里，不需要可以留空####
server_key = 'SCU102384Tbda8eb6ed4bf8ec01eb04dd3adc11ff95eef779fd44c1'
def qiandao(headers):
    url = 'http://n.cg.163.com/api/v2/sign-today'
    r = requests.post(url,headers=headers).text
    if (r[0] == "{"):        
        return("cookie已失效")
    else:
        return("签到成功")
####Server酱#######
def server(server_key):
    msg = qiandao(headers) 
    url = 'http://sc.ftqq.com/'+ server_key +'.send?text=网易云游戏签到&desp='+ msg
    r = requests.get(url).text
    return r
#######结束签到#######
def main_handler(event, context):
    if (server_key==''):
        return qiandao(headers)
    else:
        return server(server_key)
