## ECDH Encryption and Decryption using Python Flask

This Python program demonstrates the usage of Elliptic Curve Diffie–Hellman (ECDH) key exchange for encrypting and decrypting messages transmitted via HTTP requests. The program utilizes two Flask applications running simultaneously to simulate a communication platform between two clients.

### Step 1: Running Flask Apps
To begin, run two Flask apps concurrently, each representing a client. Make sure to use different ports for each app.

### Step 2: Sending Public Key and Combined Key
Port 5000 sends its public key and combined key to port 5001 by sending an HTTP request to http://127.0.0.1:5000/send_keys.

### Step 3: Sending Public Key and Combined Key (Reverse)
Port 5001 sends its public key and combined key to port 5000 by sending an HTTP request to http://127.0.0.1:5001/send_keys.

### Step 4: Viewing Data
To view the data of a port, send requests to http://127.0.0.1:5000/show for port 5000 and http://127.0.0.1:5001/show for port 5001. The shared key will be displayed in the respective terminal, ensuring that it is not visible on the web page or through network monitoring tools like WireShark.

### Step 5: Sending Encoded Message
Port 5000 sends an encoded message to port 5001 by sending an HTTP request to http://127.0.0.1:5000/send_msg.

### Step 6: Decoding Message
Port 5001 decodes the received message by sending an HTTP request to http://127.0.0.1:5001/decrypt_msg. The decoded message will be displayed in the terminal, ensuring confidentiality even when using WireShark or similar tools.

## How to Run
1. Clone the repository and set up your Python environment.
2. Install Flask and any necessary dependencies.
3. Run both Flask apps concurrently, ensuring they use different ports.
4. Follow the steps outlined above to perform the ECDH encryption and decryption.

## Future Enhancements
- Improved User Interface: Develop a user-friendly interface for easy interaction with the application.
- Enhanced Security: Implement additional encryption techniques to further secure the communication.
- Error Handling: Enhance error handling and validation to handle various scenarios.

Feel free to contribute to this project and explore the powerful encryption capabilities provided by ECDH and Flask.
