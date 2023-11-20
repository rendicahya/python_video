# Python Video Utilities

A Python library for video-related tasks. 

## Dependencies
```shell
pip install opencv-python-headless moviepy decord av
```

## Installation
This library should be used as a git submodule:
```shell
git submodule add https://github.com/rendicahya/python_video.git
```

## Available Functions
1. `video_info()`

Returns a dictionary containing information about a video:
- Width
- Height
- FPS
- Number of frames

Available readers are`"opencv"` (default) and `"moviepy"`. `path` can be either a string or a `PosixPath`.

Usage:
```python
from python_video import video_info
from pathlib import Path

path = "/path/to/video"
# or path = Path("/path/to/video")
info = video_info(path, reader="opencv")

print(info)
```

Output:
```python

```

2. `video_writer_like()`

Returns an OpenCV video writer with the same properties as the specified video.

Usage:
```python
from python_video import video_writer_like

path = "/path/to/video"
# or path = Path("/path/to/video")
writer = video_writer_like(path)

for frame in frames:
    writer.write(frame)

writer.release()
```

4. `get_video_frames()`
5. `frames_to_video()`
