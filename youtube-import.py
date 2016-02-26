import os, sys, subprocess, json, datetime
from shutil import copyfile

DEBUG = False

if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " input_dir output_dir")
    exit()

input_dir = sys.argv[1]
output_dir = sys.argv[2]

json_data = []

input_files = []
for file in os.listdir(input_dir):
    if file.endswith(".json"):
        with open(input_dir + "/" + file) as json_desc:
            json_data.append(json.load(json_desc))
        print("Imported input descriptor: " + file)
        #if os.path.exists(video_filename):
        #    print("Found input video: " + video_filename)
        #    filenames_no_ext.append(filename_no_ext)
        #else:
        #    print("No matching input video.")
