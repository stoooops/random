import argparse
import os
import imageio
import youtube_dl
from typing import Any, Dict, Tuple


def convert_to_gif(
    video_id: str, start_time: float, end_time: float, output_file: str
) -> None:
    # Download the video using youtube_dl
    ydl_opts: Dict[str, str] = {"outtmpl": "temp.%(ext)s"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

    reader: Any = imageio.get_reader("temp.mp4")
    fps: Any = reader.get_meta_data()["fps"]
    writer: Any = imageio.get_writer(output_file, fps=fps)
    for i, frame in enumerate(reader):
        if i / fps < start_time:
            continue
        if i / fps > end_time:
            break
        writer.append_data(frame)
    writer.close()
    # Delete the temporary video file
    # os.remove("temp.mp4")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("start_time", type=float, help="Start timestamp in seconds")
    parser.add_argument("end_time", type=float, help="End timestamp in seconds")
    parser.add_argument("output_file", help="Output file name (e.g. output.gif)")
    args = parser.parse_args()

    convert_to_gif(args.video_id, args.start_time, args.end_time, args.output_file)
