from flask import Flask, render_template, request, redirect
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

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tune = request.form['content']
        new_tune = Tune(content=tune)
        
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
        target_tune.content = request.form['new_content']
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

if __name__=='__main__':
    app.run(debug=True)

