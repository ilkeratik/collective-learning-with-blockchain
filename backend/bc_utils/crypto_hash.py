
import hashlib
import json
import numpy as np
def crypto_hash(*args): 
    """
    Return a sha-256 hash of the given arguments.
    """
    json_data = json.dumps(args, 
                        sort_keys=True,
                       cls=NumpyEncoder)
    return hashlib.sha256(json_data.encode("utf-8")).hexdigest() #should be encoded first, return the digest result in base 16(up to 64 characters).

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main(): #test purpose
    print(f"crypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
    main()
