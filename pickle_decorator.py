# Persistent reuse of function call results
# Mistral Large
from time import sleep

import os
import pickle
from functools import wraps
from collections import deque
from typing import Deque

# Create a dictionary to store the caches of all functions
caches = {}

def cache_results(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        # Create a unique key for each combination of function and arguments
        key = f"{function.__name__}_{hash(args)}_{hash(frozenset(kwargs.items()))}"

        if function.__name__ not in caches:
            caches[function.__name__] = {}

        if key in caches[function.__name__]:
            # If the key is in the cache, return the cached result
            return caches[function.__name__][key]
        else:
            # If the key is not in the cache, call the function and cache the result
            result = function(*args, **kwargs)

            # Add the result to the cache
            caches[function.__name__][key] = result

            # If the number of caches exceeds the limit, remove the oldest cache
            if len(caches[function.__name__]) > 3:
                oldest_key = next(iter(caches[function.__name__]))
                del caches[function.__name__][oldest_key]

        return result

    return wrapper

def save_caches():
    # Save the caches to a pickle file
    with open("caches.pickle", "wb") as f:
        pickle.dump(caches, f)

def load_caches():
    global caches

    # Check if the pickle file exists
    if os.path.exists("caches.pickle"):
        # If the pickle file exists, load the caches from the file
        with open("caches.pickle", "rb") as f:
            caches = pickle.load(f)



load_caches()

@cache_results
def long_computation(seconds):
	sleep(seconds)
	return seconds

print(long_computation(3))
print(long_computation(3))

save_caches()