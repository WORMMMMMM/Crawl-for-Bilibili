import json
import time
from random import random
from urllib.parse import urlencode

import pandas as pd
import requests

DATA_PATH="./bilibilitry.csv"
#是否要填写cookie以正常访问？
Cookie="buvid3=308F7EF7-2391-53B0-5CB7-EA7CB6D226FD11269infoc; b_nut=1692205111; _uuid=BD710C343-9144-344F-4D55-1CEC775DFC1E10900infoc; buvid4=C296ADD0-E87C-44A6-4CE1-B22A0C6E617911809-023081700-cWZGbE4cldrLhquQpQlk3Q%3D%3D; rpdid=|(k|k)J|YY)l0J'uYmkk|luuk; DedeUserID=512085467; DedeUserID__ckMd5=d4840e2a81268595; header_theme_version=CLOSE; buvid_fp_plain=undefined; LIVE_BUVID=AUTO9816925335295486; hit-new-style-dyn=1; hit-dyn-v2=1; enable_web_push=DISABLE; is-2022-channel=1; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; CURRENT_QUALITY=80; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; PVID=1; fingerprint=623acec7653de94b226112ebdc65f629; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTc4NTIxNDIsImlhdCI6MTcxNzU5Mjg4MiwicGx0IjotMX0.aATOhxi27Vgl4Yt4o3HFSXCA6wrp3hfJ4sopgC44xkE; bili_ticket_expires=1717852082; bp_t_offset_512085467=939578045117759513; SESSDATA=f4e76abf%2C1733224593%2Cfd237%2A62CjCm1FFdpLf6GJK9gw3nPB05B3UicKr2LfvSYBBGTH4bqjCBwgo5TK0ltKQIXsaM5c0SVlVUQ1dLYUxkZGxMQmVBZE1wVUlLSVNDZjhGU0d1dnI4MklzMmQ2amg2REo0ZGtMWmx1ZjVuNHg0STRzYTdGOTdkTk9BQzVqRnpTSElqeHNZUEszTEpBIIEC; bili_jct=3c53cb50426c6e36ff19b29218469ef4; buvid_fp=623acec7653de94b226112ebdc65f629; b_lsid=C271569C_18FF7567F46; bsource=search_bing; sid=4yx86sj6; home_feed_column=4; browser_resolution=843-935"

headers={
    "Accept":"*/*",
    "Accept-Encoding":"gzip,deflate,br,zstd",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection":"keep-alive",
    "Cookie":Cookie,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
}

#种子用户
seed_usr=["20918528"]

for p in range(1): #先尝试爬取50个用户 #TODO needs to be changed
    try:
        data = pd.read_csv(DATA_PATH)
    except:
        data = pd.DataFrame()

    #搭建客户端, #TODO offset needs to be changed
    params = {
        "mid":seed_usr,
        "token":"",
        "platform":"web",
        "web_location":"1550101",
        "dm_img_list":'[{"x":3400,"y":953,"z":0,"timestamp":3,"k":104,"type":0},{"x":3578,"y":1397,"z":24,"timestamp":66,"k":114,"type":0}]',
        "dm_img_str":"V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
        "dm_cover_img_str":"QU5HTEUgKEludGVsLCBJbnRlbChSKSBJcmlzKFIpIFhlIEdyYXBoaWNzICgweDAwMDA0NkE2KSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC",
        "dm_img_inter":'{"ds":[{"t":0,"c":"","p":[36,12,12],"s":[122,5354,920]}],"wh":[4256,3607,36],"of":[301,602,301]}',
        "w_rid":"44bd44cec323df5b834acb95238f332f",
        "wts":"1717847844"
    }
    #TODO langlang0614 needs to be changed
    url="https://api.bilibili.com/x/space/wbi/acc/info?" + urlencode(params)
    res = requests.get(url,headers=headers)
    data_json = json.loads(res.content)
    
    mid= data_json["data"]["mid"]
    birthday = data_json["data"]["birthday"]
    name = data_json["data"]["name"]
    title = data_json["data"]["official"]["title"]
    sign = data_json["data"]["sign"]
    sex = data_json["data"]["sex"]

    #爬取点赞数等信息
    params = {
        "vmid":str(seed_usr[p]),
        "web_location":"1550101",        
        "w_rid":"44bd44cec323df5b834acb95238f332f",
        "wts":"1717847844"
    }
    #TODO langlang0614 needs to be changed
    url="https://api.bilibili.com/x/relation/stat?" + urlencode(params)
    res = requests.get(url,headers=headers)
    data_json = json.loads(res.content)
    followings = data_json["data"]["following"]
    followers = data_json["data"]["follower"]

    params = {
        "mid":str(seed_usr[p]),
        "web_location":"333.999"
    }
    #TODO langlang0614 needs to be changed
    url="https://api.bilibili.com/x/space/upstat?" + urlencode(params)
    res = requests.get(url,headers=headers)
    data_json = json.loads(res.content)
    likes = data_json["data"]["likes"]
    plays = data_json["data"]["archive"]["view"]

    '''
    params = {
        "mid":str(seed_usr[p]),
        "ps":"30",
        "tid":"0",
        "special_type":"",
        "pn":"1",
        "keyword":"",
        "order":"click",
        "platform":"web",
        "web_location":"1550101",
        "dm_img_list":"[]",
        "dm_img_str":"V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
        "dm_cover_img_str":"QU5HTEUgKEludGVsLCBJbnRlbChSKSBJcmlzKFIpIFhlIEdyYXBoaWNzICgweDAwMDA0NkE2KSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC",
        "dm_img_inter":'{"ds":[{"t":2,"c":"Y2xlYXJmaXggZy1zZWFyY2ggc2VhcmNoLWNvbnRhaW5lcg","p":[1828,74,601],"s":[24,486,464]},{"t":2,"c":"d3JhcHBlcg","p":[825,59,1355],"s":[242,4221,3536]}],"wh":[4082,2979,92],"of":[353,706,353]}',
        "w_rid":"20292049e42832e1dcea8415d1422eb2",
        "wts":"1717850396"
    }
    #TODO langlang0614 needs to be changed
    url="https://api.bilibili.com/x/space/wbi/arc/search?" + urlencode(params)
    res = requests.get(url,headers=headers)
    data_json = json.loads(res.content)
    print(data_json)
    exit()
    for i in range(3):
        video = {"title":data_json["data"]["list"]["vlist"][i]["title"],"bvid":data_json["data"]["list"]["vlist"][i]["bvid"],"comment":data_json["data"]["list"]["vlist"][i]["comment"],
                 "play":data_json["data"]["list"]["vlist"][i]["play"],"comment":data_json["data"]["list"]["vlist"][i]["comment"],"description":data_json["data"]["list"]["vlist"][i]["description"]
                 }
        top3_views.append(video)
    

    #最多收藏，区别在于order
    params = {
        "mid":str(seed_usr[p]),
        "ps":"30",
        "tid":"0",
        "special_type":"",
        "pn":"1",
        "keyword":"",
        "order":"stow",
        "platform":"web",
        "web_location":"1550101",
        "dm_img_list":"[]",
        "dm_img_str":"V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
        "dm_cover_img_str":"QU5HTEUgKEludGVsLCBJbnRlbChSKSBJcmlzKFIpIFhlIEdyYXBoaWNzICgweDAwMDA0NkE2KSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC",
        "dm_img_inter":'{"ds":[{"t":2,"c":"Y2xlYXJmaXggZy1zZWFyY2ggc2VhcmNoLWNvbnRhaW5lcg","p":[1828,74,601],"s":[24,486,464]},{"t":2,"c":"d3JhcHBlcg","p":[825,59,1355],"s":[242,4221,3536]}],"wh":[4082,2979,92],"of":[353,706,353]}',
        "w_rid":"20292049e42832e1dcea8415d1422eb2",
        "wts":"1717850396"
    }
    #TODO langlang0614 needs to be changed
    url="https://api.bilibili.com/x/space/wbi/arc/search?" + urlencode(params)
    res = requests.get(url,headers=headers)
    data_json = json.loads(res.content)
    for i in range(3):
        video = {"title":data_json["data"]["list"]["vlist"][i]["title"],"bvid":data_json["data"]["list"]["vlist"][i]["bvid"],"comment":data_json["data"]["list"]["vlist"][i]["comment"],
                 "play":data_json["data"]["list"]["vlist"][i]["play"],"comment":data_json["data"]["list"]["vlist"][i]["comment"],"description":data_json["data"]["list"]["vlist"][i]["description"]
                 }
        top3_likes.append(video)
    '''
    
    tmp = pd.DataFrame(
        {
            "mid":mid,#用户id
            "sex":sex,#用户性别
            "name":name,#用户昵称
            "followings":followings,#关注人数
            "followers":followers,#粉丝数量
            "likes":likes,#点赞数
            "plays":plays,#播放数
            "intro":introduction,#个人介绍
            "level":level,#等级
            "birth":birthday,#生日
            "sign":sign,#签名
            "title":title,#官方认证
        }
    )
    print(followings)
    '''
    "top3_likes":top3_likes,#最多收藏
    "top3_views":top3_views#最多播放
    '''
    data = pd.concat((data, tmp), axis=0)  # 与之前结果合并
    
    data.to_csv(DATA_PATH, index=False, encoding="UTF-8")  # 写入文件