from numpy import average
from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS
import time
bc = Blockchain()

times = []

for i in range(1000):
    start_time = time.time_ns()

    bc.add_block(i)
    end_time = time.time_ns()

    time_took_to_mine = (end_time - start_time) / SECONDS
    times.append(time_took_to_mine)

    average_time = sum(times) / len(times)

    print(f'New block difficulty: {bc.chain[-1].difficulty}\n')
    print(f'Time took to mine new block: {time_took_to_mine}\n')
    print(f'Average time to add blocks: {average_time}\n')