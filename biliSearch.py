import re

import myhtml


def getBidsBySearch(searchKeyword, page=1):
    urlSearch = "https://search.bilibili.com/all?keyword=" + \
        searchKeyword+"&from_source=web_search&page=" + str(page)
    htmlSearch = myhtml.getRequestsContentUtf8(urlSearch)
    reBid = re.compile(r'//www.bilibili.com/video/(.*?)\?from=search')
    listBid = re.findall(reBid, htmlSearch)
    return listBid