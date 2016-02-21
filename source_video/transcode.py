import os, subprocess

# Video Resolutions

video_files = ['my-first-video.mp4']

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

for filename in video_files:
    filename_no_ext = "".join(filename.split(".").pop(0))
    native_res = int(subprocess.check_output("mediainfo '--Inform=Video;%Height%' " + filename, shell=True));
    print("Transcoding " + filename + " which has resolution " + str(native_res) + "p:");
    for res in resolutions:
        opts = resolutions[res]
        if (opts["resolution"] >= native_res):
            print(str(opts["resolution"]) + " is equal or larger than native resolution. Skipping..")
            continue
        print("Outputting at " + res + "..")
        ffmpeg_call = "ffmpeg -i " + filename + " -codec:v libx264 -profile:v high -preset slow -b:v " + str(opts["video_bitrate_kb"]) + "k -maxrate " + str(opts["video_bitrate_kb"]) + "k -bufsize " + str(2 * opts["video_bitrate_kb"]) + "k -vf scale=-1:" + str(opts["resolution"]) + " -threads 0 -codec:a libfdk_aac -b:a " + str(opts["audio_bitrate_kb"]) + "k ../video/" + filename_no_ext + "-" + res + ".mp4"
        print(ffmpeg_call)
        subprocess.call(ffmpeg_call, shell=True)
        
print('All videos converted');

#TODO
# 1) Process all files in the source videos directory
# 2) Output and optimize thumbnails if they don't exist, nothing if they do
# 3) Create a description .yaml so that the main app knows which resolutions of each video exist

