# Deep Mock
A mock server based on deep learning designed for different usages. Written in python.

Usage:
```bash
deepmock.py
--url, -U:  LLM service base url
--key, -K:  LLM service API key
--model, -M:  LLM model name
--api, -A:  path of a plain text file (such as OpenAPI documentation) describing the API
```
All the parameters are required.

It's designed to be a development server so werkzeug is acceptable. The project currently does not provide maintenance and support through methods other than starting directly from the Python file itself.
