import math
from collections import defaultdict
import time

def calculate_shannon_entropy(data_str: str) -> float:
    """
    Calculates Shannon Entropy (H) = - sum(p(x) * log2(p(x)))
    Structured JSON/plain text typically scores between 2.0 and 4.5.
    Encrypted payloads/ransomware blobs typically score > 5.2.
    """
    if not data_str:
        return 0.0
    entropy = 0.0
    length = len(data_str)
    for char in set(data_str):
        p_x = float(data_str.count(char)) / length
        entropy -= p_x * math.log2(p_x)
    return entropy

class TrafficRateAnalyzer:
    def __init__(self, window_seconds: float = 5.0, max_requests: int = 10):
        self.window_seconds = window_seconds
        self.max_requests = max_requests
        self.history = defaultdict(list)

    def is_rate_exceeded(self, device_id: str) -> bool:
        now = time.time()
        # Clean older requests outside the sliding window
        self.history[device_id] = [t for t in self.history[device_id] if now - t < self.window_seconds]
        self.history[device_id].append(now)
        return len(self.history[device_id]) > self.max_requests