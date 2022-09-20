import collections
import matplotlib.pyplot as py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import json
import requests
from flask import Flask, jsonify, request
import base64
app = Flask(__name__)
app2 = Flask(__name__)
Coord = collections.namedtuple("Coord", ["x", "y"])
a = -1; b = 3; q = 31

def modular_inverse(n, q):
    for i in range(q):
        if (n * i % q) == 1:
            return i

def add(pa, pb):
    zero = Coord(0, 0)
    if pa == zero: return pb
    if pb == zero: return pa
    if pa.x == pb.x and (pa.y != pb.y or pa.y == 0): return zero

    if pa.x == pb.x:
        m = (3 * pa.x * pa.x + a) * modular_inverse(2 * pa.y, q) % q
    else:
        m = (pb.y - pa.y) * modular_inverse(pb.x - pa.x, q) % q
    x = (m * m - pa.x - pb.x) % q
    y = (m * (pa.x - x) - pa.y) % q
    return Coord(x, y)

def ml(p, k):  # Montgomery Ladder (ML)
    p0 = Coord(0, 0)
    p1 = p
    while k > 0:
        if k & 1 == 1:  # odd
            p0 = add(p0, p1)
        k = k >> 1  # =int(n/2)
        p1 = add(p1, p1)
    return p0

def generate_publicKey():
    py.style.use('seaborn-whitegrid')
    Coord = collections.namedtuple("Coord", ["x", "y"])
    points = []  # saving possible points in this curve

    # Compute EC within [1,q]
    for x in range(1, q + 1):
        for y in range(1, q + 1):
            y0 = (y ** 2 - (x ** 3 + a * x + b)) % q
            if y0 == 0:
                points.append(Coord(x, y))
                py.plot(x, y, 'o', markersize=4, fillstyle='none', color='black')
    return points[0]


def encryption(shared, msg):
    shared = str(shared[0]) + str(shared[1])  # convert sharekey to string
    while 1:
        shared += shared
        if len(shared) >= 16:
            break
    key = shared.encode("utf-8")  # string to byte
    # convert the share key to 16 byte format
    key = padding.PKCS7(128).padder().update(key)
    key += padding.PKCS7(128).padder().finalize()
    aesCipher = Cipher(algorithms.AES(key), modes.ECB(),
                       backend=default_backend())
    aesEncryptor = aesCipher.encryptor()
    padder = padding.ANSIX923(128).padder()

    msg = msg.encode("utf-8")

    padded_msg = padder.update(msg)
    padded_msg += padder.finalize()

    enc_msg = aesEncryptor.update(padded_msg)
    enc_msg += aesEncryptor.finalize()
    enc_msg = base64.b64encode(enc_msg)  # byte to base64-byte
    enc_msg = enc_msg.decode("UTF-8")  # base64-byte to string
    return enc_msg  # string

def decryption(shared, enc_msg):
    shared = str(shared[0]) + str(shared[1])
    while 1:
        shared += shared
        if len(shared) >= 16:
            break
    key = shared.encode("utf-8")
    # convert the share key to 16 byte format
    key = padding.PKCS7(128).padder().update(key)
    key += padding.PKCS7(128).padder().finalize()

    aesCipher = Cipher(algorithms.AES(key), modes.ECB(),
                       backend=default_backend())
    aesDecryptor = aesCipher.decryptor()
    unpadder = padding.ANSIX923(128).unpadder()

    enc_msg = enc_msg.encode("utf-8")
    enc_msg = base64.b64decode(enc_msg)

    padded_msg = aesDecryptor.update(enc_msg)
    padded_msg += aesDecryptor.finalize()
    dec_msg = unpadder.update(padded_msg)
    dec_msg += unpadder.finalize()
    dec_msg = dec_msg.decode("utf-8")

    return dec_msg

@app.route('/get_keys', methods=['POST'])
def get_keys():
    data = request.form
    pubkey_x = int(json.loads(data.get('publicKey'))['x'])
    pubkey_y = int(json.loads(data.get('publicKey'))['y'])
    comkey_x = int(json.loads(data.get('combineKey'))['x'])
    comkey_y = int(json.loads(data.get('combineKey'))['y'])
    myData.publicKey = Coord(pubkey_x, pubkey_y)
    myData.combineKey = Coord(comkey_x, comkey_y)

    # calculate sharekey and store to dataset
    myData.shared_key = ml(myData.combineKey, myPriKey)
    return 'keys are accepted', 201

@app.route('/send_keys', methods=['GET'])
def send_keys():
    info = {'publicKey': publicKey,
            'combineKey': combineKey, }
    requests.post('http://' + '127.0.0.1:' + str(anotherPort) + '/get_keys', data=info)
    return "your keys are sent", 201

@app.route('/show', methods=['GET'])
def show():
    response = {
        'combine': myData.combineKey,
        'publicKey': myData.publicKey,
        'enc_msg': myData.enc_msg,
    }
    
    # print share key on our own terminal only, 
    # so that others cannot see by using Wireshark
    
    print("share key: ", myData.shared_key)
    return response, 201

@app.route('/decrypt_msg', methods=['GET'])
def decrypt_msg():
    myData.dec_msg = decryption(myData.shared_key, myData.enc_msg)
    
    # print decode message on our own terminal only, 
    # so that others cannot see even using Wireshark

    print("decode message ", myData.dec_msg)
    return "message is decoded", 201

@app.route('/send_msg', methods=['GET'])
def send_msg():
    myData.enc_msg = encryption(myData.shared_key, message)
    info = {'enc_msg': myData.enc_msg, }
    requests.post('http://' + '127.0.0.1:' + str(anotherPort) + '/get_enc_msg', data=info)
    return "Your encoded message is sent", 201

@app.route('/get_enc_msg', methods=['POST'])
def get_enc_msg():
    data = request.form
    myData.enc_msg = data.get('enc_msg')
    return 'encoded message is accepted', 201

class DataSet:
    publicKey = None
    combineKey = None
    shared_key = None
    enc_msg = None
    dec_msg = None

if __name__ == '__main__':
    myData = DataSet()
    publicKey = generate_publicKey()  # generate publicKey
    myPriKey = 4564  # generate priKey
    myCombineKey = ml(publicKey, myPriKey)  # generate combineKey

    publicKey = json.dumps(publicKey._asdict())
    combineKey = json.dumps(myCombineKey._asdict())

    message = "This is a secret message from port 5001!"

    port = 5001
    anotherPort = 5000
    app.run(host='127.0.0.1', port=port)