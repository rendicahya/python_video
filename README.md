# Python Video Utilities

## Available Function
1. `video_info()`

Reads information about a video. Available readers: `"opencv"` and `"moviepy"`.

Usage:
```python
from python_video import video_info

path = "/path/to/video"
info = video_info(path, reader="opencv")

print(info)
```

Output:
```python

```

2. `video_writer_like()`
3. `get_video_frames()`
4. `frames_to_video()`
