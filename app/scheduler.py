import psutil
import time
import threading
import multiprocessing
import numpy as np
import requests
import os

class TaskScheduler:
    def __init__(self):
        self.cpu_count = psutil.cpu_count(logical=True)

    def classify_task(self, func, *args, **kwargs):
        """Classifies a task as CPU-bound or I/O-bound based on CPU usage over multiple runs"""
    
        # Run the function multiple times for better accuracy
        iterations = 5  # Adjust based on function execution time
        cpu_times_before = os.times()  # Get CPU usage before execution
    
        for _ in range(iterations):
            func(*args, **kwargs)  # Run the function multiple times

        cpu_times_after = os.times()  # Get CPU usage after execution

        # Compute the CPU usage difference
        cpu_utilization = (cpu_times_after.user + cpu_times_after.system) - \
                        (cpu_times_before.user + cpu_times_before.system)

        avg_cpu_util = cpu_utilization / iterations

        # Set threshold (adjust based on experiments)
        if avg_cpu_util > 0.1:  # If CPU time usage is high
            return "CPU-bound"
        else:
            return "I/O-bound"
    
    def run_normal_task(self, func, *args, **kwargs):
        """Run the task normally (Single-threaded)"""
        start= time.time()
        func(*args, **kwargs)   
        return time.time() - start
    
    def run_multi_threaded_task(self, func, *args, **kwargs):
        """Run the task using multiple threads"""
        start= time.time()
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        thread.join()
        return time.time() - start
    
    def run_multi_process_task(self, func, *args, **kwargs):
        """Run the task using multiple processes"""
        start= time.time()
        process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        process.start()
        process.join()
        return time.time() - start
    
    def execute(self, func, *args, **kwargs):
        """Execute the task based on its classification"""
        task_type = self.classify_task(func, *args, **kwargs)
        
        if task_type == "CPU-bound":    
            if self.cpu_count > 1:  # Use multiprocessing if enough cores
                print("Using Multiprocessing")
                return self.run_multi_process_task(func, *args, **kwargs)
            else:
                print("Using Normal Processing")
                return self.run_normal_task(func, *args, **kwargs)
        else:
            print("Using Multithreading")
            return self.run_multi_threaded_task(func, *args, **kwargs)
        
def cpu_bound_task():
    """Heavy computation task (e.g., Matrix Multiplication)"""
    x = np.random.rand(1000, 1000)
    np.dot(x, x)

def io_bound_task():
    """Simulated I/O-bound task (e.g., Network Request)"""
    requests.get("https://www.google.com")


# Test Execution
if __name__ == "__main__":
    scheduler = TaskScheduler()
    
    print("\nRunning CPU-bound Task:")
    cpu_time = scheduler.execute(cpu_bound_task)
    print(f"Execution Time: {cpu_time:.4f}s")

    print("\nRunning I/O-bound Task:")
    io_time = scheduler.execute(io_bound_task)
    print(f"Execution Time: {io_time:.4f}s")        

#     what and why is init and self mean
# what are are self, func, args, kwargs as function parameters
# what is this three commas """
# what is threading.Thread mean 