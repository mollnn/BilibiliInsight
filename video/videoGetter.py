import os
import sys
import requests
import re
import json

def GetRequestsText(url, referee):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).text

def GetRequestsContent(url, referee):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).content

def GetMP4ByBid(video_id):
    pageUrl = "https://www.bilibili.com/video/" + video_id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': pageUrl
    }
    htmlText = GetRequestsText(pageUrl, pageUrl)
    urlJson = json.loads(re.findall('<script>window\.__playinfo__=(.*?)</script>', htmlText)[0])
    print("finish get av url")
    videoUrl = urlJson['data']['dash']['video'][0]['backupUrl'][0]
    audioUrl = urlJson['data']['dash']['audio'][0]['backupUrl'][0]
    audioFile = GetRequestsContent(audioUrl, pageUrl)
    print("finish get audio file")
    with open('temp/audio.mp3', 'wb') as f:
        f.write(audioFile)
    videoFile = GetRequestsContent(videoUrl, pageUrl)
    print("finish get video file")
    with open('temp/video.mp4', 'wb') as f:
        f.write(videoFile)
    os.system('ffmpeg -y -i temp/video.mp4 -i temp/audio.mp3 -c:v copy -c:a aac -strict experimental output/'+video_id+'.mp4')
    print("Succeed! :)")

GetMP4ByBid("BV1rs411s7Ur")