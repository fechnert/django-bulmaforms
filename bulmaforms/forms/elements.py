from django.utils.safestring import mark_safe
from django.utils.html import format_html

from bulmaforms.forms.utils import render_form_field


class AbstractElement(object):
    markup = ''

    def __init__(self, *args, **kwargs):
        self.elements = args

    def render(self, content):
        return format_html(self.markup, content)


class Field(AbstractElement):

    def __init__(self, field_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_name = field_name

    def render(self, field):
        return mark_safe(render_form_field(field))


class Columns(AbstractElement):
    markup = '<div class="columns is-multiline">{}</div>'


class Column(AbstractElement):
    markup = '<div class="column is-{}">{}</div>'

    def __init__(self, width, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width

    def render(self, content):
        return format_html(self.markup, self.width, content)


class Card(AbstractElement):
    markup = '<div class="card">{}<div class="card-content">{}</div></div>'
    card_header_markup = '<header class="card-header"><p class="card-header-title">{}</p></header>'

    def __init__(self, *args, title='', **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title

    def render(self, content):
        if self.title:
            return format_html(self.markup, format_html(self.card_header_markup, self.title), content)
        else:
            return format_html(self.markup, self.title, content)


class Submit(AbstractElement):
    markup = '<div class="field"><div class="control"><button type="submit" class="button {}">{}</button></div></div>'

    def __init__(self, label, css_class='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = label
        self.css_class = css_class

    def render(self, content):
        return format_html(self.markup, self.css_class, self.label)
