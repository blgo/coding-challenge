import math
import re
import requests
import statistics
from PIL import Image

from color_preferences import prodigi_sku_colors as colors
from errors import ImageTooBig, InvalidURL

# Constants to calculate file size from Content-Length header
MBFACTOR = float(1 << 20)
MAX_IMAGE_SIZE_MB = 300

# Regex to validate URLs passed to the API
# https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    # domain...
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)"
    # Only allow image file formats
    r"(?:.*\.[png|jpg|bmp]+)$",
    re.IGNORECASE,
)


def validate_url(url):
    if not URL_REGEX.match(url):
        raise InvalidURL(url)


def check_image_size(url):
    # Check size before attempting to download the file:
    response = requests.head(url, allow_redirects=True)
    # Raise Exception from API response if status code is not 200
    response.raise_for_status()
    size = response.headers.get("content-length", 0)
    megabytes = int(size) / MBFACTOR

    if megabytes > MAX_IMAGE_SIZE_MB:
        raise ImageTooBig()


def download_image(url):
    response = requests.get(url, stream=True)
    # Raise Exception from API response if status code is not 200
    response.raise_for_status()
    response.raw.decode_content = True
    return response.raw


def load_image(raw_image):
    return Image.open(raw_image)


def calc_most_common_color(image):
    most_frecuent_color = tuple(
        [int(statistics.quantiles(x.getdata(), n=10)[0]) for x in image.split()]
    )
    return most_frecuent_color


def get_closest_color(image_rgb):
    # Lower score is better
    scores = [ { 
            "key": color,
                # Calculate euclidean distance
            "value": math.sqrt((image_rgb[0] - rgb[0]) ** 2
                    + (image_rgb[1] - rgb[1]) ** 2 
                    + (image_rgb[2] - rgb[2]) ** 2)
            } 
            for rgb, color in colors.items()]
    # Sort scores by closest match
    scores.sort(key=lambda x: x["value"])
    return scores[0]