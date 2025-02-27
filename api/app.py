from flask import Flask, request, jsonify
from app.scheduler import TaskScheduler, cpu_bound_task, io_bound_task


app = Flask(__name__)
scheduler = TaskScheduler()

@app.route("/")
def home():
    return jsonify({"message": "Task Scheduler API is running!"})


@app.route("/execute", methods=["POST"])
def execute_task():
    """Endpoint to execute a task dynamically"""
    data = request.json
    task_type = data.get("task_type", "").lower()

    if task_type == "cpu":
        exec_time = scheduler.execute(cpu_bound_task)
        return jsonify({"task_type": "CPU-bound", "execution_time": exec_time})
    
    elif task_type == "io":
        exec_time = scheduler.execute(io_bound_task)
        return jsonify({"task_type": "I/O-bound", "execution_time": exec_time})

    return jsonify({"error": "Invalid task type. Use 'cpu' or 'io'."}), 400


if __name__ == "__main__":
    app.run(debug=True)
