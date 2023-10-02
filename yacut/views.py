from urllib.parse import urljoin

from flask import render_template, abort, flash, request, Markup, redirect

from yacut import app, db
from yacut.utils import get_unique_short_id
from yacut.validators import validate_short_id
from yacut.models import URLMap
from yacut.forms import UrlForm


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short_url = URLMap.get_unique_short_id()
        if form.custom_id.data:
            short_url = form.custom_id.data
            message, code = validate_short_id(short_url)
            if code != 200:
                flash(message)
                return render_template('content.html', form=form), code
        instance = URLMap(
            original=form.original_link.data,
            short=short_url,
        )
        db.session.add(instance)
        db.session.commit()
        url = urljoin(request.base_url, short_url)
        flash(Markup(
              f'<a href="{url}">{url}</a>'))
        return render_template('content.html', form=form)
    return render_template('content.html', form=form)


@app.route('/<string:slug>', methods=['GET'])
def short_url_view(slug):
    link = URLMap.query.filter_by(short=slug).first()
    if link is not None:
        return redirect(link.original), 302
    abort(404)
