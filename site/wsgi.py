from flask import Flask, render_template
from danmu.redis import RedisClient

app = Flask(__name__)

redis_client = RedisClient()


@app.route('/')
def home():
    meta = redis_client.load_meta()

    return render_template('home.html', meta=meta)


@app.route('/room/<int:rid>')
def live(rid):
    return render_template('live.html')


if __name__ == '__main__':
    app.run(debug=True)
