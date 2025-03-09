import argparse

import flask
import openai

from utils.generate_response import generate_response
from utils.system_prompt_generator import system_prompt_generator

app = flask.Flask(__name__)


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE', 'CONNECT'])
def anypath(path):
    structure = {
        "url": "/" + path,
        "method": flask.request.method,
        "arguments": flask.request.args.to_dict(),
        "cookies": flask.request.cookies.to_dict(),
        "headers": dict(flask.request.headers),
        "body": flask.request.json if flask.request.is_json else flask.request.get_data().decode(),
        "form": flask.request.form.to_dict(),
    }
    generated = generate_response(structure)
    return (generated['body'], generated['code'], generated['header'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A tool based on large language model to create a mock server.')
    parser.add_argument('--url', '-U', type=str, help="API URL", required=True)
    parser.add_argument('--key', '-K', type=str, help="API key", required=True)
    parser.add_argument('--model', '-M', type=str, help="Model name", required=True)
    parser.add_argument('--api', '-A', type=str, help="API description", required=True)
    app.model = parser.parse_args().model
    app.aiclient = openai.OpenAI(
        base_url=parser.parse_args().url,
        api_key=parser.parse_args().key,
    )
    app.message = [
        {
            "role": "system",
            'content': system_prompt_generator(parser.parse_args().api)
        }
    ]
    app.run()
