
import secrets
import time
from sympy import isprime

start = time.perf_counter()

# miller rabin test
def miller_rabin(n, k=40):
    # k means number of bases we test it against
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    d=n-1
    s=0

    while d % 2 == 0:
        d //= 2
        s += 1

    for i in range(k):
        a=secrets.randbelow(n - 3) + 2 # randomly chosen base from 2,n-2
        x=pow(a,d,n) # a^d mod n

        if x==1 or x==n-1:
            continue

        for j in range(s-1):
            x = pow(x,2,n)

            if x==n-1:
                break
        else: # if break executed, then false is skipped
            return False

    return True


# generate 512 bit prime
def generate_prime(bits=512):
    count=0 # count of candidates we have generated

    while True:
        count+=1

        n=secrets.randbits(bits) # generates a random number with atmost 512 bits
        n= n | (1 << (bits - 1)) # this line sets 511 bit to 1 so that the number is of 512 bits
        n = n | 1 # makes it odd

        if miller_rabin(n, 40):
            return n, count


# test using a particular base
def test_base(n, a):
    d=n-1
    s=0

    while d%2==0:
        d//=2
        s+=1

    x=pow(a,d,n)

    if x==1 or x==n-1:
        return True

    for i in range(s-1):
        x=pow(x,2,n)

        if x==n-1:
            return True

    return False


# generate prime
prime,count=generate_prime()

print("Generated prime:")
print(prime)

# verify bit length
print("\nBit length:", prime.bit_length())
assert prime.bit_length() == 512 # stop the code if wrong

# test using fixed bases
bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

print("\nMiller-Rabin test:")
for a in bases:
    if test_base(prime, a):
        print("Base", a, ": PASS")
    else:
        print("Base", a, ": FAIL")

# independent check using sympy
result = isprime(prime)
print("\nSymPy result:", result)

assert result

end = time.perf_counter()
elapsed = end - start

# display final report
print("\n" + "=" * 65)
print("{:<40} {}".format("Parameter", "Value"))
print("=" * 65)

print("{:<40} {}".format("Assigned bit length", 512))
print("{:<40} {}".format("Generated prime candidate", prime))
print("{:<40} {}".format("Actual bit length of the candidate",
                          prime.bit_length()))
print("{:<40} {}".format("Number of candidates tested", count))
print("{:<40} {}".format("Number of Miller-Rabin rounds", 40))
print("{:<40} {:.6f} seconds".format("Total execution time", elapsed))

print("=" * 65)
print("All verifications passed.")
