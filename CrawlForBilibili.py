import json
import time
from random import random
from urllib.parse import urlencode

import pandas as pd
import requests
#定义一个Person类，用来存储人的信息
class Person:
    def __init__(self, name, mid):
        self.name = name
        self.mid = mid

DATA_PATH_personal_information = "./personal_information.csv"
DATA_PATH_social_network = "./social_network.csv"
# TODO: 根据分析结果，构建Headers
Cookie = "buvid3=A1F0E047-AE95-D788-A1DC-61A5D8340A1495364infoc; b_nut=1714019595; _uuid=E1A7599C-F9BA-F73F-963F-2F5EFB5A578394039infoc; enable_web_push=DISABLE; buvid4=DCD806D9-5143-7DCC-8D96-65F6E0EB4D4F76556-024030614-N93wYaw5nav0jnXIG8Zldg%3D%3D; CURRENT_FNVAL=4048; rpdid=|(J|)ulRlulm0J'u~uR|umYJR; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; PVID=3; CURRENT_QUALITY=80; buvid_fp_plain=undefined; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgwMzU5ODksImlhdCI6MTcxNzc3NjcyOSwicGx0IjotMX0.0m4SkimqzFO72LKoK0OBxnpPb5-krxLR04k9BZpQQbA; bili_ticket_expires=1718035929; SESSDATA=788d938d%2C1733328789%2C4f9b5%2A61CjDhlGK2Eq-ZBXjL7PtZtratPuoDcvIA6eQvtknHJbeV_D6JuNMfsSszIHH77eTeyZcSVm5aQTVTVlA3VE53MWc1VTRzVG1pVTBSQWhHLWZMaVpEa2xuYmtyMWh3c3NoUVBXTndmcXoxbWo4YWMwMDRkcWQtZWhUVWp3V09ReGFJcHJvb1pqZXVnIIEC; bili_jct=5943a61699a10ed491e2cfa5dc637487; DedeUserID=89627183; DedeUserID__ckMd5=261642d5b9251dcd; b_lsid=B9DF72510_18FF75A95FC; fingerprint=e6114bd0f8bdde0d871819cc3065c55c; buvid_fp=e6114bd0f8bdde0d871819cc3065c55c; sid=73sgkwcx; bp_t_offset_89627183=940612784316481657; home_feed_column=5; browser_resolution=1488-742"
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
                "vmid": "652239032",
                "ps": "20",
                "order": "desc",
                "gaia_source": "main_web",
                "web_location": "333.999"
            }
        else:
            params = {
                "pn": page,
                "page_type": "searchall",
                "vmid": "652239032",
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
                #print(singlewb["uname"])
       
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
    sourceperson = Person("IGN中国", "652239032")
    person_queue=[]
    person_queue.append(sourceperson)
    duplicate_check=set()
    duplicate_check.add(sourceperson.name)
    nowstep=10
    while len(person_queue)>0:
        currentperson=person_queue.pop(0)
        scrape_bilibili_followings(DATA_PATH_social_network, 1, currentperson.name, currentperson.mid, person_queue,duplicate_check,nowstep)
        #print("current person:",currentperson.name)
        #print("queue length:",len(person_queue))
        #print("duplicate check length:",len(duplicate_check))
        time.sleep(random() * 2)  # 0~2秒随机sleep
        nowstep-=1
if __name__ == "__main__":
    main()
    print("over")
