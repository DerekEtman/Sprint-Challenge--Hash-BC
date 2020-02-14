import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random



def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    proof = random.randint(1000000, 999999999)
    print("Checking")

    encoded_last_p = f"{last_proof}".encode()
    last_hash = hashlib.sha256(encoded_last_p).hexdigest()

    counter = 0

    while not valid_proof(last_hash, proof):
        proof = random.randint(1000000, 999999999)

        counter += 1

        if counter == 1000000:
            print(f"Mining.")
            if requests.get(url=node + "/last_proof").json()["proof"] != last_proof:
                print(f"already taken")
                counter = 0
                return None
            counter = 0

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?
    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

    # taking in proof and encoding it.
    encoded_new = f"{proof}".encode()

    # Converting encoded proof and changing it to sha256
    new_hash = hashlib.sha256(encoded_new).hexdigest()

    # Comparing first 6 chars to new_hash last 6 chars 
    return last_hash[-6:] == new_hash[:6]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        if new_proof is not None:
            post_data = {"proof": new_proof,
                         "id": id}

            r = requests.post(url=node + "/mine", json=post_data)
            data = r.json()
            print(data)
            if data.get('message') == 'New Block Forged':
                coins_mined += 1
                print("Total coins mined: " + str(coins_mined))
            else:
                print(data.get('message'))