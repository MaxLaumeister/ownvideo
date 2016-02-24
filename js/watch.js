/* Library functions */

// Source: http://stackoverflow.com/a/16861050/2234742
function PopupCenter(url, title, w, h) {
    // Fixes dual-screen position                         Most browsers      Firefox
    var dualScreenLeft = window.screenLeft != undefined ? window.screenLeft : screen.left;
    var dualScreenTop = window.screenTop != undefined ? window.screenTop : screen.top;

    var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
    var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

    var left = ((width / 2) - (w / 2)) + dualScreenLeft;
    var top = ((height / 2) - (h / 2)) + dualScreenTop;
    var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);

    // Puts focus on the newWindow
    if (window.focus) {
        newWindow.focus();
    }
}

// Source: https://gist.github.com/mathewbyrne/1280286
function slugify(text)
{
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
    .replace(/\-\-+/g, '-')         // Replace multiple - with single -
    .replace(/^-+/, '')             // Trim - from start of text
    .replace(/-+$/, '');            // Trim - from end of text
}

// Source: https://github.com/m-gagne/limit.js

/**
 * debounce
 * @param {integer} milliseconds This param indicates the number of milliseconds
 *     to wait after the last call before calling the original function.
 * @param {object} What "this" refers to in the returned function.
 * @return {function} This returns a function that when called will wait the
 *     indicated number of milliseconds after the last call before
 *     calling the original function.
 */
Function.prototype.debounce = function (milliseconds, context) {
    var baseFunction = this,
        timer = null,
        wait = milliseconds;

    return function () {
        var self = context || this,
            args = arguments;

        function complete() {
            baseFunction.apply(self, args);
            timer = null;
        }

        if (timer) {
            clearTimeout(timer);
        }

        timer = setTimeout(complete, wait);
    };
};

/**
* throttle
* @param {integer} milliseconds This param indicates the number of milliseconds
*     to wait between calls before calling the original function.
* @param {object} What "this" refers to in the returned function.
* @return {function} This returns a function that when called will wait the
*     indicated number of milliseconds between calls before
*     calling the original function.
*/
Function.prototype.throttle = function (milliseconds, context) {
    var baseFunction = this,
        lastEventTimestamp = null,
        limit = milliseconds;

    return function () {
        var self = context || this,
            args = arguments,
            now = Date.now();

        if (!lastEventTimestamp || now - lastEventTimestamp >= limit) {
            lastEventTimestamp = now;
            baseFunction.apply(self, args);
        }
    };
};

/* Show the correct playlist in sidebar */

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}

var playlist = getURLParameter("playlist");
if (!playlist) playlist = "uploads";

var next_videos_panels = document.getElementsByClassName("next-videos");
var panel_showing = false;
for (var i = 0; i < next_videos_panels.length; i++) {
    var panel = next_videos_panels[i];
    var num_vids = parseInt(panel.getElementsByClassName("meta-posts-count")[0].textContent, 10);
    if (num_vids !== 0 && panel.dataset.categoryName === playlist) {
        panel_showing = true;
        panel.style.display = "block";
        if (playlist !== "uploads") {
            var vidLink = panel.getElementsByClassName("vid-link")[0];
            vidLink.setAttribute("href", vidLink.getAttribute("href") + "?playlist=" + slugify(playlist));
        }
    }
}
if (!panel_showing) {
    document.querySelector(".next-videos[data-category-name=uploads]").style.display = "block";
}

/* Initialize sharing buttons */

var title = document.title;
var encoded_title = encodeURIComponent(title);

var url = window.location.href;
var encoded_url = encodeURIComponent(url);

var fb = document.getElementsByClassName("ico-facebook");

for (var i = 0; i < fb.length; i++) {
    fb[i].href = "https://www.facebook.com/sharer.php?u=" + encoded_url;
}

var tw = document.getElementsByClassName("ico-twitter");

for (var i = 0; i < tw.length; i++) {
    tw[i].href = "https://twitter.com/share?text=" + encoded_title + "&url=" + encoded_url;
}

var gp = document.getElementsByClassName("ico-google");

for (var i = 0; i < gp.length; i++) {
    gp[i].href = "https://plus.google.com/share?url=" + encoded_url;
}

/* Lock video wrapper size */
        
var video_wrapper = document.getElementById("main-video-wrap");
video.oncanplay = function() {
    video_wrapper.style.width = video_wrapper.clientWidth + "px";
    video_wrapper.style.height = video_wrapper.clientHeight + "px";
}

/* Save video volume */

var prev_volume = 1;
function saveVideoVolume() {
    var volume = video.volume;
    if (volume !== prev_volume) {
        console.log(volume);
        // TODO: Save volume here
    }
    prev_volume = volume;
}

var sv_throttled = saveVideoVolume.throttle(200);

video_wrapper.addEventListener("mouseleave", sv_throttled);
video_wrapper.addEventListener("mousemove", sv_throttled);
window.addEventListener("beforeunload", saveVideoVolume);