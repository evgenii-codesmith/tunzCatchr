from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    pass

print(__name__)
if __name__=='__main__':
    app.run(debug=True)