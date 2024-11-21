# %%
from flask import Flask, render_template, send_from_directory
from dataclasses import dataclass
import os

app = Flask(__name__)



@app.route('/')
def home():  # put application's code here
    return render_template('index.html')

@app.route('/routes')
def routes():
    files = os.listdir('templates/maps/')
    files = sorted(files)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
        print('removed')
    for i in range(len(files)):
        files[i] = files[i].removesuffix('.html')
    

    return render_template('routes.html', files=files)


@app.route('/routes/<path:path>')
def map(path):  # put application's code here

    return send_from_directory('templates/maps',path=path)


if __name__ == '__main__':
    app.run()

# %%
