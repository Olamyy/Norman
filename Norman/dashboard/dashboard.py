from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@app.route('/create-user')
def create_user():
    return render_template('admin/create-user.html')


@app.route('/view-users')
def view_users():
    return render_template('admin/view-users.html')


if __name__ == '__main__':
    app.run()
