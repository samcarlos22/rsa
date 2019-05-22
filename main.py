import random
import time


#Fast (Squared) Exponentiation
def power(base, exp, mod):
    #(base ^ exponent) % mod
    result = 1
    while exp: #exp > 0
        if exp & 1: #exp mod 2 != 0
            result = result * base % mod
        exp >>= 1 #exp / 2
        base = base * base % mod
    return result


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


def generate_e(phi):  # recives phi(n) as a parameter
    def mcd(n1, n2):  # compute the MCD of the phi and e
        rest = 1
        while n2 != 0:
            rest = n1 % n2
            n1 = n2
            n2 = rest

        return n1

    while True:
        e = random.randrange(2, phi)  #retrieve a random number in the range 2 < x < phi(n)
        if mcd(phi, e) == 1:
            return e


def encrypt(message, public_key):
    n, e = public_key

    message_ascii = [ord(letter) for letter in message]
    message_cypher = [str(power(letter_ascii, e, n)) for letter_ascii in message_ascii] #letter ^ e mod n

    return ' '.join(message_cypher)


#Decryption using Chinese Remainder Theorem (CRT)
def decrypt(cipher_text, p, q, d):
    cipher_text = cipher_text.split()
    m = ''

    x, y = eea(p, q)

    for cipher in cipher_text:
        mp = power(int(cipher), d % (p - 1), p)  # c1 = c ^ pow(d,(p-1) mod p
        mq = power(int(cipher), d % (q - 1), q)  # c2 = c ^ pow(d,(q-1) mod q
        m += chr(mp * x * p + mq * y * q)

    return m


#Extended Euclidian Algorithm
def eea(prime1, prime2):
    a = prime1
    b = prime2
    prevx, x = 1, 0;
    prevy, y = 0, 1
    while b:
        q = a // b
        x, prevx = (prevx - q * x), x
        y, prevy = (prevy - q * y), y
        a, b = b, a % b
    assert (1 == (prime1 * prevx) + (prime2 * prevy))
    return prevx, prevy


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
    private_key = eea(phi, e)  # EEA
    end = time.time()
    print("Private Key generated in " + str(end - start) + " seconds.")

    # Encryption
    start = time.time()
    cipher_text = encrypt(text, public_key)
    end = time.time()
    print("Message encrypted in " + str(end - start) + " seconds.")

    # Decryption
    start = time.time()
    plain_text = decrypt(cipher_text, p, q, private_key[1])
    end = time.time()
    print("Message decrypted in " + str(end - start) + " seconds.\n")

    # Results
    print('Public Key:', public_key)
    print('Private Key:', private_key[1]) #[0] = x , [1] = y = d
    print('Cipher Text:', cipher_text)
    print('Plain Text:', plain_text)