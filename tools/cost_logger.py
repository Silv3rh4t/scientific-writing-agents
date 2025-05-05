
import time

def track_cost(func, price_per_1k=0.20):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        tokens_used = kwargs.get("token_estimate", 1000)  # crude estimate
        cost = (tokens_used / 1000) * price_per_1k
        print(f"Used {tokens_used} tokens | Approx cost: ${cost:.4f} | Time: {time.time() - start:.2f}s")
        return result
    return wrapper
