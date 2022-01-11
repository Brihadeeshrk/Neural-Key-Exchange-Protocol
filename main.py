from tpm import *
from cryptography.fernet import Fernet

# import hashlib
# import base64
# import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

print("Enter the word you want to encrypt\n")
ui = raw_input()

N = 4  # Number of input neurons per hidden neuron
K = 128  # Number of neurons in hidden layer
L = 1  # Range of values that weights can take {-L, ..., L}

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

# Print final weights
print(a.weights)
print(b.weights)

# Check whether weights are the same
for i in range(len(a.weights)):
    if a.weights[i] != b.weights[i]:
        print("Weights have not synced.")
        exit()
print("Weights have synced.")

# ------------------------------
# now, the code works until here, now i need to find a way to make the weights into a 'Key'

key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(ui)

print("ENCRYPTED DATA: \n\n", token)

token = f.decrypt(token)
print("DECRYPTED DATA: \n\n", token)
