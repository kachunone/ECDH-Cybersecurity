A python program using ECDH (Elliptic Curve Diffie–Hellman key Exchange) to encrypt and decrypt messages transmitting under HTTP requests

STEP 1: we need to run 2 flask apps at the same time to simulate a communication platform. Each port represents a client.

STEP 2: port 5000 sends its public key and combinekey to port 5001 by sending a request:
        http://127.0.0.1:5000/send_keys

STEP 3: port 5001 sends its public key and combinekey to port 5000 by sending a request:
        http://127.0.0.1:5001/send_keys

STEP 4: show all the data of a port by sending requests:
        http://127.0.0.1:5000/show, and http://127.0.0.1:5001/show
        
        The share key will show on its own terminal rather than on the web page,
        so others cannot see it even using WireShark.

STEP 5: port 5000 sends an encoded message to port 5001 by sending a request:
        http://127.0.0.1:5000/send_msg

STEP 6: port 5001 decoded message by sending a request:
        http://127.0.0.1:5001/decrypt_msg

The decoded message will show on its own terminal rather than on the web page,
so others cannot see it even using WireShark.
