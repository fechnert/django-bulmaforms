from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django.template import defaulttags


def render_form_field(field):
    try:
        input_type = field.field.widget.input_type
    except AttributeError:
        input_type = None

    if input_type in ['text', 'number', 'email', 'url', 'password']:
        # one of those text-like that support icons
        out = BulmaFieldMarkup.label(field.label, BulmaFieldMarkup.with_icons(field, field.as_widget()))
    elif input_type and getattr(BulmaFieldMarkup, input_type, None):
        # something else explicitly defined
        out = getattr(BulmaFieldMarkup, input_type)(field, field.as_widget())
    else:
        # fallback default
        out = BulmaFieldMarkup.label(field.label, BulmaFieldMarkup.div_control(field.as_widget()))

    return BulmaFieldMarkup.div_field(field, out)


class BulmaFieldMarkup(object):
    """
    HTML wrapper for input fields to add bulma styles.
    """

    def __init__(self):
        raise AssertionError("I'm a singleton. Boo.")

    @classmethod
    def div_field(cls, field, content):
        """Bulma requires to wrap every input field with this <div class="field">"""
        args_generator = ([str(e)] for e in field.errors)
        error_tags = format_html_join(str(), '<p class="help is-danger">{0}</p>', args_generator)
        return format_html('<div class="field">{}{}</div>', content, error_tags)

    @classmethod
    def div_control(cls, content, control_class='control'):
        """Bulma requires to wrap input elements with an <div class="control">"""
        return format_html('<div class="{1}">{0}</div>', content, control_class)

    @classmethod
    def label(cls, label, content='', css_class='label', for_id=''):
        """Define <label> seperately so it can be used elsewhere instead as a children of the <div class="field">"""

        if for_id:
            return format_html('<label for="{}" class="{}">{}</label> {}', for_id, css_class, label, content)
        else:
            # don't output a empty for="" attribute as it breaks some form functionality
            return format_html('<label class="{}">{}</label> {}', css_class, label, content)

    @classmethod
    def with_icons(cls, field, content):
        """
        Input field with icon in the left. Usage:
        my_field = forms.CharField(widget=forms.TextInput(attrs={"icon": "fa-barcode"}))
        """

        icon_html = '<span class="icon is-small {side}"><i class="fa {icon}"></i></span>'
        control_classes = ['control']
        icon_left, icon_right = None, None

        # left icon is user customizable
        icon_left = field.field.widget.attrs.get('icon', None)

        if icon_left:
            control_classes.append('has-icons-left')

        # right icon appears on field errors
        if field.errors:
            control_classes.append("has-icons-right")
            icon_right = 'fa-warning'

        content = format_html(
            '{content}{i1}{i2}',
            content=content,
            i1=format_html(icon_html, side='is-left', icon=icon_left) if icon_left else str(),
            i2=format_html(icon_html, side='is-right', icon=icon_right) if icon_right else str(),
        )

        return cls.div_control(content, control_class=' '.join(control_classes))

    @classmethod
    def select(cls, field, content):
        """Dropdowns have an extra wrapping <div class="select">"""
        return cls.label(field.label, cls.div_control(format_html('<div class="select">{}</div>', content)))

    @classmethod
    def checkbox(cls, field, content):
        """Checkboxes are super special, they wrap the input field with the label"""
        return cls.div_control(cls.label(mark_safe(content + ' ' + str(field.label)), css_class='checkbox'))

    @classmethod
    def radio(cls, field, content):
        choice_markup = ''
        for choice in field:
            choice_markup += cls.label(
                choice.tag(), choice.choice_label.title(),
                for_id=choice.id_for_label, css_class='radio'
            )
        return cls.div_control(mark_safe(choice_markup))

    @classmethod
    def hidden(cls, field, content):
        """Hidden fields with labels are silly"""
        return cls.div_control(content)


def render_form_generics(context, rendered_fields, rendered_errors, submit_text, submit_class, submit_only_once=True):
    csrf_field = defaulttags.CsrfTokenNode().render(context)
    submit_only_once = "true" if submit_only_once else "false"
    return format_html(
        """
        <form method="post" data-submit-only-once="{submit_only_once}">
            {rendered_errors}
            {rendered_fields}
            {csrf_field}
            <button class="{submit_class}" type="submit">{submit_text}</button>
        </form>
        """,
        **locals()
    )


def render_form_errors(errors):
    if not errors:
        return format_html(str())
    args_generator = ([str(e)] for e in errors)
    error_tags = format_html_join(str(), '<p>{}</p>', args_generator)
    return format_html(
        """
        <div class="message is-danger is-1">
            <div class="message-body is-1">
                {error_tags}
            </div>
        </div>
        """,
        error_tags=error_tags,
    )
