from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from time import sleep
import json
import serial
import socket

RST_INPUT = "000000000000"
FORWARD_MASK = "000100001000"
BACKWARD_MASK = "000001100000"
LEFT_MASK = "001000000000"
RIGHT_MASK = "000000000100"

USE_WIFI = True

mode = 'a'
# mode = 'r'

if not USE_WIFI:
    serialPort = ''
    if mode == 'a':
        serialPort = serial.Serial(
            port="/dev/ttyUSB0",
            baudrate=115200,
            bytesize=8,
            timeout=2,
            stopbits=serial.STOPBITS_ONE)

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///libray.db"
db.init_app(app)


class Sequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    period = db.Column(db.String)
    input = db.Column(JSON)

    def __init__(self, title, period, input):
        self.title = title
        self.period = period
        self.input = input

    def as_dict(self):
        return {c.title: getattr(self, c.title) for c in self.__table__.columns}


def create_socket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_ip = "192.168.0.22"
    server_port = 23

    client.connect((server_ip, server_port))

    return client

def run_client(message, client):
    try:
        client.send(message.encode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")

def get_mask(direction):
    if (direction == "F"):
        return FORWARD_MASK
    if (direction == "B"):
        return BACKWARD_MASK
    if (direction == "L"):
        return LEFT_MASK
    return RIGHT_MASK


def get_level(time):
    if (time > 4):
        return 7
    return 2


def create_monster_input(mask, level):
    res = ''
    for e in mask:
        res += str(int(e)*level)
    return res


@app.route('/listlibrary')
def list_libray():
    sequences = Sequence.query.all()
    library = []
    for sequence in sequences:
        library.append(
            {'id': sequence.id, 'title': sequence.title})
    print(library)
    return json.dumps({'success': True, 'message': library})


@app.route('/getinput', methods=['POST'])
def get_input():
    id = request.json['id']
    sequence = Sequence.query.filter_by(id=id).first()
    return json.dumps({'sucess': True, 'input': sequence.input, 'period': sequence.period})


@app.route('/libraryinput', methods=['POST'])
def lib_input():
    id = request.json['id'] if request.json['id'] else None
    sequence = Sequence.query.get(int(id))
    data = {'id': sequence.id, 'title': sequence.title,
            'period': sequence.period, 'input': sequence.input}
    client = create_socket()
    if mode == 'a':
        for state in data["input"]:
            if USE_WIFI:
                run_client(state, client)
            else:
                serialPort.write(bytes(state, 'utf-8'))

            print(state)
            sleep(float(data["period"]))
    return json.dumps({'sucess': True, 'message': f'Sequencia {data["title"]} executada'})


@app.route('/saveinput', methods=['POST'])
def save_input():
    title = request.json['title'] if request.json['title'] else None
    period = request.json['period'] if request.json['period'] else None
    input = request.json['input'] if request.json['input'] else None
    sequence = Sequence(title, period, input)
    db.session.add(sequence)
    db.session.commit()
    return json.dumps({'success': True, 'message': f'{Sequence.query.all()}'})


@app.route('/custominput', methods=['POST'])
def custom_input():
    input = request.json['input']
    period = float(request.json['period'])
    client = create_socket()
    if mode == 'a':
        for sequence in input:
            if USE_WIFI:
                run_client(sequence, client)
            else:
                serialPort.write(bytes(sequence, 'utf-8'))

            print(sequence)
            sleep(period)
    return json.dumps({'success': True, "message": f"Input recebido {input}, com periodo {period}"})


@app.route('/monsterinput', methods=['POST'])
def monster_input():
    time = request.json['intensity']
    direction = request.json['direction']
    level = get_level(time)
    mask = get_mask(direction)
    sequence = [create_monster_input(mask, level), RST_INPUT]
    client = create_socket()
    if mode == 'a':
        for state in sequence:
            if USE_WIFI:
                run_client(state, client)
            else:
                serialPort.write(bytes(state, 'utf-8'))

            print(state)
            sleep(time/10)
    return json.dumps({'success': True, "message": f"Sequencia monstro executada"})


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run()
