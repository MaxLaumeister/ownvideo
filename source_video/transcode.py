import os, sys, subprocess, json

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

# Prepare output directory

if not os.path.exists('output'):
    os.makedirs('output')

# Perform transcode

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
        ffmpeg_call = "ffmpeg -i " + filename + " -ss " + str(duration_s / 2) + " -vframes 1 "  + output_path
        print(ffmpeg_call)
        subprocess.call(ffmpeg_call, shell=True)
    # Output small thumbnail for video
    output_path = "../video/" + filename_no_ext + "-small.jpg"
    print("Outputting small thumbnail..")
    if os.path.exists(output_path):
        print("Output file already exists. Skipping..")
    else:
        ffmpeg_call = "ffmpeg -i " + filename + " -ss " + str(duration_s / 2) + " -vframes 1 -vf scale=120:68 "  + output_path
        print(ffmpeg_call)
        subprocess.call(ffmpeg_call, shell=True)
    # Output resolution descriptor for this video
    res_descriptor = json.dumps({"resolutions": output_resolutions})
    print("Resolution descriptor: " + res_descriptor)
    f = open("../video/" + filename_no_ext + "-resolutions.json", "w")
    f.write(res_descriptor)
    f.close()
        
print('All videos converted');

#TODO: Output and optimize thumbnails if they don't exist, nothing if they do

