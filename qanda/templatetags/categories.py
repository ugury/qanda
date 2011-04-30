import qanda.models
from django import template

register = template.Library()

def do_category_list(parser,token):
    return GetCategoryListNode()

class GetCategoryListNode(template.Node):
    def render(self,context):
        context["category_list"] = qanda.models.Category.objects.all()
        return ''

register.tag('get_category_list', do_category_list)