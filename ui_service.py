from flask import Flask, render_template, request, redirect, url_for, abort
import requests

app = Flask(__name__)

POST_SERVICE_URL = 'http://localhost:5000/api/posts'

@app.route('/')
def index():
    try:
        response = requests.get(POST_SERVICE_URL)
        response.raise_for_status()
        posts = response.json()
    except requests.RequestException:
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    try:
        response = requests.get(f'{POST_SERVICE_URL}/{post_id}')
        response.raise_for_status()
        post = response.json()
    except requests.RequestException:
        abort(404)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = {'title': title, 'content': content}
        try:
            response = requests.post(POST_SERVICE_URL, json=new_post)
            response.raise_for_status()
        except requests.RequestException:
            abort(500)
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:post_id>', methods=('GET', 'POST'))
def update(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        updated_post = {'title': title, 'content': content}
        try:
            response = requests.put(f'{POST_SERVICE_URL}/{post_id}', json=updated_post)
            response.raise_for_status()
        except requests.RequestException:
            abort(500)
        return redirect(url_for('index'))
    else:
        try:
            response = requests.get(f'{POST_SERVICE_URL}/{post_id}')
            response.raise_for_status()
            post = response.json()
        except requests.RequestException:
            abort(404)
        return render_template('update.html', post=post)

@app.route('/delete/<int:post_id>', methods=('POST',))
def delete(post_id):
    try:
        response = requests.delete(f'{POST_SERVICE_URL}/{post_id}')
        response.raise_for_status()
    except requests.RequestException:
        abort(500)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001)
