import random
import time

# Generate a 16-byte token using MT19937
def generate_token(seed):
    rng = random.Random(seed)

    token = bytearray()

    for i in range(16):
        value = rng.getrandbits(8)
        token.append(value)

    return bytes(token)


# Generate password reset token
T = int(time.time())
# Unix timestamps represent the number of seconds elapsed since January 1, 1970

token = generate_token(T)

print("Original timestamp:", T)
print("Timestamp in hex:", hex(T))
print("Generated token:", token.hex())


# Save timestamp and token
with open("token.txt", "w") as file:
    file.write("Timestamp: " + hex(T) + "\n")
    file.write("Token: " + token.hex() + "\n")


# Attacker observes the token
observed_token = token

# Estimated timestamp (in a real attack, this is approximate)
estimated_time = T

start_time = estimated_time - 300
end_time = estimated_time + 300

print("\nStarting timestamp search...")
print("Search range:", start_time, "to", end_time)


# Brute-force timestamp seeds
count = 0
recovered_timestamp = None

for candidate in range(start_time, end_time + 1):

    count += 1

    candidate_token = generate_token(candidate)

    if candidate_token == observed_token:
        recovered_timestamp = candidate
        break


# 4. Display results
print("\nTotal timestamps tested:", count)

if recovered_timestamp is not None:

    print("Matching timestamp:", recovered_timestamp)
    print("Recovered timestamp in hex:", hex(recovered_timestamp))

    # 5. Verify recovered timestamp
    recovered_token = generate_token(recovered_timestamp)

    print("\nRecovered token:", recovered_token.hex())

    if recovered_token == observed_token:
        print("Verification successful!")
        print("Token matches the original token.")

else:
    print("No matching timestamp found.")

