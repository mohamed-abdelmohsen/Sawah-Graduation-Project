from django import template

register = template.Library()

@register.filter
def get_range(value):
    if isinstance(value, int):
        return range(1, value + 1)
    elif isinstance(value, float):
        return range(1, int(value) + 1)
    else:
        return None


@register.filter
def get_class_name(value):
    return value.__class__.__name__

@register.filter
def batch(sequence, count):
    """Batch a sequence into chunks of a specified size."""
    try:
        count = int(count)
    except ValueError:
        return [sequence]

    size = len(sequence) // count
    if size * count < len(sequence):
        size += 1

    return [sequence[i:i + size] for i in range(0, len(sequence), size)]
