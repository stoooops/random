import argparse
import json
import os
from typing import Any, Dict, Tuple

import imageio
import yt_dlp
from yt_dlp import YoutubeDL


class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith("[debug] "):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now post-processing ...")


def format_selector(ctx):
    """Select the best video and the best audio that won't result in an mkv.
    NOTE: This is just an example and does not handle all cases"""

    # formats are already sorted worst to best
    formats = ctx.get("formats")[::-1]

    # acodec='none' means there is no audio
    best_video = next(
        f for f in formats if f["vcodec"] != "none" and f["acodec"] == "none"
    )

    # find compatible audio extension
    audio_ext = {"mp4": "m4a", "webm": "webm"}[best_video["ext"]]
    # vcodec='none' means there is no video
    best_audio = next(
        f
        for f in formats
        if (f["acodec"] != "none" and f["vcodec"] == "none" and f["ext"] == audio_ext)
    )

    # These are the minimum required fields for a merged format
    yield {
        "format_id": f'{best_video["format_id"]}+{best_audio["format_id"]}',
        "ext": best_video["ext"],
        "requested_formats": [best_video, best_audio],
        # Must be + separated list of protocols
        "protocol": f'{best_video["protocol"]}+{best_audio["protocol"]}',
    }


ydl_opts = {
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
    "format": format_selector,
}


def download_video(video_id: str) -> str:
    mp4: str = f"temp.{video_id}.mp4"
    url: str = f"https://www.youtube.com/watch?v={video_id}"
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info: Dict[str, Any] = ydl.extract_info(url, download=False)

    # ℹ️ ydl.prepare_filename makes the filename safe
    filename: str = ydl.prepare_filename(info)
    print(f"Downloading video to {filename}...")

    ydl.download([url])

    return mp4


def convert_to_gif(
    mp4: str, start_time: float, end_time: float, output_file: str
) -> None:
    gif: str = output_file.split(".")[0] + ".gif"
    gifv = output_file.split(".")[0] + ".gifv"

    print("Converting video to GIF...")
    reader: Any = imageio.get_reader(mp4)
    fps: Any = reader.get_meta_data()["fps"]
    writer: Any = imageio.get_writer(gif, fps=fps)
    for i, frame in enumerate(reader):
        if i % fps == 0:
            print(f"Processed {i} frames ({i/fps}s)")
        if i / fps < start_time:
            continue
        if i / fps > end_time:
            break
        writer.append_data(frame)
    writer.close()

    # convert gif to gifv
    print("Converting GIF to GIFV...")
    os.system(f"gifsicle --colors 256 --optimize=3 {gif} -o {gifv}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("start_time", type=float, help="Start timestamp in seconds")
    parser.add_argument("end_time", type=float, help="End timestamp in seconds")
    parser.add_argument("output_file", help="Output file name (e.g. output.gif)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    mp4: str = download_video(args.video_id)
    print("Downloaded video to", mp4)
    convert_to_gif(mp4, args.start_time, args.end_time, args.output_file)


if __name__ == "__main__":
    main()
