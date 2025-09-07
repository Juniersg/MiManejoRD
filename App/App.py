from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        'Titulo': 'Index',
        'Porcentaje': 34 / 100
    }
    return render_template('index.html', data = data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

