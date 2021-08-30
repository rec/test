from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!</p>'

@app.route('/search/<two>')
def search(two):
    return f'<pre>search-{two}</pre>'

@app.route('/restrict/<three>/search')
def restrict1(three):
    return f'<pre>restrict1-{three}-search</pre>'

@app.route('/restrict/<three>')
def restrict2(three):
    return f'<pre>restrict2-{three}</pre>'

"""
Try these URLs:

http://127.0.0.1:5000
http://127.0.0.1:5000/search
http://127.0.0.1:5000/search/x
http://127.0.0.1:5000/restrict/one.com
http://127.0.0.1:5000/restrict/one.com/search

"""
