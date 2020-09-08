import subprocess
import settings
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(settings.FLASK_CONFIG)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search', methods=['POST'])
def search():
    from models import Result, Task
    url = request.form['url']
    keyword = request.form['keyword']
    task = Task(url=url, keyword=keyword)
    db.session.add(task)
    db.session.commit()
    subprocess.check_output([
        'scrapy', 'runspider', 'crawler.py',
        "-a", "url=%s" % url,
        "-a", "task_id=%d" % task.id,
        "-a", "keyword=%s" % keyword
    ])

    db.session.rollback()
    results = Result.query.filter_by(task_id=task.id).all()
    return render_template('search.html', **locals())


if __name__ == '__main__':
    from models import *
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0', port='5000')