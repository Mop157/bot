import random

lol = {}

lol[123456789] = {'play': {"hello": 1, "kok": 4, "ji": 2}}

# keys = list(lol[123456789]['play'].keys())

# q = keys[0] if len(keys) > 0 else None
# q1 = keys[1] if len(keys) > 1 else None
# q2 = keys[2] if len(keys) > 2 else None
# q3 = keys[3] if len(keys) > 3 else None
# q4 = None
# q5 = None

# lol[123456789]["play"]["hello"]

# print(f"q = {q}")
# print(f"q1 = {q1}")
# print(f"q2 = {q2}")
# print(f"q3 = {q3}")
# print(f"q4 = {q4}")
# print(f"q5 = {q5}")
# lol[123456789]["play"]["hello"] += 1
# k = random.choice(keys)

del lol[123456789]["play"]['hello']

print(lol[123456789]["play"])

# n = 7

# if n > 4 and n < 7:
#     print(1)

