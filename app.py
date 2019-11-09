from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from url_parse import get_tune_data
from file_download import get_file_from_youtube
import multiprocessing

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tunes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tune(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), unique=True, nullable=False)
    artist = db.Column(db.String(100), nullable=True)
    tune_name = db.Column(db.String(100), nullable=True)
    audio_file_format = db.Column(db.String(10), nullable=True)
    downloaded = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Tune %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tune_url = request.form['url']
        artist, tune_name = get_tune_data(tune_url)
        new_tune = Tune(url=tune_url, artist=artist, tune_name=tune_name)
        try:
            db.session.add(new_tune)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return redirect('/')

    else:
        all_tunes = Tune.query.order_by(Tune.date_created).all()
        return render_template('index.html', tunes=all_tunes)


@app.route('/delete/<int:id>')
def delete(id):
    target_tune = Tune.query.get_or_404(id)
    try:
        db.session.delete(target_tune)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return e


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    target_tune = Tune.query.get_or_404(id)

    if request.method == 'POST':
        target_tune.url = request.form['new_url']
        target_tune.artist = request.form['new_artist']
        target_tune.tune_name = request.form['new_tune_name']
        downloaded = request.form['downloaded']

        if downloaded == 'Yes':
            target_tune.downloaded = True
        elif downloaded == 'No':
            if target_tune.downloaded:
                target_tune.downloaded = False

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return e
    else:
        return render_template('update.html', tune=target_tune)


@app.route('/download/<int:id>', methods=['GET'])
def download(id):
    target_tune = Tune.query.get_or_404(id)
    p = multiprocessing.Process(
        target=get_file_from_youtube, args=(db, target_tune, 'flac', '0'))
    p.start()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
