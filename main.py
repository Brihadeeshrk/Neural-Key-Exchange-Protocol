import hashlib
from tpm import *
from cryptography.fernet import Fernet

import hashlib
import os
import binascii
import base64


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


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    pwdhash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 200000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode("ascii")


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    pwdhash = hashlib.pbkdf2_hmac(
        "sha512", provided_password.encode("utf-8"), salt.encode("ascii"), 200000
    )
    stored_password = stored_password[64:]
    pwdhash = binascii.hexlify(pwdhash).decode("ascii")
    return pwdhash == stored_password


strWeight = "".join([str(x) for x in a.weights])
# base64_bytes = base64.b64encode(strWeight)

hp = hash_password(base64_bytes)
print(hp)
x = verify_password(
    hp,
    "111"
)
y = verify_password(hp, "1111")
print(x,y)

# # m = hashlib.sha512()
# # m.update(strWeight)
# salt = os.urandom(32)
# dk = hashlib.pbkdf2_hmac("sha512", strWeight.encode("utf-8"), salt, 200000)

# print(dk.hex())
# key = Fernet.generate_key()
# f = Fernet(m.copy())
# token = f.encrypt(ui)

# print("ENCRYPTED DATA: \n\n", token)

# token = f.decrypt(token)
# print("DECRYPTED DATA: \n\n", token)
