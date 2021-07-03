from google.protobuf.json_format import MessageToJson, Parse
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
import dm_pb2
import myhtml

def createDatalist(datestart, dateend=None):
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')
    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=+1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    return date_list

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64",
    'Cookie': "_uuid=208B301F-786B-1E0B-902F-2CD4198A925706079infoc; buvid3=E38961E8-FAE3-4D04-93C9-52409EA0824534758infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(klY~ukYuJm0J'uYkulmmRJR; buvid_fp=E38961E8-FAE3-4D04-93C9-52409EA0824534758infoc; SESSDATA=fc746865%2C1637151493%2Cdca9d%2A51; bili_jct=16a5f32376347ecbc36121747c2b28ef; DedeUserID=476056253; DedeUserID__ckMd5=84365a35da043136; sid=7q9haodl; fingerprint=a918db7b096efdf26df9e2e5e5bf95d8; buvid_fp_plain=F4A56341-4EE6-456C-8F6B-D3F6D7B1B87813414infoc; PVID=4; CURRENT_QUALITY=120; bfe_id=393becc67cde8e85697ff111d724b3c8"
}

def getDanmuHistory(url):
    try:
        danmu = requests.get(url, headers=headers)
        DM = dm_pb2.DmSegMobileReply()
        DM.ParseFromString(danmu.content)
        danmu = MessageToJson(DM)
        danmuobj = json.loads(danmu)
        return danmuobj
    except all:
        return []


def getDanmuHistoryRange(cid, start):
    ans = []
    for time in createDatalist(start):
        url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid='+cid+'&date='+time
        ans += getDanmuHistory(url)
        print(time)
    return ans


def getCidByBid(queryBid):
    urlGetCid = "https://api.bilibili.com/x/player/pagelist?bvid=" + \
        queryBid + "&jsonp=jsonp"
    strCidJson = myhtml.getRequestsContentUtf8(urlGetCid)
    jsonCid = json.loads(strCidJson)
    print(jsonCid["data"])
    return str(jsonCid["data"][0]["cid"])


if __name__ == '__main__':
    bid = "BV16K4y1h7eq"
    cid = getCidByBid(bid)
    ans = getDanmuHistoryRange(cid, '2021-05-01')
    with open("output.json","w") as f:
        f.write(json.dumps(ans))