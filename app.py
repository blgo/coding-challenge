from requests import RequestException
from flask import Flask, jsonify, request
from PIL import Image

from errors import ImageTooBig, InvalidURL
from utils import (
    check_image_size,
    download_image,
    load_image,
    validate_url,
    get_closest_color,
    calc_most_common_color,
)

# Prevent overloading the server by a DecompressionBomb attack
Image.MAX_IMAGE_PIXELS = (
    10000 * 10000
)

# Endpoint will flag up image as bad if we didn't get a good enought match
SCORE_TOO_LOW = 50

# Initialise Flask app
app = Flask(__name__)


# Register Error Handlers
@app.errorhandler(InvalidURL)
@app.errorhandler(ImageTooBig)
def bad_request(error):
    """
    JSON description for Validation errors (400)
    """
    return jsonify({"description": error.description}), error.code


@app.errorhandler(RequestException)
def requests_error_handler(error):
    """
    Capture all errors from API requests to external websites and return them as a JSON object wth description and error code
    """
    print(error.response)
    if error.response:
        return (
            jsonify({"description": f"{error.response.reason}: ${error.response.url}"}),
            error.response.status_code,
        )
    else:
        raise error


# Register routes
@app.route("/healthcheck")
def healthcheck_api():
    return "OK"


@app.route("/detectcolour", methods=["POST"])
def detectcolour_api():
    url = request.json.get("url")
    validate_url(url)
    check_image_size(url)
    image_raw_data = download_image(url)
    image = load_image(image_raw_data)
    image_most_common_colour = calc_most_common_color(image)
    closest_color = get_closest_color(image_most_common_colour)
    if closest_color['value'] > SCORE_TOO_LOW:
        return jsonify({**closest_color, "error": f"Score was lower than {SCORE_TOO_LOW}"}), 404
    return jsonify(closest_color)
