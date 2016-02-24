import os, sys, subprocess, json, datetime
from shutil import copyfile

# Library functions

# http://stackoverflow.com/a/27168937/2234742
def iso8601(value):
    # split seconds to larger units
    seconds = value.total_seconds()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    days, hours, minutes = map(int, (days, hours, minutes))
    seconds = round(seconds, 6)

    ## build date
    date = ''
    if days:
        date = '%sD' % days

    ## build time
    time = u'T'
    # hours
    bigger_exists = date or hours
    if bigger_exists:
        time += '{:02}H'.format(hours)
    # minutes
    bigger_exists = bigger_exists or minutes
    if bigger_exists:
      time += '{:02}M'.format(minutes)
    # seconds
    if seconds.is_integer():
        seconds = '{:02}'.format(int(seconds))
    else:
        # 9 chars long w/leading 0, 6 digits after decimal
        seconds = '%09.6f' % seconds
    # remove trailing zeros
    seconds = seconds.rstrip('0')
    time += '{}S'.format(seconds)
    return u'P' + date + time

# Video Resolutions

video_extensions = ['webm', 'mkv', 'flv', 'ogv', 'gifv', 'avi', 'mov', 'wmv', 'rm', 'rmvb', 'mp4', 'm4p', 'm4v', 'mpg', 'mpeg', '3gp', '3g2']

input_dir = "./"

input_files = []
for file in os.listdir(input_dir):
    for ext in video_extensions:
        if file.endswith("." + ext):
            print("Found input file: " + file)
            input_files.append(file)

resolutions = {
    '360p': { 'resolution': 360, 'video_bitrate_kb': 1000, 'audio_bitrate_kb': 128 },
    '480p': { 'resolution': 480, 'video_bitrate_kb': 1500, 'audio_bitrate_kb': 128 },
    '720p': { 'resolution': 720, 'video_bitrate_kb': 2500, 'audio_bitrate_kb': 192 },
    '1080p': { 'resolution': 1080, 'video_bitrate_kb': 4000, 'audio_bitrate_kb': 192 }
}

# Perform transcode

final_res_descriptor = {}

for filename in input_files:
    filename_no_ext = "".join(filename.split(".").pop(0))
    native_res = int(subprocess.check_output("mediainfo '--Inform=Video;%Height%' " + filename, shell=True));
    duration_ms = float(subprocess.check_output("mediainfo '--Inform=Video;%Duration%' " + filename, shell=True));
    duration_s = duration_ms / 1000
    output_resolutions = []
    print("Transcoding " + filename + " which has resolution " + str(native_res) + "p:");
    for res in resolutions:
        opts = resolutions[res]
        if opts["resolution"] > native_res:
            print(str(opts["resolution"]) + " is larger than native resolution. Skipping..")
            continue
        # Output MP4
        output_path = "../video/" + filename_no_ext + "-" + res + ".mp4"
        print("Outputting MP4 at " + res + "..")
        if os.path.exists(output_path):
            print("Output file already exists. Skipping..")
        else:
            ffmpeg_call = "ffmpeg -i " + filename + " -codec:v libx264 -profile:v high -preset slow -b:v " + str(opts["video_bitrate_kb"]) + "k -maxrate " + str(opts["video_bitrate_kb"]) + "k -bufsize " + str(2 * opts["video_bitrate_kb"]) + "k -vf scale=-1:" + str(opts["resolution"]) + " -threads 0 -codec:a libfdk_aac -b:a " + str(opts["audio_bitrate_kb"]) + "k " + output_path
            print(ffmpeg_call)
            subprocess.call(ffmpeg_call, shell=True)
        # Output VP9
        output_path = "../video/" + filename_no_ext + "-" + res + ".webm"
        print("Outputting WEBM at " + res + "..")
        if os.path.exists(output_path):
            print("Output file already exists. Skipping..")
        else:
            ffmpeg_call = "ffmpeg -i " + filename + " -codec:v libvpx-vp9 -preset slow -b:v " + str(opts["video_bitrate_kb"]) + "k -vf scale=-1:" + str(opts["resolution"]) + " -threads 0 -codec:a libvorbis -b:a " + str(opts["audio_bitrate_kb"]) + "k " + output_path
            print(ffmpeg_call)
            subprocess.call(ffmpeg_call, shell=True)
        # Cleanup
        output_resolutions.append(opts["resolution"])
    # Output large thumbnail for video
    output_path = "../video/" + filename_no_ext + ".jpg"
    print("Outputting full-size thumbnail..")
    if os.path.exists(output_path):
        print("Output file already exists. Skipping..")
    else:
        input_path = "../source_video/" + filename_no_ext + ".jpg"
        if os.path.exists(input_path):
            print("Copying custom thumbnail")
            copyfile(input_path, output_path)
        else:
            # Auto-generate thumbnail
            ffmpeg_call = "ffmpeg -i " + filename + " -ss " + str(duration_s / 2) + " -vframes 1 "  + output_path
            print(ffmpeg_call)
            subprocess.call(ffmpeg_call, shell=True)
    # Output small thumbnail for video
    output_path = "../video/" + filename_no_ext + "-small.jpg"
    print("Outputting small thumbnail..")
    if os.path.exists(output_path):
        print("Output file already exists. Skipping..")
    else:
        input_path = "../source_video/" + filename_no_ext + ".jpg"
        if os.path.exists(input_path):
            print("Processing custom thumbnail")
            ffmpeg_call = "ffmpeg -i " + input_path + " -vf scale=120:68 "  + output_path
            print(ffmpeg_call)
            subprocess.call(ffmpeg_call, shell=True)
        else:
            # Auto-generate thumbnail
            ffmpeg_call = "ffmpeg -i " + filename + " -ss " + str(duration_s / 2) + " -vframes 1 -vf scale=120:68 "  + output_path
            print(ffmpeg_call)
            subprocess.call(ffmpeg_call, shell=True)
    # Output resolution descriptor for this video
    output_preferred_res = subprocess.check_output("mediainfo '--Inform=Video;%Width%,%Height%' " + "../video/" + filename_no_ext + "-" + str(output_resolutions[0]) + "p.mp4", shell=True)
    output_res_dims = list(map(int, output_preferred_res.replace("\n", "").split(",")))
    print("OUTPUT RES: " + str(output_res_dims))
    # print("Resolution descriptor: " + output_res_dims)
    final_res_descriptor[filename_no_ext] = {'resolutions': output_resolutions, 'duration_ms': duration_ms, 'duration_iso8601': iso8601(datetime.timedelta(milliseconds=duration_ms)), 'preferred_resolution_dims': {'w': output_res_dims[0], 'h': output_res_dims[1]}}
    
res_desc = open("../_data/resolutions.json", "w")
res_desc.write(json.dumps(final_res_descriptor))
res_desc.close()
        
print('All videos converted');

#TODO: Output and optimize thumbnails if they don't exist, nothing if they do

