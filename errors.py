from werkzeug.exceptions import HTTPException


class InvalidURL(HTTPException):
    code = 400
    description = 'This is not a valid URL'


class ImageTooBig(HTTPException):
    code = 400
    description = 'Image is too big'
