# Coding Test

Test description can be found on [this file](./SeniorPythonDevTechTest.pdf)

## Requirements
Python 3.10
venv
Pillow native dependencies: [https://pillow.readthedocs.io/en/stable/installation.html](https://pillow.readthedocs.io/en/stable/installation.html)

## Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
# Ensure you install libimagequant for your OS/Linux distro
pip install --upgrade Pillow --global-option="build_ext" --global-option="--enable-imagequant"
export FLASK_ENV=development
export FLASK_APP=app
python -m flask runflask run
```

## Test the detect colors endpoint:

```bash
 curl -X POST http://localhost:5000/detectcolour \
    -H 'Content-Type: application/json' \
    -d '{"url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-black.png"}' \
    --verbose

*   Trying 127.0.0.1:5000...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /detectcolour HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.83.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 89
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.10.4
< Date: Sun, 12 Jun 2022 11:35:42 GMT
< Content-Type: application/json
< Content-Length: 38
< Connection: close
< 
{
  "key": "black", 
  "value": 0.0
}
* Closing connection 0

```

```bash
$ curl -X POST http://localhost:5000/detectcolour \
    -H 'Content-Type: application/json' \
    -d '{"url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-grey.png"}' \
    --verbose

Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1:5000...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /detectcolour HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.83.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 88
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.10.4
< Date: Sun, 12 Jun 2022 11:36:29 GMT
< Content-Type: application/json
< Content-Length: 37
< Connection: close
< 
{
  "key": "grey", 
  "value": 0.0
}
* Closing connection 0
```

```bash
$ curl -X POST http://localhost:5000/detectcolour \
    -H 'Content-Type: application/json' \
    -d '{"url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-teal.png"}' \
    --verbose
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1:5000...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /detectcolour HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.83.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 88
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.10.4
< Date: Sun, 12 Jun 2022 11:30:59 GMT
< Content-Type: application/json
< Content-Length: 37
< Connection: close
< 
{
  "key": "teal", 
  "value": 0.0
}
* Closing connection 0
```

```bash
$ curl -X POST http://localhost:5000/detectcolour \
    -H 'Content-Type: application/json' \
    -d '{"url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-navy.png"}' \
    --verbose
Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1:5000...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /detectcolour HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.83.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 88
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: Werkzeug/2.1.2 Python/3.10.4
< Date: Sun, 12 Jun 2022 11:34:22 GMT
< Content-Type: application/json
< Content-Length: 37
< Connection: close
< 
{
  "key": "navy", 
  "value": 0.0
}
* Closing connection 0
```

## Low score test

SCORE_TOO_LOW determines when an image is flagged by the API.

The API will show the score and an error message. 
The response code is 404.

```bash
curl -X POST http://localhost:5000/detectcolour -H 'Content-Type: application/json' -d '{"url": "https://blgo.netlify.app/img/profile.jpg"}' --verbose

Note: Unnecessary use of -X or --request, POST is already inferred.
*   Trying 127.0.0.1:5000...
* Connected to localhost (127.0.0.1) port 5000 (#0)
> POST /detectcolour HTTP/1.1
> Host: localhost:5000
> User-Agent: curl/7.83.1
> Accept: */*
> Content-Type: application/json
> Content-Length: 51
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 404 NOT FOUND
< Server: Werkzeug/2.1.2 Python/3.10.4
< Date: Sun, 12 Jun 2022 11:05:58 GMT
< Content-Type: application/json
< Content-Length: 90
< Connection: close
< 
{
  "error": "Score was lower than 50", 
  "key": "grey", 
  "value": 51.43928459844674
}
* Closing connection 0
```
