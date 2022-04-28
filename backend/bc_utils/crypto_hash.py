
import hashlib
import json

def crypto_hash(*args): 
    """
    Return a sha-256 hash of the given arguments.
    --Order of arguments doesn't matter as long as content is the same.
    """
    stringified_args = map(json.dumps, args)
    #stringified_args = sorted(map(lambda data: json.dumps(data), args)) #it wil supply same hash for different ordered same arguments
    #joined_data = ''.join(stringified_args) #concat'em all, in this case (12, 34, 56) and (123, 4, 56) will have the same hash result
    joined_data = '^'.join(stringified_args) #concat'em all
    
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest() #should be encoded first, return the digest result in base 16(up to 64 characters).

def main(): #test purpose
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
    main()