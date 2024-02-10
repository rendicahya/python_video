import types
from pathlib import Path
from typing import Union

import av
import cv2
from assertpy.assertpy import assert_that
from decord import VideoReader, cpu
from moviepy.editor import ImageSequenceClip, VideoFileClip


def video_info(path: Union[Path, str], reader: str = "opencv"):
    assert_that(path).is_file().is_readable()
    assert_that(reader).is_in("opencv", "moviepy")

    if reader == "opencv":
        video = cv2.VideoCapture(str(path))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    elif reader == "moviepy":
        clip = VideoFileClip(str(path))
        width = clip.w
        height = clip.h
        fps = clip.fps
        n_frames = clip.reader.nframes

    return {"width": width, "height": height, "fps": fps, "n_frames": n_frames}


def video_writer_like(
    path: Union[Path, str], target: Union[Path, str], format: str = "mp4"
):
    assert_that(path).is_file().is_readable()
    assert_that(format).is_in("mp4")

    fourcc_formats = {"mp4": "mp4v"}
    fourcc_format = fourcc_formats[format]
    fourcc = cv2.VideoWriter_fourcc(*fourcc_format)
    info = video_info(path)
    width = info["width"]
    height = info["height"]
    fps = info["fps"]

    return cv2.VideoWriter(
        str(target),
        fourcc,
        fps,
        (width, height),
    )


def video_frames(path: Union[Path, str], reader: str = "opencv", bgr2rgb: bool = True):
    """
    Generator function that yields frames from a video file using different video readers.

    Args:
    - path (Union[Path, str]): Path to the video file.
    - reader (str, optional): Specifies the video reader library to use. Default is "opencv".
        Available options: "opencv", "moviepy", "pyav", "decord".
    - bgr2rgb (bool, optional): If True, converts BGR formatted frames to RGB. Default is True.

    Yields:
    - ndarray: Frames from the video file in RGB format (if specified) or in the original format.

    Raises:
    - AssertionError: If the path is not a readable file or if an invalid video reader is provided.
    """
    assert_that(path).is_file().is_readable()
    assert_that(reader).is_in("opencv", "moviepy", "pyav", "decord")

    if reader == "opencv":
        cap = cv2.VideoCapture(str(path))

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if bgr2rgb else frame

        cap.release()
    elif reader == "moviepy":
        with VideoFileClip(str(path)) as clip:
            for frame in clip.iter_frames():
                yield frame
    elif reader == "pyav":
        with av.open(path) as container:
            for frame in container.decode(video=0):
                yield frame.to_ndarray(format="rgb24")
    elif reader == "decord":
        with open(path, "rb") as f:
            video_reader = VideoReader(f, ctx=cpu(0))

            for i in range(len(video_reader)):
                yield video_reader[i].asnumpy()


def frames_to_video(
    frames: Union[list, types.GeneratorType],
    target: Union[Path, str] = "video.mp4",
    writer: str = "opencv",
    fps: int = 30,
    codec: str = "mp4v",
    rgb2bgr: bool = True,
) -> None:
    assert_that(writer).is_in("opencv", "moviepy")
    assert_that(Path(target).parent).is_directory().is_readable()

    if writer == "opencv":
        if type(frames) == types.GeneratorType:
            first_frame = next(frames, None)

            if first_frame is None:
                return
        else:
            if len(frames) == 0:
                return

            first_frame = frames[0]

        fourcc = cv2.VideoWriter_fourcc(*codec)
        height, width = first_frame.shape[:2]

        video_writer = cv2.VideoWriter(
            str(target),
            fourcc,
            fps,
            (width, height),
        )

        convert = lambda frame: cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # If frames is a generator, the first frame has been
        # extracted above (next(frames, None)), so it should be written
        if type(frames) == types.GeneratorType:
            video_writer.write(convert(first_frame) if rgb2bgr else first_frame)

        for frame in frames:
            video_writer.write(convert(frame) if rgb2bgr else frame)

        video_writer.release()
    elif writer == "moviepy":
        frames = list(frames)

        if len(frames) > 0:
            ImageSequenceClip(frames, fps=fps).write_videofile(str(target), logger=None)
        else:
            print(f"Video {str(target)} not written because frames are empty.")
    # elif writer == "pyav":
    #     with av.open(str(target), "w", format="mp4") as container:
    #         out_stream = container.add_stream("h264", fps)

    #         for frame in frames:
    #             new_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
    #             new_frame = out_stream.encode(new_frame)
    #             container.mux(new_frame)
