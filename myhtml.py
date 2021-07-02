import requests


def GetRequestsContentUtf8(url, referee=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).content.decode("utf-8")


def GetRequestsText(url, referee=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).text


def GetRequestsContent(url, referee=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).content