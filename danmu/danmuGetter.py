import json
import re
import requests
import json

def GetHTMLContent(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.content.decode("utf-8")

def SaveDanmuList(list, cid):
    strsDanmu = re.compile(r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)">(.*?)</d>')
    listDanmu = re.findall(strsDanmu, list)
    fileOutput = open("output.json", "w", encoding="utf-8")
    for itemDanmu in listDanmu:
        dictItemDanmu={}
        dictItemDanmu["cid"]=cid
        dictItemDanmu["time"]=itemDanmu[0]
        dictItemDanmu["mode"]=itemDanmu[1]
        dictItemDanmu["size"]=itemDanmu[2]
        dictItemDanmu["color"]=itemDanmu[3]
        dictItemDanmu["timestamp"]=itemDanmu[4]
        dictItemDanmu["pool"]=itemDanmu[5]
        dictItemDanmu["author"]=itemDanmu[6]
        dictItemDanmu["rowid"]=itemDanmu[7]
        dictItemDanmu["text"]=itemDanmu[8]
        strjsonItemDanmu=json.dumps(dictItemDanmu, ensure_ascii=False)
        fileOutput.write(strjsonItemDanmu)
        fileOutput.write("\n")
    fileOutput.close()

def GetDanmuByCid(queryCid):
    urlDanmuXml = 'https://comment.bilibili.com/'+queryCid+'.xml'
    strDanmuXml = GetHTMLContent(urlDanmuXml)
    SaveDanmuList(strDanmuXml, queryCid)

def GetCidByBid(queryBid):
    urlGetCid = "https://api.bilibili.com/x/player/pagelist?bvid=" + queryBid + "&jsonp=jsonp"
    strCidJson = GetHTMLContent(urlGetCid)
    jsonCid = json.loads(strCidJson)
    return str(jsonCid["data"][0]["cid"])

def GetDanmuByBid(queryBid):
    queryCid=GetCidByBid(queryBid)
    GetDanmuByCid(queryCid)

if __name__ == "__main__":
    GetDanmuByBid("BV1Aa4y1a7HP")
    print("Succeed :)")