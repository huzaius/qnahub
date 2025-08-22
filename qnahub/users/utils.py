import os
import secrets
from PIL import Image
from datetime import datetime, timezone
from qnahub import app

@app.context_processor
def utility_processor():
    def time_ago(start_time):
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        return time_diff(datetime.now(timezone.utc), start_time)
    return dict(time_ago=time_ago)


def time_diff(end_time, start_time):
    time_difference = end_time - start_time
    seconds = time_difference.total_seconds()

    if seconds < 1:
        return "just now"
    elif seconds < 60:
        return f"{int(seconds)} second{'s' if int(seconds) > 1 else ''} ago"

    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} minute{'s' if int(minutes) > 1 else ''} ago"

    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} hour{'s' if int(hours) > 1 else ''} ago"

    days = hours / 24
    return f"{int(days)} day{'s' if int(days) > 1 else ''} ago"


# reduce picture size, re-filename and save
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_fn)

    output_size = (255, 255)
    i = Image.open(form_picture)

    # Convert image to a standard mode to handle different formats like
    # PNGs with transparency or palette-based images.
    if i.mode not in ("RGB", "L"):
        i = i.convert("RGB")

    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn