from django import template

register = template.Library()

@register.filter
def money(value):
    """
    Chuyển số nguyên thành dạng 69.000 đ
    """
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".") + " đ"
    except (ValueError, TypeError):
        return value
