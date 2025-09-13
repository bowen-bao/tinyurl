# Mathmatical encoding algorithm

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def encode(n: int) -> str:
    if n == 0: return ALPHABET[0]
    s = []
    base = len(ALPHABET)
    while n:
        n, r = divmod(n, base)
        s.append(ALPHABET[r])
    return "".join(reversed(s))
