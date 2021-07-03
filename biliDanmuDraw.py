import json
from os import read
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.stride_tricks import DummyArray
import ffmpeg
import math

import biliDanmu
import biliMedia


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
                ans[i] += 1/Delta
    return ans


if __name__ == '__main__':
    bid = "BV16K4y1h7eq"

    biliDanmu.saveDanmuByBid(bid)
    # biliMedia.getMP4ByBid(bid)

    danmu_list = readDanmuList(bid)
    duration = getMediaDuration(bid)
    ans = calcDanmuDensity(danmu_list, duration)

    print(ans)
    plt.plot(ans)
    plt.show()
