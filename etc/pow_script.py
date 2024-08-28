import hashlib
import string
import itertools

def solve_pow(prefix, target_hash, pow_strength):
    """
    Finds the correct suffix that, when combined with the given prefix, matches the target hash.
    """
    characters = string.ascii_lowercase + string.digits
    
    suffix_length = pow_strength
    
    for suffix in itertools.product(characters, repeat=suffix_length):
        candidate = prefix + ''.join(suffix)
        if hashlib.md5(candidate.encode()).hexdigest() == target_hash:
            return candidate
    
    return None

if __name__ == "__main__":
    prefix = input("Enter the prefix: ")
    target_hash = input("Enter the target hash: ")
    pow_strength = int(input("Enter the number of chars to bruteforce: "))
    
    solution = solve_pow(prefix, target_hash, pow_strength)

    if solution:
        print(f"Solution found: {solution}")
    else:
        print("No solution found.")
