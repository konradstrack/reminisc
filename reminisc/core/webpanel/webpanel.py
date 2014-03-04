from flask import Flask, render_template

app = Flask(__name__)
storage = None  # TODO: I'm not sure if this being None is the greatest idea on earth


def start():
    app.run()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/account/<handle>/messages')
def messages(handle):
    msgs = storage.get_messages(handle)
    return render_template('messages.html', messages=msgs, account=handle)