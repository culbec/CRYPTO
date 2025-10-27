import argparse

def decompose(n: int) -> tuple[int, int]:
    """
    Decomposes the number n - 1 = 2^s * t, where t is odd.

    :param int n: The number to decompose.
    :return tuple[int, int]: the exponent s and the odd number t.
    """
    s, t = 0, n - 1
    
    while t % 2 == 0:
        s += 1
        t //= 2
    
    return s, t

def miller_rabin(n: int, a: int, s: int, t: int) -> bool:
    """
    Performs the Miller-Rabin primality test for the number n with the base a.

    :param int n: The number to test.
    :param int a: The base of the test.
    :param int s: The exponent of 2 in the decomposition of n - 1.
    :param int t: The odd number in the decomposition of n - 1.
    :return bool: True if n is prime, False otherwise.
    """    
    results = []

    for i in range(s + 1):
        result = pow(a, 2**i * t, n)
        
        if i == 0 and result == 1:
            return True
        
        if i > 0 and result == 1 and results[-1] == n - 1:
            return True
        
        results.append(result)
        
    return False

def is_prime(n: int, bases: list[int]) -> bool:
    """
    Performs the Miller-Rabin primality test for the number n with bases.

    :param int n: The number to test.
    :param list[int] bases: The bases to test.
    :param int pow_iters: The number of times to run the power operation.
    :return bool: True if n is prime, False otherwise.
    """
    if n < 2:
        return False
    
    if n % 2 == 0:
        return False
    
    s, t = decompose(n)
    print(f"n - 1 = 2^{s} * {t} | {t} in binary: {bin(t)}")
    
    for k, a in enumerate(bases):
        print(f"[Iteration {k + 1}] Base a = {a} (results mod {n}):\n")
        t_copy, i , results = t, 0, []
        while t_copy > 0:
            results.append(f"{a}^(2^{i}) mod {n} = {pow(a, 2**i, n)}")
            t_copy >>= 1
            i += 1
        print("\n".join(results))
        print("\n--------------------------------\n")
    
    print(f"\nTesting with bases: {bases}\n")
    
    for k, a in enumerate(bases):
        print(f"[Iteration {k + 1}] Base a = {a} (results mod {n}):\n")
        results = [f"{a}^(2^{i}*{t}) mod {n} = {pow(a, 2**i * t, n)}" for i in range(s+1)]
        print("\n".join(results))
        if not miller_rabin(n, a, s, t):
            return False
        print("\n--------------------------------\n")
        
    return True

def parser() -> argparse.ArgumentParser:
    argp = argparse.ArgumentParser()
    argp.add_argument("-n", type=int, required=True, help="The number to test")
    argp.add_argument("-b", type=int, nargs="+", required=True, help="The bases to test")
    return argp

if __name__ == "__main__":
    p = parser()
    args = p.parse_args()
    
    n, bases = args.n, args.b
    result = is_prime(n, bases)
    print(f"The number {n} is {'likely to be prime' if result else 'composite'}")
    
    
