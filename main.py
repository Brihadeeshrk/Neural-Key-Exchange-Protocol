from tpm import *
from cryptography.fernet import Fernet
import hashlib
import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

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

print(hashlib.algorithms_available)

# convert weights to base64
weights64 = "".join([str(c) for c in a.weights])
base64_bytes = base64.b64encode(weights64)

password = weights64
salt = os.urandom(16)

#kdf = PBKDF2HMAC(
#    algorithm=hashes.SHA256(),
#    length=32,
#    salt=salt,
#    iterations=390000,
#    backend=default_backend(),
#)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

# print("STRING: \n\n", weightStr)
# f = Fernet(key)
# token = f.encrypt(b"my deep dark secret")
# print(token)
# token = f.decrypt(token)
# print("after\n")
# print(token)

k = hashlib.sha256()
# print(hashlib.algorithms_available)
# # k.update(a.weights)
# k.update(base64_bytes)

# key = k.digest()
print(key)

# f = Fernet(key)
user_input = input("Enter the String you want to Encrypt: \n")
token = f.encrypt(user_input)

print("token: \n\n")
print(token)
