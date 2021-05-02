import os

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
    json
)

from datetime import datetime

RESET_TO='admin1234'
USER_CONF="/Users/bongkyo/git/bnd/camr/config.json"
DMS_CONF="/Users/bongkyo/git/bnd/camr/dmsconfig.json"
SYS_INFO="/Users/bongkyo/git/bnd/camr/sysinfo.json"

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



# app = Flask(__name__, static_url_path='')
app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

def is_on(val):
    if val == 1:
        return 'is-success'
    else:
        return ''

def get_sensitivity(val, curlevel):
    if val == curlevel:
        return 'is-success'
    else:
        return ''

app.jinja_env.globals.update(is_on=is_on)
app.jinja_env.globals.update(get_sensitivity=get_sensitivity)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

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
    
    # SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    # json_url = os.path.join(SITE_ROOT, "static/data", "taiwan.json")
    # data = json.load(open(json_url))
    data = json.load(open(SYS_INFO))

    return render_template('systeminfo.html', jsonObj=data)

@app.route('/dmssetting', methods=['GET', 'POST'])
def dmssetting():
    if not g.user:
        return redirect(url_for('login'))

    data = json.load(open(DMS_CONF))
    
    return render_template('dmssetting.html', jsonObj=data)

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

@app.route('/api/curtime')
def curtime():
    return jsonify(datetime.now().timestamp())


@app.route('/api/updatetime', methods=['POST'])
def updatetime():
    targetTime = request.form['targetTime']
    return jsonify(targetTime)

@app.route('/api/resetpass', methods=['POST'])
def resetpass():
    data = json.load(open(USER_CONF))
    data['admin'] = RESET_TO
    with open(USER_CONF, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify("OK")

@app.route('/api/updatepass', methods=['POST'])
def updatepass():
    passwd = request.form['targetPass']
    data = json.load(open(USER_CONF))
    data['admin'] = passwd
    with open(USER_CONF, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify("OK")


@app.route('/api/update_dms_conf', methods=['POST'])
def update_dms_conf():

    dmsConfig = request.form['dmsConfig']

    with open(DMS_CONF, 'w', encoding='utf-8') as f:
        json.dump(dmsConfig, f, ensure_ascii=False, indent=4)
    return jsonify("OK")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)