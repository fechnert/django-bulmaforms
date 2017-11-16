from django import template
from django.utils.safestring import mark_safe

from bulmaforms.forms.utils import render_form_field, render_form_generics, render_form_errors
from bulmaforms.forms.elements import Field

register = template.Library()


@register.simple_tag
def bulma_form_fields(form):
    """Renders form fields with bulma styles and elements"""

    # append bulma css classes to widgets and let django render these widgets
    for field in form:

        widget_classes = list()

        # not every form element in bulma has the 'input' css class, so we need to differ here
        if getattr(field.field.widget, 'input_type', None) not in ['checkbox', 'radio']:
            widget_classes.append("input")

        # highlight fields with errors
        if field.errors:
            widget_classes.append("is-danger")

        # done
        if field.field.widget.attrs.get('class'):
            widget_classes.append(field.field.widget.attrs['class'])

        field.field.widget.attrs['class'] = " ".join(widget_classes)

    if getattr(form, 'layout', None):
        output = render_layout(form.layout, form)
    else:
        output = render_without_layout(form)

    return mark_safe(output)


@register.simple_tag
def bulma_form_errors(form):
    return render_form_errors([str(e) for e in form.non_field_errors()])


@register.simple_tag(takes_context=True)
def bulma_form(context, form, submit_text="OK", submit_class="button is-outlined", submit_only_once=True):
    """Renders whole form, including errors, csrf and a submit button."""

    fields = bulma_form_fields(form)
    errors = bulma_form_errors(form)

    return render_form_generics(context, fields, errors, submit_text, submit_class, submit_only_once)


def render_layout(elements, form):
    element_html = ''

    for element in elements:

        if isinstance(element, Field):
            # if the element itself is an field, give it the form field instance and render it
            element_html += element.render([field for field in form if field.name == element.field_name][0])
        else:
            content = ''

            # if the element has some child elements, render them
            if getattr(element, 'elements', []):
                content += render_layout(element.elements, form)

            # and now put the rendered things into the element's html markup
            element_html += element.render(mark_safe(content))

    return mark_safe(element_html)


def render_without_layout(form):
    output = ''
    for field in form:
        output += render_form_field(field)
    return mark_safe(output)
