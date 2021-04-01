
import hashlib
import json

def crypto_hash(*args): 
    """
    Return a sha-256 hash of the given arguments.
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args)) #it wil supply same hash for different ordered same arguments
    joined_data = ''.join(stringified_args) #unify'em all

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest() #should be encoded first

def main(): #test purposed
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
    main()