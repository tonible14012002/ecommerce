from operator import imod
from django import template
from .. models import Category

register = template.Library()

@register.inclusion_tag('store/tag_template/categories_dropdown.html')
def categories_dropdown():
    categories = Category.objects.all()
    return {'categories': categories}

@register.inclusion_tag('store/tag_template/product_card.html')
def show_product(product):
    return {'product':product}
