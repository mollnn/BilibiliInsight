import os
import re
import json

import myhtml



def GetMP4ByBid(video_id, ffmpeg_config="-c:v copy -c:a aac -strict experimental"):
    pageUrl = "https://www.bilibili.com/video/" + video_id
    htmlText = myhtml.GetRequestsText(pageUrl, pageUrl)
    urlJson = json.loads(re.findall(
        '<script>window\.__playinfo__=(.*?)</script>', htmlText)[0])

    videoUrl = urlJson['data']['dash']['video'][0]['backupUrl'][0]
    audioUrl = urlJson['data']['dash']['audio'][0]['backupUrl'][0]

    print("Downloading...")

    audioFile = myhtml.GetRequestsContent(audioUrl, pageUrl)
    with open('temp/audio_'+video_id+'.mp3', 'wb') as f:
        f.write(audioFile)
    videoFile = myhtml.GetRequestsContent(videoUrl, pageUrl)
    with open('temp/video_'+video_id+'.mp4', 'wb') as f:
        f.write(videoFile)

    os.system('ffmpeg -y -i temp/video_'+video_id+'.mp4 -i temp/audio_' +
              video_id+'.mp3 ' + ffmpeg_config + ' output/'+video_id+'.mp4')
    print("Succeed! :)")

    # 此处还应当删除临时文件


GetMP4ByBid("BV1sk4y1k73b")
