import argparse
from math import gcd
from typing import Callable

POLLARD_F = lambda x: x**2 + 1


def parser() -> argparse.ArgumentParser:
    argp = argparse.ArgumentParser()
    argp.add_argument("-nf", type=int, required=False, help="The number to factorize for Fermat's method")
    argp.add_argument("-np", type=int, required=False, help="The number to factorize for Pollard's rho method")
    return argp


def fermat_factorize(n: int, max_iterations: int = 20) -> tuple[tuple[int, int], int]:
    """
    Fermat's method for factoring a number.

    :param int n: The number to factorize.
    :param int max_iterations: The maximum number of iterations to run.
    :return tuple[tuple[int, int], int]: The factors of the number and the number of iterations.
    """
    t0 = int(n**0.5)

    print(f"t0 = [sqrt({n})] = {t0}\n")

    counter = 1
    print("Iterations:\n")
    for _ in range(max_iterations):
        t = t0 + counter

        t2 = t * t - n
        s = int(t2**0.5)

        perfect_square = "yes" if s * s == t2 else "no"
        print(f"t = t0 + {counter}: t^2 - n = {t2} | s = [sqrt({t2})] = {s} | perfect square: {perfect_square}")

        if perfect_square == "yes":
            print(f"Values: s={s}, t={t}\n")
            print(f"Conclusion:\nThe obtained two factors of n are (in increasing order): {t-s} and {t+s}\n")
            return (t - s, t + s), counter

        counter += 1
        t += 1

    return None, counter


def pollar_rho_factorize(
    n: int, x0: int = 2, f: Callable[[int], int] = POLLARD_F, max_iterations: int = 20
) -> tuple[tuple[int, int], int]:
    """
    Pollard's rho method for factoring a number.

    :param int n: The number to factorize.
    :param int x0: The initial value for the sequence.
    :param Callable[[int], int] f: The function to use for the sequence.
    :param int max_iterations: The maximum number of iterations to run.
    :return tuple[tuple[int, int], int]: The factors of the number and the number of iterations.
    """
    x = x0
    y = x0
    factor = 1
    values = {1: x0}

    print("Iterations (results mod n):\n")
    counter = 1
    for _ in range(max_iterations):
        x = f(x) % n
        y = f(f(y)) % n
        values[counter] = x

        print(f"[Iteration {counter}] x{counter} = {x} (mod {n})")

        if counter % 2 == 0:
            factor = gcd(abs(x - values[counter // 2]), n)
            print(f"\n(|x{counter} - x{counter//2}|, {n}) = {factor}\n")

            if factor > 1 and factor < n:
                break
        
        counter += 1
    
    if counter >= max_iterations:
        return None, counter
    
    second_factor = n // factor
    print(
        f"Conclusion:\nThe obtained two factors of n are (in increasing order): {min(factor, second_factor)} and {max(factor, second_factor)}\n"
    )
    return (min(factor, second_factor), max(factor, second_factor)), counter


if __name__ == "__main__":
    p = parser()
    args = p.parse_args()

    nf, np = args.nf, args.np
    if nf is not None:
        factors, iterations = fermat_factorize(nf)
        print(f"The number {nf} is factored as {factors} in {iterations} iterations")
    if np is not None:
        factors, iterations = pollar_rho_factorize(np)
        print(f"The number {np} is factored as {factors} in {iterations} iterations")