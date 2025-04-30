from jinja2 import Template


def custom_tag(argument):
    # 实现标签逻辑
    return argument + "hcw"


template = Template("这是一个示例模板，标签结果为: {{ custom_tag('11') }} {{ data }}")
result = template.render(custom_tag=custom_tag, data={"test": 1})
print(result)
