## Overview

This API provides a simple way to generate QR codes based on user-defined data. By using the API, you can create a QR code image that can be scanned by any compatible device to access the encoded information.

## Endpoint

`GET /qrgenerator/generate/`

## Parameters

-   `data`: (required) A string containing the information to be encoded in the QR code. It can be a URL, a plain text, or any other data that can be represented as a string. Example: `https://example.com`

## Example Request

`GET /qrgenerator/generate/?data=https://example.com`

## Response

The API will return a QR code image in PNG format, containing the encoded data provided in the request.

## Usage

To use the QR code generator API, simply make a GET request to the `/qrgenerator/generate/` endpoint with the `data` parameter. For example, you can use the following Python code to make a request to the API and save the resulting QR code image:

```
import requests

api_url = "http://localhost:8000/qrgenerator/generate/"
data = "https://example.com"
response = requests.get(api_url, params={"data": data})

if response.status_code == 200:
    with open("qr_code.png", "wb") as f:
        f.write(response.content)
else:
    print("Error:", response.status_code)

```

## Notes

-   Make sure to properly URL-encode the `data` parameter if it contains special characters or spaces.
-   The generated QR code will use the default settings for size and error correction level. If you need to customize these settings, you can modify the `generate_qr` view function in the `qrgenerator/views.py` file.

