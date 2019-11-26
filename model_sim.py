import random

def main():
    return random.choice([True, False])

def ballInFrame(frame):
    return random.choice([True, True])

def ballInHoop(frame):
    return random.choice([True, True, False])

if __name__ == '__main__':
    main()