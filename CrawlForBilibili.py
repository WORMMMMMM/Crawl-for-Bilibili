import json
import time
from random import random
from urllib.parse import urlencode
import math
import pandas as pd
import requests
#定义一个Person类，用来存储人的信息
class Person:
    def __init__(self, name, mid, likes="", views="", followings="", followers=""):
        self.name = name
        self.mid = mid
        self.likes = likes
        self.views = views
        self.followings = followings
        self.followers = followers

DATA_PATH_personal_information = "./personal_information.csv"
DATA_PATH_social_network = "./social_network.csv"
# TODO: 根据分析结果，构建Headers

Cookie = "buvid3=A1F0E047-AE95-D788-A1DC-61A5D8340A1495364infoc; b_nut=1714019595; _uuid=E1A7599C-F9BA-F73F-963F-2F5EFB5A578394039infoc; enable_web_push=DISABLE; buvid4=DCD806D9-5143-7DCC-8D96-65F6E0EB4D4F76556-024030614-N93wYaw5nav0jnXIG8Zldg%3D%3D; CURRENT_FNVAL=4048; rpdid=|(J|)ulRlulm0J'u~uR|umYJR; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; PVID=3; CURRENT_QUALITY=80; buvid_fp_plain=undefined; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgwMzU5ODksImlhdCI6MTcxNzc3NjcyOSwicGx0IjotMX0.0m4SkimqzFO72LKoK0OBxnpPb5-krxLR04k9BZpQQbA; bili_ticket_expires=1718035929; fingerprint=e6114bd0f8bdde0d871819cc3065c55c; buvid_fp=e6114bd0f8bdde0d871819cc3065c55c; home_feed_column=5; browser_resolution=1488-742; SESSDATA=a29b6690%2C1733496225%2Ccf64a%2A61CjDT82qQKNNxazv-vyF7Wj7qbksvKOXwYnWV_QAI91eDMgohPuDbenbqw0aN1-_MzGESVjh2X1VFaVV3REVLMGExOVZHVUxyS2sxVEMzdURuYnRGSDhQTHN1bEhoT0FjVDhiNzYyMmxQQzBvTGt6SzZVb2kzQzBnYnpSZXQxX3UwQmdfUGJaOEt3IIEC; bili_jct=8bb992b88eacea78349a2592d2d93f89; DedeUserID=89627183; DedeUserID__ckMd5=261642d5b9251dcd; sid=6laikshi; bp_t_offset_89627183=941039218780536881; b_lsid=1B106FC64_190016301C4"
headers = {
    "authority":"api.bilibili.com",
    "Cookie": Cookie,
    "method": "GET",
    "scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br,zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Origin": "https://space.bilibili.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
}

# 模拟访问，得到数据
#count=0#用来记录爬取的信息数
import pandas as pd
import requests
from urllib.parse import urlencode
import json
import time
from random import random

def scrape_bilibili_personal_info(DATA_PATH,srcid,srcname):
    exception1=0
    exception2=0
    exception3=0
    try:
        data = pd.read_csv(DATA_PATH)
    except:
        data = pd.DataFrame()
        print("personal_info establish")
    srcid1=str(srcid)
    srcname1=str(srcname)
    followings = "privacy"
    followers = "privacy"
    likes = "privacy"
    views = "privacy"

    params={
        "vmid":str(srcid),
        "pn":"1",
        "ps":"20",
        "order":"desc",
        "gaia_source":"main_web",
        "web_location":"333.999"
    }
    url = "https://api.bilibili.com/x/relation/fans?" + urlencode(params)
    
    res = requests.get(url,headers=headers)
    try:
        data_json = json.loads(res.content.decode('utf-8', 'ignore'))   
    except:
        followers="privacy"
        exception1=1
    if exception1!=1:
        if "data" in data_json:
            followers=data_json["data"]["total"]
        else:
            followers="privacy"
    
    time.sleep(random() * 2)  # 0~2秒随机sleep

    url = "https://api.bilibili.com/x/relation/followings?" + urlencode(params)
    res = requests.get(url,headers=headers)
    try:
        data_json = json.loads(res.content.decode('utf-8', 'ignore'))   
    except:
        followings="privacy"
        exception2=1
    if exception2!=1:
        if "data" in data_json:
            followings=data_json["data"]["total"]
        else:
            followings="privacy"
    time.sleep(random() * 2)  # 0~2秒随机sleep

    params = {
        "mid":str(srcid),
        "web_location":"333.999"
    }
    url = "https://api.bilibili.com/x/space/upstat?" + urlencode(params)
    res = requests.get(url,headers=headers)
    #print(res.headers)
    try:
        data_json=json.loads(res.content)
    except:
        likes="privacy"
        views="privacy"
        exception3=1
    if exception3!=1:
        if "data" in data_json:
            likes=data_json["data"]["likes"]
            if "archive" in data_json["data"]:
                views=data_json["data"]["archive"]["view"]
    ''' print("---Error!---")
        print("---Array Length error---")
        print(srcname)
        print(srcid)
        print(likes)
        print(views)
        print(followers)
        print(followings)
        print("----------------")'''
#        a=input()
    tmp = pd.DataFrame(
    {
        "SourceName": [srcname1],  # 将标量值转换为列表
        "SourceID": [srcid1],      # 将标量值转换为列表
        "followers": [followers],  # 将标量值转换为列表
        "followings": [followings], # 将标量值转换为列表
        "likes": [likes],
        "views": [views]
    }
)
        
    data = pd.concat((data, tmp), axis=0)  # 与之前结果合并   
    data.to_csv(DATA_PATH, index=False, encoding="UTF-8")  # 写入文件
        
        # 随机sleep一段时间，防止爬取频率过高被封号
            
    time.sleep(random() * 2)  # 0~2秒随机sleep
    return  followers, followings



def scrape_bilibili_followings(DATA_PATH,pagenumber,srcname,srcid,person_queue,duplicate_check,steps):
    if steps<=0:
        return

    page = "0"
    for p in range(pagenumber):
        try:
            data = pd.read_csv(DATA_PATH)  # 从之前保存的结果继续爬取
        except:
            data = pd.DataFrame()  # 新建一个csv对象
            print("establish")
        name = []
        id=[]
        sourcename=[]
        sourceid=[]
        page = int(page)
        page += 1
        page = str(page)
        # 构建Url中的query参数
        if page == "1":
            params = {
                "pn": "1",
                "vmid": str(srcid),
                "ps": "20",
                "order": "desc",
                "gaia_source": "main_web",
                "web_location": "333.999"
            }
        else:
            params = {
                "pn": page,
                "page_type": "searchall",
                "vmid": str(srcid),
                "ps": "20",
                "order": "desc",
                "gaia_source": "main_web",
                "web_location": "333.999"
            }

        # 通过urlencode将参数拼接到url后面
        url = "https://api.bilibili.com/x/relation/followings?" + urlencode(params)
        res = requests.get(url, headers=headers)
        data_json = json.loads(res.content)
        if "data" in data_json:
            for singlewb in data_json["data"]["list"]:
                name.append(singlewb["uname"])
                id.append(singlewb["mid"])
                sourcename.append(srcname)
                sourceid.append(srcid)
                print(singlewb["uname"],steps)
                if singlewb["uname"] not in duplicate_check:
                    person_queue.append(Person(singlewb["uname"],singlewb["mid"]))
                    duplicate_check.add(singlewb["uname"])
                # print(singlewb["uname"])
       
        # 保存结果
            tmp = pd.DataFrame(
                {
                 "SourceName": sourcename,
                 "SourceID": sourceid,
                 "NAME": name,
                 "ID": id
                 }
                )
            data = pd.concat((data, tmp), axis=0)  # 与之前结果合并
            data.to_csv(DATA_PATH, index=False, encoding="UTF-8")  # 写入文件
   
        # 随机sleep一段时间，防止爬取频率过高被封号
            time.sleep(random() * 2)  # 0~2秒随机sleep
        print("page:", page)

def main():#主函数,bfs爬取社交网络
    sourceperson = Person("刘守元", "1755748572")
    person_queue=[]
    person_queue.append(sourceperson)
    duplicate_check=set()
    duplicate_check.add(sourceperson.name)
    nowstep=10
    sourceperson.followers, sourceperson.followings = scrape_bilibili_personal_info(DATA_PATH_personal_information,sourceperson.mid,sourceperson.name)
    while len(person_queue )>0 and nowstep>=0:
        currentperson=person_queue.pop(0)
        currentperson.followers, currentperson.followings = scrape_bilibili_personal_info(DATA_PATH_personal_information,currentperson.mid,currentperson.name)
        if(currentperson.followings=="privacy"):
            continue
        page_number=math.ceil(int(currentperson.followings)/20)
        scrape_bilibili_followings(DATA_PATH_social_network, page_number, currentperson.name, currentperson.mid, person_queue,duplicate_check,nowstep)
        #print("current person:",currentperson.name)
        #print("queue length:",len(person_queue))
        #print("duplicate check length:",len(duplicate_check))
        time.sleep(random() * 2)  # 0~2秒随机sleep
        nowstep-=1
if __name__ == "__main__":
    main()
    print("over")
