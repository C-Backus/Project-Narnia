from flask import Flask, render_template
from ssh import list_files

app = Flask(__name__)

@app.route('/')
def index():
    files = list_files()   #for ssh file list
    return render_template('index.html', files=files)  # loads templates/index.html

if __name__ == '__main__':
    app.run(debug=True)
