def system_prompt_generator(api_desc_path: str):
    with open(api_desc_path) as desc_file:
        prompt = """现在，你需要模拟一个应用服务器后端。我会给你一个文档，里面包含有API的描述，然后我会提供请求的内容，请依据文档给出返回。请以这种方式给出返回：
{
  "code": code,
  "header": {
    "key1": value1
  },
  "body": body
}
返回包含且仅包含这些内容，除此之外再无其它。请以严格的JSON格式输出。不要加上任何额外提示。
每次返回结果应当与前后保持关联性。
现在，文档如下：
""" + desc_file.read()
    return prompt
