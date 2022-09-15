from flask import Flask, render_template, request
from PIL import Image
from cv2 import VideoCapture
from werkzeug.utils import secure_filename
import os
from numpy import arange

ASCII_CHARS = " .:-=+*#%@"
PIXEL_WIDTH = 28.34
SIZE = (10, 10)
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/")
def home():
    return render_template("index.html")


def convert(image_data) -> str:
    image = Image.fromarray(image_data)  # Create PIL Image object
    image = image.resize(SIZE)
    width = SIZE[0]

    # rgb_image_data = image.getdata()
    image = image.convert('L')  # Convert the image into shades of black
    image_data = image.getdata()  # Get the image data

    new_data = [
        ASCII_CHARS[int(pixel_value/PIXEL_WIDTH)]
        for
        pixel_value
        in
        image_data
    ]
    length = len(new_data)
    split_data = [
        ''.join(new_data[index: index+width])
        for
        index
        in
        arange(0, length, width)
    ]
    # new_data = [
    #     colored(*rgb, ascii_chars[int(pixel_value/pixel_width)])
    #         for
    #     rgb, pixel_value
    #         in
    #     zip(rgb_image_data, image_data)
    # ]
    # length = len(new_data)
    # split_data = [
    #     ''.join(new_data[index: index+width])
    #         for
    #     index
    #         in
    #     arange(0, length, width)
    # ]
    # The code above is too complicated to explain

    return '\n'.join(split_data)


def vid_to_ascii(vidcap) -> list:
    text = []
    success, frame = vidcap.read()  # Read next frame
    while success:
        converted = convert(frame)
        text.append(converted)
        success, frame = vidcap.read()
    return text


@app.route("/sendVideo", methods=["POST"])
def handle_message():
    if (not (vid := request.files["VID"])):
        return {"ERROR": "VID NOT FOUND"}
    print(vid)
    try:
        file_name = secure_filename(vid.filename)
        path = os.path.join("uploads", file_name)
        vid.save(path)
        vidcap = VideoCapture(path)
        result = vid_to_ascii(vidcap)
        return ''.join(result)

    except Exception as e:
        print(e)
        return {"ERROR": "VID NOT VALID"}


if __name__ == "__main__":
    app.run()
