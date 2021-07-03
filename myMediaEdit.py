import ffmpeg
import json


def edit(clip_desc_list, output_filename):
    # clip_desc_list is a list of dict{'filename'=?, 'start'=?, 'duration'=?}
    clip_list = []
    for clip_desc in clip_desc_list:
        clip = ffmpeg.input(
            clip_desc["filename"], ss=clip_desc["start"], t=clip_desc["duration"])
        clip_list += [clip]
    print(clip_list)
    ans = clip_list[0]
    for i in range(1, len(clip_list)):
        ans = ffmpeg.concat(ans, clip_list[i])
    ans.output(output_filename).run(quiet=False, overwrite_output=True)


if __name__ == '__main__':
    bid = "BV16K4y1h7eq"
    media_filename = "output/{bid}.mp4".format(bid=bid)
    edit([{"filename": media_filename, "start": 0, "duration": 1}, {
        "filename": media_filename, "start": 10, "duration": 1}, {"filename": media_filename, "start": 20, "duration": 1}], "output_edit/1.mp4")
