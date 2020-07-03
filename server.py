#!/usr/bin/env python

from bottle import get, run, request
import subprocess
import re

def form_template(term=''):
    return '''
      <form action="/search" method="GET">
        <input type="text" name="q" placeholder="Search keyword" value="{value}"/>
        <input type=submit>
      </form>
      <hr />
    '''.format(value=term)

def search_man(terms):
    try:
        result = subprocess.check_output(['apropos', terms]).decode('utf-8').strip()
        manpages = [re.split('\s+\-\s+', manpage) for manpage in result.split('\n')]
        structured_manpages = [{ 'title': re.sub('\s+\(\w+\)', '', manpage[0]), 'description': manpage[1] } for manpage in manpages]
        return structured_manpages
    except:
        return False

def dtdd(structured_manpage):
    return '''
        <dt><a href="/man/{title}">{title}</a></dt>
        <dd>{description}</dd>
    '''.format(**structured_manpage)

@get('/')
def index():
    return form_template()

@get('/search')
def search():
    page = request.query.q or 'man'
    manpages = search_man(page)
    html = form_template(term=page)

    if not manpages:
        return html + '<pre>Not found</pre>'

    manpage_list = '\n'.join([dtdd(manpage) for manpage in manpages])
    html += '<dl>{result}</dl>'.format(result=manpage_list)

    return html

@get('/man/<page>')
def man(page):
    html = form_template(term=page)

    try:
        manpage = subprocess.check_output(['man', '-Thtml', page]).decode('utf-8')
        return manpage
    except:
        return html + '<pre>Not found</pre>'


run(host='localhost', port=8080, debug=True)
