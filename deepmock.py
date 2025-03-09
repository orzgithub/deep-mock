import argparse

import flask
import openai

from utils.generate_response import generate_response
from utils.system_prompt_generator import system_prompt_generator


class DeepMockApp(flask.Flask):
    def __init__(self, *app_args, **kwargs):
        super().__init__(*app_args, **kwargs)
        parser = argparse.ArgumentParser(
            description='A tool based on large language model to create a mock server.')
        parser.add_argument('--url', '-U', type=str, help="API URL", required=True)
        parser.add_argument('--key', '-K', type=str, help="API key", required=True)
        parser.add_argument('--model', '-M', type=str, help="Model name", required=True)
        parser.add_argument('--api', '-A', type=str, help="API description", required=True)
        app_args = parser.parse_args()
        self.model = app_args.model
        self.aiclient = openai.AsyncOpenAI(
            base_url=app_args.url,
            api_key=app_args.key,
        )
        self.message = [
            {
                "role": "system",
                'content': system_prompt_generator(app_args.api)
            }
        ]


app = DeepMockApp(__name__)


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE', 'CONNECT'])
async def anypath(path):
    structure = {
        "url": "/" + path,
        "method": flask.request.method,
        "arguments": flask.request.args.to_dict(),
        "cookies": flask.request.cookies.to_dict(),
        "headers": dict(flask.request.headers),
        "body": flask.request.json if flask.request.is_json else flask.request.get_data().decode(),
        "form": flask.request.form.to_dict(),
    }
    generated = await generate_response(structure)
    return (
        generated['body'] if generated['body'] is not None else "",
        generated['code'],
        generated['header']
    )


if __name__ == '__main__':
    app.run()
