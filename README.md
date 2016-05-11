# OwnVideo Jekyll Theme

OwnVideo is a free [Jekyll](https://jekyllrb.com/) theme that lets you Host Your Own Video! In the OwnVideo theme, every Jekyll "post" is a video, and like most video sharing sites, each video has its own "watch" page that puts that video front-and-center.

OwnVideo was created with user control in mind. If you upload videos to a video sharing service, they can be taken down by copyright claims and takedown requests. In some cases the large video sharing services have been known to take down videos that receive complaints just to be safe, even if there is no copyright infringement! OwnVideo bypasses video sharing sites and lets you control your videos on your own domain, on your own terms.

## Features
  - Full-fledged video "watch" pages with multiple video qualities, share buttons, and optional integrated Disqus comments
  - Custom playlist and custom thumbnail support
  - Automatic video conversion using FFmpeg (via included Python script) for full browser video compatibility
  - Mobile-first responsive design
  - Host your video files on a separate domain - for example, your site can be hosted on GitHub pages, but serve its video files from Amazon S3.
  - Automatic creation of Structured Data and OpenGraph tags, so your videos look great in search engine results
  - Uses the Jekyll static site templating system, so no backend (server-side) code is required

## Demo

Please check out my site [MusicalWolfe.com](https://www.musicalwolfe.com/) to see an instance of OwnVideo running with some of my videos.

## Installing OwnVideo

Ownvideo does video conversion, so it's a little more involved than most Jekyll themes. The installation and build steps assume that you have some experience with Jekyll and the general workflow of building a Jekyll site.

### Prerequisites

1. [**Jekyll**](https://jekyllrb.com/) version 3 or later. For how to install Jekyll, see the page on [Installing Jekyll](https://jekyllrb.com/docs/installation/).
2. [**Python 2.7**](https://www.python.org/). This is used for the video conversion script. If you're using Ubuntu you can run `sudo apt-get install python`.
3. [**FFmpeg**](https://www.ffmpeg.org/). The video conversion script uses this to convert your video files to web-streamable formats and resolutions. For how to install FFmpeg on Ubuntu, please see [this AskUbuntu thread](https://askubuntu.com/questions/432542/is-ffmpeg-missing-from-the-official-repositories-in-14-04)
4. [**MediaInfo**](https://mediaarea.net/en/MediaInfo). The video conversion script uses this to extract video metadata from your video files. If you're using Ubuntu you can run `sudo apt-get install mediainfo`.

### Building the Sample Site

1. Clone or download this GitHub repository, which contains the sample site.
2. `cd` into the `source_video` directory and run `python ./transcode.py`. This will use `ffmpeg` and `mediainfo` to transcode all of the source videos into web-streamable formats and resolutions.
3. `cd` into the main directory and run `jekyll serve`. You should be able to view the built sample site at http://localhost:4000/.

### Building Your Own Site

In OwnVideo, every video has a `video id`. A `video id` in OwnVideo is similar in concept to a YouTube video id - it's an immutable string that is used as a unique identifier for a video, and it serves as that video's custom URL. When building your own OwnVideo site, the most important thing to note is to always use the same `video id` to refer to a specific video. Unlike on YouTube, instead of being a random string, a video id can be a custom slug based on the title of the video it represents.

#### Folder Structure

The following folders are important moving parts of the OwnVideo Jekyll theme:

* `source_video` - The source_video folder is where you will put all of the videos you want to post to your OwnVideo site. Every video file name should be in the format `video-id.ext`, where `video-id` is the unique video id of the video, and `ext` is one of any common video extensions such as `mp4`, `avi`, `wmv`, etc.. If you have any custom thumbnails, they should be named `video-id.jpg`, and ideally be in the same resolution as the source video.

* `_posts` - The posts folder is where the metadata for the videos goes, such as titles and video descriptions. The post filenames should be in the format `YYYY-MM-DD-video-id.markdown`. The front-matter should contain the video `title`, the `video-id`, the `categories` (playlists) that the video is a part of, and the `date` that the video was published. All videos that you want to show on the front page of your site should be at least part of the special `uploads` category.

* `video` - The video folder is the output folder of the `transcode.py` script, and it is where the web-streamable video and thumbnails will be produced and hosted from. If you choose to host your video folder on a different domain than the rest of your site, be sure to update the `video-baseurl` in your `_config.yml` file.

* `_data` - In addition to populating the `video` folder, the `transcode.py` script also creates a resolution descriptor file called `resolutions.json` in the `_data` folder. Leave this where it is, as it contains the information necessary for the watch page to know which video resolutions and formats are available for the user to stream.

* `img` - Overwrite the image files here with your own custom branding.

#### Building OwnVideo with Your Own Videos

Now that you know the general folder structure of the OwnVideo theme, let's build it using your own custom videos.

1. Put your videos in the `source_video` folder with the naming scheme `video-id.ext`.
2. Put your custom thumbnails in the `source_video` folder with the naming scheme `video-id.jpg`. If you don't have custom thumbnails, video thumbnails will be automatically created for you!
3. Put your video metadata in the `_posts` folder with the naming scheme `YYYY-MM-DD-video-id.markdown`. For examples of what the metadata file should look like, please see the `_posts` folder in the example site.
4. `cd` into the `source_videos` folder and run `python transcode.py`. This will transcode your videos into web-streamable formats and output them ready-to-go in the `videos` folder. It will probably take a while.
5. Open up the `img` folder and replace the images there with your own custom branding.
6. Open the `about` folder and edit the `index.markdown` file to create your own about/contact page. Or you can just delete it. On the other hand, you may add additional pages - for example a `terms/index.markdown` or a `press/index.markdown`. As long as you set a permalink and title for them in the front-matter (and use the `page` layout), they should automatically show up in the site's nav bar.
6. Open `_config.yml` and add some info about yourself to the `title`, `description`, and `author` fields.
7. `cd` into the main folder and run `jekyll serve`. Visit http://localhost:4000/ and make sure your videos play well and your site looks exactly how you want it.
8. Open `_config.yml` one last time and change the `url` and `video-baseurl` fields to point to the final URLs where you will be hosting your site online.
9. Run `jekyll build` to produce the final build of your site, then upload the contents of the `_site` folder to your web hosting server.

## License

The MIT License (MIT)
Copyright (c) 2016 Maximillian Laumeister

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




