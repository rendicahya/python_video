# Python Video Utilities

A Python library for video-related tasks. 

## Dependencies
```bash
pip install opencv-python-headless moviepy decord av
```

## Installation
This library should be used as a git submodule:
```bash
git submodule add https://github.com/rendicahya/python_video.git
```

## Available Functions
1. `video_info()`

Returns a dictionary containing information about a video:
- Width
- Height
- FPS
- Number of frames

Available readers are `"opencv"` (default) and `"moviepy"`. `path` can be either a string or a `PosixPath`.

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

3. `get_video_frames()`

Returns a frame generator from the specified video. Available readers are `"opencv"` (default), `"moviepy"`, `"pyav"`, `"decord"`.

Usage:
```python
from python_video import video_writer_like

path = "/path/to/video"
# or path = Path("/path/to/video")
frames = get_video_frames(path)

for frame in frames:
    # ...
```

To grab all frames at once, cast to a `list`:
```python
frames = list(get_video_frames(path))
```

4. `frames_to_video()`

Writes the specified frames to a video file. Available writers are `"opencv"` (default) and `"moviepy"`.

Usage:
```python
path = "/path/to/target/video"
# or path = Path("/path/to/target/video")

frames_to_video(frames, path, writer="opencv", fps=30, codec="mp4v")
```
