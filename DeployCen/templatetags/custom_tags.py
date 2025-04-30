from django import template

from ConfCen.models import TaskCreate
from jinja2 import Template

register = template.Library()  

@register.simple_tag
def get_rollBack_type(name):
    n=TaskCreate.objects.get(name=name)
    if n.rollBack != "是" :
 
        return "否"
    return  n.rollBack

# @register.simple_tag
# def get_href(id,id2,id3):
#     temp=Template(web_list.objects.get(Id=id).node.describe)
#     href=temp.render(profix_by=[id2+"/"+id3])

#     return  href

