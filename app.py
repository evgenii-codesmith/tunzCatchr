from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tunes.db'
db = SQLAlchemy(app)

class Tune(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    downloaded = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Tune %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')



if __name__=='__main__':
    app.run(debug=True)