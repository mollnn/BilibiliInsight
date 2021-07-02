import json
import re
import json
import time
import threading

import myhtml
import biliSearch

def SaveDanmuList(list, filename, bid):
    reDanmu = re.compile(
        r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)">(.*?)</d>')
    listDanmu = re.findall(reDanmu, list)
    fileOutput = open(filename, "w", encoding="utf-8")
    listDictDanmu = []
    for itemDanmu in listDanmu:
        dictItemDanmu = {}
        dictItemDanmu["bid"] = bid
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
    strDanmuXml = myhtml.GetRequestsContentUtf8(urlDanmuXml)
    return strDanmuXml


def GetCidByBid(queryBid):
    urlGetCid = "https://api.bilibili.com/x/player/pagelist?bvid=" + \
        queryBid + "&jsonp=jsonp"
    strCidJson = myhtml.GetRequestsContentUtf8(urlGetCid)
    jsonCid = json.loads(strCidJson)
    print(jsonCid["data"])
    return str(jsonCid["data"][0]["cid"])


def GetDanmuByBid(queryBid):
    queryCid = GetCidByBid(queryBid)
    return GetDanmuByCid(queryCid)

def GetDanmuByBids(listBid):
    print(listBid)
    for itemBid in listBid:
        SaveDanmuList(GetDanmuByBid(itemBid), 'outputdanmu/' +
                      itemBid+'.danmu.json', itemBid)
    print("Thread finish")


if __name__ == "__main__":
    threadHandles = []
    timeStart = time.time()
    for page in range(1,2):
        listBid = biliSearch.GetBidsBySearch("老番茄", page)
        listBid = list(set(listBid))
        # GetDanmuByBids(listBid)
        threadHandles += [threading.Thread(target=GetDanmuByBids,
                                           name="Thread "+str(page), args=(listBid,))]
    for threadHandle in threadHandles:
        threadHandle.start()
    print("all start")
    for threadHandle in threadHandles:
        threadHandle.join()
    timeEnd = time.time()
    print("timeused: ", timeEnd-timeStart)
