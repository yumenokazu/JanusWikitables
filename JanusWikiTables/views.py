from flask import request, render_template, Markup


from JanusWikiTables import app
from JanusWikiTables.table_gen import get_table_html
from JanusWikiTables.exceptions import NoTableFoundException, HTTPStatusError


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def domain_form():
    lang = request.form['lang_input']
    page = request.form['page_input']
    url = f"https://{lang}.wikipedia.org/wiki/{page}"
    try:
        table = Markup(get_table_html(url))
        return render_template('index.html', table=table)
    except HTTPStatusError as e:
        return render_template('index.html', error=e)
    except NoTableFoundException as e:
        return render_template('index.html', error=e)


