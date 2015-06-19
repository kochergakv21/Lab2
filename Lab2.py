
from flask import Flask, jsonify, render_template, request
import random
import time
import string
app = Flask(__name__,  static_url_path='')


Row = ''
RowIndex = 0
RowN = 1
N = 204800
FirstText = ''
SecondText = ''
ComputationTime = 0
UsersOnline = 0
CurrentIndex = 0
isFinished = False
isBegin = True
Count = 0


def generate_random_texts(n):
    """Generates random texts for computing."""
    assert n >= 0
    global FirstText, SecondText
    FirstText = str("".join([random.choice(string.letters[:26]) for i in xrange(n)]))
    SecondText = str("".join([random.choice(string.letters[:26]) for i in xrange(n)]))

@app.route('/calculate_current')
def calculate():
    """Return current data for calculation(borders of calculation for client)."""
    print 'AJAX getJSON request to get current data and begin compute on new client'
    global isBegin, CurrentIndex, isFinished, ComputationTime, N, Row, RowIndex
    if isBegin:
        generate_random_texts(N)
        ComputationTime = time.time()
        RowIndex = (RowN - 1) * 256
        Row = FirstText[RowIndex:RowIndex + 255]
        part = SecondText[CurrentIndex:CurrentIndex+1024]
        isBegin = False
    else:
        Row = FirstText[RowIndex:RowIndex + 255]
        part = SecondText[CurrentIndex:CurrentIndex+1024]
    if isFinished:
        Row = ''
        part = ''
    return jsonify(current_row=Row, current_part=part)


@app.route('/online')
def online():
    """Returns number of online clients."""
    global UsersOnline
    print 'AJAX request to get online user count; users online now: ', UsersOnline
    return jsonify(result=UsersOnline)


@app.route('/users_online')
def users_online():
    """Renders page, that displaying number of online clients."""
    return render_template('online.html')


@app.route('/watch_worker', methods=['POST'])
def watch_worker():
    """Watch current worker state."""
    global isFinished, ComputationTime, UsersOnline, N, CurrentIndex, Count
    received_data = request.json
    Count += received_data
    if CurrentIndex >= N:
        print 'Second text got ', Count, ' entries of given row.'
        print '--- %s seconds ---' % (time.time() - ComputationTime)
        isFinished = True
        return jsonify(current_row='', current_part='')
    else:
        print 'Current row in second text: ', CurrentIndex / 256
        part = SecondText[CurrentIndex:CurrentIndex+1023]
        CurrentIndex += 1024
        return jsonify(current_row=Row, current_part=part)



@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders main page. Case work is finished returns alert message."""
    global isFinished
    if isFinished:
        return 'Computation is finished. Nothing to do.'
    return render_template('index.html')


@app.route('/mark_online', methods=['POST'])
def mark_online():
    """Marks client online."""
    user_id = request.remote_addr
    # mark user, before worker started
    global UsersOnline
    UsersOnline += 1
    print 'AJAX POST client registered: ', user_id
    return jsonify(result=user_id)


@app.route('/mark_offline', methods=['POST'])
def mark_offline():
    """Marks client offline."""
    user_id = request.remote_addr
    global UsersOnline
    if UsersOnline != 0:
        UsersOnline -= 1
        print 'AJAX POST client gone offline: ', user_id
    return jsonify(result=user_id)


@app.route('/input_custom_data')
def custom_data():
    return render_template('input_custom_data.html')


@app.route('/custom_data')
def custom_data_try():
    data = request.args.get('a', 0, type=str)
    global RowN
    try:
        data_test = int(data)
        if 0 < int(data) < N / 256:
            print 'Input data saved.'
    except ValueError:
        print 'Value Error: input data is not acceptable.'
        return jsonify(result=0)
    RowN = int(data)
    print 'Custom data input: ', RowN
    return jsonify(result=RowN)


@app.route('/get_res')
def get_res():
    global Count
    return jsonify(result=Count)


if __name__ == "__main__":
    app.run(host='0.0.0.0')  # making server visible across local network for test purposes
