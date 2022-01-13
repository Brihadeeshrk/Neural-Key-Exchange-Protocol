from tpm import TPM
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import socket


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def server_program():
    weightsFlag = False
    weight_alert = ""
    N = 101      # Number of input neurons per hidden neuron
    K = 2        # Number of neurons in hidden layer
    L = 3        # Range of values that weights can take {-L, ..., L}

    # Create two tree parity machines
    a = TPM(N, K, L)
    b = TPM(N, K, L)

    # Generate random weights for both machines
    a.randomWeights()
    b.randomWeights()

    # Perform syncing for key exchange
    count = 0
    while True and count < 500:
        # Create random inputs (same inputs for both machines)
        a.randomInputs()
        b.inputs = a.inputs

        # Calculate outputs for both machines
        a.calcWeights2()
        a.tow()

        b.calcWeights2()
        b.tow()

        # Perform Hebbian learning if outputs are the same
        if a.output == b.output:
            a.HebbianLearning(a.output, b.output)
            b.HebbianLearning(b.output, a.output)
        count += 1

    # Check whether weights are the same
    for i in range(len(a.weights)):
        if a.weights[i] != b.weights[i]:
            weightsFlag = False
            exit()
    weightsFlag = True

    # Create
    l = ''.join([str(x) for x in a.weights])

    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(l.encode()))
    print("KEY: ", key)
    f = Fernet(key)

    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    if weightsFlag:
        weight_alert = "\n{}WEIGHTS SYNCED{}".format(
            bcolors.OKBLUE, bcolors.ENDC)
    else:
        weight_alert = "\n{}WEIGHTS HAVE NOT SYNCED{}".format(
            bcolors.WARNING, bcolors.ENDC)
    while True:
        conn.send(weight_alert.encode())  # send weights alert to the client
        # receive data stream. it won't accept data packet greater than 1024 bytes

        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("Message to be Encrypted: " + str(data))
        token = str(data)
        enc_data = f.encrypt(token.encode())
        print("Encoded Message:\t", enc_data)
        dec_data = f.decrypt(f.encrypt(token.encode())).decode()
        print("Decoded Message:\t", dec_data)
        # data = "Decoded Message:\t", f.decrypt(
        #     f.encrypt(token.encode())).decode()
        data = "Encrypted Message: {}".format(enc_data)
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
