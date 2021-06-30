import json
import re
import requests
import json
import time
import threading


def GetHTMLContent(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.content.decode("utf-8")


def SaveDanmuList(list, cid):
    reDanmu = re.compile(
        r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)">(.*?)</d>')
    listDanmu = re.findall(reDanmu, list)
    fileOutput = open("output/"+cid+".json", "w", encoding="utf-8")
    listDictDanmu = []
    for itemDanmu in listDanmu:
        dictItemDanmu = {}
        dictItemDanmu["cid"] = cid
        dictItemDanmu["time"] = itemDanmu[0]
        dictItemDanmu["mode"] = itemDanmu[1]
        dictItemDanmu["size"] = itemDanmu[2]
        dictItemDanmu["color"] = itemDanmu[3]
        dictItemDanmu["timestamp"] = itemDanmu[4]
        dictItemDanmu["pool"] = itemDanmu[5]
        dictItemDanmu["author"] = itemDanmu[6]
        dictItemDanmu["rowid"] = itemDanmu[7]
        dictItemDanmu["text"] = itemDanmu[8]
        listDictDanmu += [dictItemDanmu]
    jsonDictDanmu = json.dumps(listDictDanmu)
    fileOutput.write(json.dumps(listDictDanmu, ensure_ascii=False,
                     sort_keys=True, indent=4, separators=(',', ':')))
    fileOutput.close()


def GetDanmuByCid(queryCid):
    urlDanmuXml = 'https://comment.bilibili.com/'+queryCid+'.xml'
    strDanmuXml = GetHTMLContent(urlDanmuXml)
    SaveDanmuList(strDanmuXml, queryCid)


def GetCidByBid(queryBid):
    urlGetCid = "https://api.bilibili.com/x/player/pagelist?bvid=" + \
        queryBid + "&jsonp=jsonp"
    strCidJson = GetHTMLContent(urlGetCid)
    jsonCid = json.loads(strCidJson)
    return str(jsonCid["data"][0]["cid"])


def GetDanmuByBid(queryBid):
    queryCid = GetCidByBid(queryBid)
    GetDanmuByCid(queryCid)


def GetBidsBySearch(searchKeyword, page=1):
    urlSearch = "https://search.bilibili.com/all?keyword=" + \
        searchKeyword+"&from_source=web_search&page=" + str(page)
    htmlSearch = GetHTMLContent(urlSearch)
    reBid = re.compile(r'//www.bilibili.com/video/(.*?)\?from=search')
    listBid = re.findall(reBid, htmlSearch)
    return listBid


def GetDanmuByBids(listBid):
    for itemBid in listBid:
        GetDanmuByBid(itemBid)
    print("Thread finish")


if __name__ == "__main__":
    threadHandles = []
    timeStart = time.time()
    for page in range(1, 10):
        listBid = GetBidsBySearch("记忆碎片", page)
        # GetDanmuByBids(listBid)
        threadHandles += [threading.Thread(target=GetDanmuByBids,
                                           name="Thread "+str(page), args=(listBid,))]
    for threadHandle in threadHandles:
        threadHandle.start()
    for threadHandle in threadHandles:
        threadHandle.join()
    timeEnd = time.time()
    print("timeused: ", timeEnd-timeStart)
