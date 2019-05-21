import random
import time


'''
power(base, exp, mod):
    n = 1;
    while exp > 0 
        if exp % 2 != 0
            n = (n * base) % mod
        exp = exp / 2
        base = (base * base) % mod
    return n;
'''


#Fast Exponentiation
def power(x, y, z):
    #(x ** y) % z
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number


def generate_prime(bits):  # generate the prime number - p e q
    if 255 < bits < 2049:
        while True:
            prime = random.getrandbits(bits)
            if isPrime(prime):
                return prime


# Miller-Rabin test
def isPrime(n):
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1 #bitwise division by 2
        s += 1
    assert (d == (n-1) // pow(2, s))

    def trial_composite(a):
        #a ^ d ≡ ? mod n
        #if ? == 1 the number is not composite
        if power(a, d, n) == 1:
            return False

        # a ^ (2*i * d) ≡ ? mod n
        # if ? == n - 1 the number is not composite
        for i in range(s):
            if power(a, pow(2, i) * d, n) == n - 1:
                return False

        #otherwise, the number is composite
        return True

    # number of trials
    for i in range(8):
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


def generate_e(phi):  # recives totient of N as a parameter
    def mcd(n1, n2):  # compute the MCD of the phi and e
        rest = 1
        while (n2 != 0):
            rest = n1 % n2
            n1 = n2
            n2 = rest

        return n1

    while True:
        e = random.randrange(2, phi)  #retrieve a random number in the range 2 < x < phi(n)
        if (mcd(phi, e) == 1):
            return e


def mod(a, b):  # mod function
    if a < b:
        return a
    else:
        c = a % b
        return c


def encrypt(message, public_key):
    n, e = public_key

    message_ascii = [ord(letter) for letter in message]
    message_cypher = [str(power(letter_ascii, e, n)) for letter_ascii in message_ascii] #letter ^ e mod n

    return ' '.join(message_cypher)


def decrypt(cipher_text, n, d):
    cipher = cipher_text.split(' ')

    ascii_message = [power(int(cipher_char), d, n) for cipher_char in cipher] #cipher_char ^ d mod n
    final_message = [chr(ascii_char) for ascii_char in ascii_message]

    return ''.join(final_message)


def private_key(phi, e):
    #remainder
    r = e
    r2 = phi
    temp_r = r

    #quocient
    q = 0

    #pkey field 1
    x2 = 1
    x = 0
    temp_x = x

    #pkey field 2
    y2 = 0
    y = 1
    temp_y = y

    while True:
        q = r2 // r
        r = r2 % r
        r2 = temp_r
        temp_r = r

        x = x2 - (q * x)
        x2 = temp_x
        temp_x = x

        y = y2 - (q * y)
        y2 = temp_y
        temp_y = y

        if r == 1:
            assert (1 == (phi * x) + (e * y))
            return y


if __name__ == '__main__':
    text = input("Insert message: ")

    # Prime generation
    start = time.time()
    p = generate_prime(1024)
    q = generate_prime(1024)
    end = time.time()
    print("\nPrimes generated in " + str(end - start) + " seconds.")

    # Phi generation
    phi = (p - 1) * (q - 1)  # compute the totient of n

    # Public key generation
    start = time.time()
    n = p * q
    e = generate_e(phi)  # generate e
    public_key = (n, e)
    end = time.time()
    print("Public Key generated in " + str(end - start) + " seconds.")

    # Private key generation
    start = time.time()
    private_key = private_key(phi, e)  # EEA
    end = time.time()
    print("Private Key generated in " + str(end - start) + " seconds.")

    # Encryption
    start = time.time()
    cipher_text = encrypt(text, public_key)
    end = time.time()
    print("Message encrypted in " + str(end - start) + " seconds.")

    # Decryption
    start = time.time()
    plain_text = decrypt(cipher_text, n, private_key)
    end = time.time()
    print("Message decrypted in " + str(end - start) + " seconds.\n")

    # Results
    print('Public Key:', public_key)
    print('Private Key:', private_key)
    print('Cipher Text:', cipher_text)
    print('Plain Text:', plain_text)