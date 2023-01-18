import argparse
import os
import imageio
import youtube_dl
from typing import Any, Dict, Tuple


def convert_to_gif(
    video_id: str, start_time: float, end_time: float, output_file: str
) -> None:
    # Download the video using youtube_dl
    ydl_opts: Dict[str, str] = {"outtmpl": f"temp.{video_id}.%(ext)s"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

    # files
    mp4: str = f"temp.{video_id}.mp4"
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

    convert_to_gif(args.video_id, args.start_time, args.end_time, args.output_file)


if __name__ == "__main__":
    main()
