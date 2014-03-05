from flask import Flask, render_template

app = Flask(__name__)
storage = None  # TODO: I'm not sure if this being None is the greatest idea on earth


def start():
    app.run()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/accounts')
def accounts():
    account_list = storage.get_accounts()
    return render_template('accounts.html', accounts=account_list)


@app.route('/account/<handle>/messages')
def messages(handle):
    msgs = storage.get_messages(handle)
    return render_template('messages.html', messages=msgs, account=handle)