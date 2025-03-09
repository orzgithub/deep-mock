import openai
import flask
import json5


def generate_response(request: dict):
    aiclient = flask.current_app.aiclient
    aimessage = flask.current_app.message
    aimessage.append(
        {
            'role': 'user',
            'content': json5.dumps(request, ensure_ascii=False, indent=2)
        }
    )
    response = aiclient.chat.completions.create(
        model=flask.current_app.model,
        messages=aimessage,
        temperature=0.2
    )
    aimessage.append(
        {
            'role': 'assistant',
            'content': response.choices[0].message.content
        }
    )
    print(response.choices[0].message.content)
    return json5.loads(response.choices[0].message.content)
