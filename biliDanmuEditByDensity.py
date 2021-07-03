import math
import ffmpeg
import json
import matplotlib.pyplot as plt

import biliDanmu
import biliMedia
import myMediaEdit


def readDanmuList(bid):
    with open("outputdanmu/{bid}.danmu.json".format(bid=bid), "r", encoding="utf-8") as f:
        str_danmu = f.read()
    return json.loads(str_danmu)


def getMediaDuration(bid):
    duration = ffmpeg.probe(
        "output/{bid}.mp4".format(bid=bid))["format"]["duration"]
    return duration


def calcDanmuDensity(danmu_list, duration, Delta=10):
    lim = int(math.ceil(float(duration)))
    ans = [0]*lim
    for i in range(lim):
        for danmu in danmu_list:
            if abs(float(danmu["time"])-i) < Delta/2:
                ans[i] += 1/min(i+1, lim-i, Delta)
    return ans


if __name__ == '__main__':
    bid = "BV1ds411k74N"
    # biliDanmu.saveDanmuByBid(bid)
    # biliMedia.getMP4ByBid(bid)

    danmu_list = readDanmuList(bid)
    duration = getMediaDuration(bid)

    density1 = calcDanmuDensity(danmu_list, duration, Delta=15)
    density2 = calcDanmuDensity(danmu_list, duration, Delta=60)

    ratio = [(density1[i]/(density2[i]+1e-6)) for i in range(len(density1))]

    print(ratio)
    plt.plot(ratio)
    plt.show()

    T=1.2
    hot_times = [i for i in range(len(ratio)) if ratio[i]>T]

    clip_desc_list = []
    for i in hot_times:
        clip_desc_list+=[{"filename":"output/{bid}.mp4".format(bid=bid),"start":i,"duration":1}];
    
    print(clip_desc_list)
    myMediaEdit.edit(clip_desc_list,"output_edit/editByDensity.mp4")