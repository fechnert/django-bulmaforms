# django-bulmaforms [![python version](https://img.shields.io/badge/python-3.x-blue.svg)]() [![django version](https://img.shields.io/badge/Django-1.11.x-brightgreen.svg)]() [![bulma version](https://img.shields.io/badge/Bulma-0.5.1-yellow.svg)]()

Render django forms in bulma styles

![Demo image](https://raw.githubusercontent.com/fechnert/django-bulmaforms/master/doc/img/demo.png)


# Installation

*Coming soon with the publishing through PyPI*

# Usage

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
