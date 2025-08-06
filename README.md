# Python Video Utilities

A Python library for video-related tasks. 

## Dependencies
```bash
pip install opencv-python-headless moviepy decord av
```

## Installation
This library is designed to be used as a git submodule:
```bash
git submodule add https://github.com/rendicahya/python_video.git
```

## Available Functions

### 1. `video_info()`
Returns a dictionary containing information about a video:
- width
- height
- FPS
- number of frames

Available readers are `"opencv"` (default) and `"moviepy"`. `path` can be either a string or a `pathlib`'s `PosixPath`.

Usage:
```python
from python_video import video_info
from pathlib import Path

path = "/path/to/video"
# or:
# path = Path("/path/to/video")

info = video_info(path, reader="opencv")
```

### 2. `video_frames()`
Returns a frame generator from the specified video. Available readers are `"opencv"` (default), `"moviepy"`, `"pyav"`, and `"decord"`.

Usage:
```python
from python_video import video_writer_like

path = "/path/to/video"
# or path = Path("/path/to/video")
frames = video_frames(path, reader="opencv")

for frame in frames:
    # ...
```

To grab all frames at once, cast to a `list`. This should be avoided, though, as it inefficiently loads all frames onto memory:
```python
frames = list(get_video_frames(path))
```

### 3. `video_writer_like()`
Returns an OpenCV video writer with the same properties as the specified video.

Usage:
```python
from python_video import video_writer_like

src_path = "/path/to/src-video.mp4"
# or src_path = Path("/path/to/src-video.mp4")

dst_path = "/path/to/dst-video.mp4"
# or dst_path = Path("/path/to/dst-video.mp4")

writer = video_writer_like(src_path, target=dst_path)

for frame in frames:
    writer.write(frame)

writer.release()
```

### 4. `frames_to_video()`
Writes images frames to a video file. Available writers are `"opencv"` (default) and `"moviepy"`.

Usage:
```python
path = "/path/to/target/video"
# or path = Path("/path/to/target/video")

frames_to_video(frames, path, writer="opencv", fps=30, codec="mp4v")
```

Combining with `video_info()` and `video_frames()` to read frames from a video and write them to another video:
```python
src_path = "/path/to/target/video-src.mp4"
# or src_path = Path("/path/to/target/video-src.mp4")

info = video_info(src_path)
frames = video_frames(src_path)

dst_path = "/path/to/target/video-dst.mp4"
# or dst_path = Path("/path/to/target/video-dst.mp4")

frames_to_video(frames, path, writer="opencv", fps=info["fps"], codec="mp4v")
```
