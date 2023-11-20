# Python Video Utilities

A Python library for video-related tasks. Should be used as a git submodule:
`git submodule add https://github.com/rendicahya/python_video.git`

## Dependencies
```bash
pip install opencv-python-headless moviepy decord av
```

## Available Function
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
# of path = Path("/path/to/video")
info = video_info(path, reader="opencv")

print(info)
```

Output:
```python

```

2. `video_writer_like()`
3. `get_video_frames()`
4. `frames_to_video()`
