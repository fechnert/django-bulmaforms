# django-bulmaforms [![python version](https://img.shields.io/badge/python-3.x-blue.svg)]() [![django version](https://img.shields.io/badge/Django-1.11.x-brightgreen.svg)]() [![bulma version](https://img.shields.io/badge/Bulma-0.6.1-brightgreen.svg)]()

Render [django](https://www.djangoproject.com/) [forms](https://docs.djangoproject.com/en/dev/topics/forms/) in [bulma](https://bulma.io/) styles

![Demo image](https://raw.githubusercontent.com/fechnert/django-bulmaforms/master/doc/img/demo.png)


# Installation

:soon: *Coming soon with the publishing through PyPI*

Don't forget to put it into your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # [...] django.contrib stuff
    'bulmaforms',
    # [...] and now your apps
]
```

# Usage

`django-bulmaforms` **does NOT** provide the bulma css library, you have to get and include it yourself somewhere in your markup. It only gives you template tags and layout elements to use them in your python code or template files.

To simply display the form with bulma styles, you can use the standard templatetag `{% bulma_form your_form %}`

```html
{% load bulmaforms %}

<form method="post">
    {% csrf_token %}

    {% bulma_form your_form %}
</form>
```

If you want to seperate form errors and the form itself, you can use the templatetags `{% bulma_form_errors your_form %}` and `{% bulma_form_fields your_form %}`

```html
{% load bulmaforms %}

<div class="columns">
    <div class="column is-half">
        {% bulma_form_errors your_form %}
    </div>
    <div class="column is-half">
        <form method="post">
            {% csrf_token %}

            {% bulma_form_fields your_form %}
        </form>
    </div>
</div>
```

You can even specify an own layout to use Bulma elements within your form markup:

```python
# forms.py

from hshassets.forms.elements import Card, Field, Submit

class MyAwesomeBulmaForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    layout = [
        Card(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Submit('Submit', css_class='is-success'),
            title='Registration',
        )
    ]
```

```html
<form method="post">
    {% csrf_token %}

    {% bulma_form form %}
</form>
```

![layout demo image](https://raw.githubusercontent.com/fechnert/django-bulmaforms/master/doc/img/layout.png)

Have a bug, need help or noticed a typo? [:love_letter: Let me know!](https://github.com/fechnert/django-bulmaforms/issues/new)
