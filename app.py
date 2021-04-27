from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from datetime import datetime

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='laon1234'))
users.append(User(id=2, username='bnd', password='bnd1234'))



app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('liveviewer'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/liveviewer')
def liveviewer():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('liveviewer.html')

@app.route('/systeminfo')
def systeminfo():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('systeminfo.html')

@app.route('/dmssetting', methods=['GET', 'POST'])
def dmssetting():
    if not g.user:
        return redirect(url_for('login'))



    
    return render_template('dmssetting.html')

@app.route('/timesetting', methods=['GET', 'POST'])
def timesetting():
    if not g.user:
        return redirect(url_for('login'))
    
    curtime = datetime.now()
    if request.method == 'POST':
        return redirect(url_for('timesetting'))

    return render_template('timesetting.html', curtime=curtime)

@app.route('/adminsetting', methods=['GET', 'POST'])
def adminsetting():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('adminsetting.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('test.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)