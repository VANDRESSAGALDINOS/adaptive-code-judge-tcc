import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    
    n = int(next(it))
    q = int(next(it))
    
    next_planet = [0] * (n + 1)
    for i in range(1, n + 1):
        next_planet[i] = int(next(it))
    
    # SLOW VERSION: Naive simulation instead of binary lifting
    # This will be O(q * k) instead of O(q * log k)
    # For large k (up to 10^9), this becomes extremely slow
    
    EXTRA_WORK = 50  # Additional wasteful computation
    waste = 0
    
    results = []
    for _ in range(q):
        x = int(next(it))
        k = int(next(it))
        
        # Naive approach: simulate k steps one by one
        for step in range(k):
            x = next_planet[x]
            
            # Add extra wasteful work to ensure TLE
            for extra in range(EXTRA_WORK):
                waste += x * 1315423911 ^ step * 2654435761
                waste ^= (waste >> 16) + (waste << 8)
                waste &= 0xFFFFFFFFFFFFFFFF  # Keep as 64-bit
        
        results.append(str(x))
    
    print('\n'.join(results))

if __name__ == "__main__":
    main()
