from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from url_parse import get_tune_data
from file_download import get_file_from_youtube

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tunes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tune(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100),nullable=True)
    tune_name = db.Column(db.String(100),nullable=True)
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
        except:
            return('Issue while adding a new tune')
        
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
    except:
        return 'Unable to delete tune %s' % id

@app.route('/update/<int:id>',methods = ['POST', 'GET'])
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
        except:
            return 'Unable to update'
    else:
        return render_template('update.html', tune=target_tune)

@app.route('/download/<int:id>', methods=['GET'])
def download(id):
    target_tune = Tune.query.get_or_404(id)
    proc = get_file_from_youtube(target_tune.url, 'mp3', '0')
    output, error = proc.communicate()
        
    if error:
        return error
    
    target_tune.downloaded = True
    
    try:
        db.session.commit()
        return '',204
    except:
        return 'Unable to update'

if __name__=='__main__':
    app.run(debug=True)