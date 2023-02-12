"""
Another example to run function of Modal
"""

import sys

import modal

# Everything will be run inside this stub
stub = modal.Stub("example-hello-world")


# Define a Modal function
# cloud code
@stub.function
def f(i):
    if i % 2 == 0:
        print("hello", i, file=sys.stdout)
    else:
        print("world", i, file=sys.stderr)

    return i * i


# local code
@stub.local_entrypoint
def main():
    # Call the function directly.
    print(f.call(1000))

    # Parallel map.
    total = 0
    for ret in f.map(range(20)):
        total += ret

    print(total)

