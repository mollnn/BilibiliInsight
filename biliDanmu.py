import json
import re
import json
import time
import threading

import myhtml
import biliSearch

def saveDanmuList(list, filename, bid):
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


def getDanmuByCid(queryCid):
    urlDanmuXml = 'https://comment.bilibili.com/'+queryCid+'.xml'
    strDanmuXml = myhtml.getRequestsContentUtf8(urlDanmuXml)
    return strDanmuXml


def getCidByBid(queryBid):
    urlGetCid = "https://api.bilibili.com/x/player/pagelist?bvid=" + \
        queryBid + "&jsonp=jsonp"
    strCidJson = myhtml.getRequestsContentUtf8(urlGetCid)
    jsonCid = json.loads(strCidJson)
    print(jsonCid["data"])
    return str(jsonCid["data"][0]["cid"])


def getDanmuByBid(queryBid):
    queryCid = getCidByBid(queryBid)
    return getDanmuByCid(queryCid)

def getDanmuByBids(listBid):
    print(listBid)
    for itemBid in listBid:
        saveDanmuList(getDanmuByBid(itemBid), 'outputdanmu/' +
                      itemBid+'.danmu.json', itemBid)
    print("Thread finish")


if __name__ == "__main__":
    threadHandles = []
    timeStart = time.time()
    for page in range(1,5):
        listBid = biliSearch.getBidsBySearch("老番茄", page)
        listBid = list(set(listBid))
        # GetDanmuByBids(listBid)
        threadHandles += [threading.Thread(target=getDanmuByBids,
                                           name="Thread "+str(page), args=(listBid,))]
    for threadHandle in threadHandles:
        threadHandle.start()
    print("all start")
    for threadHandle in threadHandles:
        threadHandle.join()
    timeEnd = time.time()
    print("timeused: ", timeEnd-timeStart)
