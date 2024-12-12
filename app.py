from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import timezone, datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['priority']
        date_created = datetime.now(timezone.utc)
        todos.insert_one(
            {'content': content, 'priority': degree, 'complete': False, 'date': date_created})
        return redirect(url_for('index'))

    all_todos = todos.find()
    all_todos.collation({'locale': 'en'})  # set english locale
    all_todos.sort('content')
    return render_template('index.html', todos=all_todos)  # add todos here!


@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


@app.post('/<id>/complete/')
def complete(id):
    filter = {'_id': ObjectId(id)}
    new_values = {'$set': {'complete': True}}
    todos.update_one(filter, new_values)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
