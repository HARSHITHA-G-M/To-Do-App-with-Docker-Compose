from flask import Flask, request, redirect, render_template
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        if task:
            r.rpush('tasks', task)
        return redirect('/')

    tasks = r.lrange('tasks', 0, -1)
    return render_template('index.html', tasks=list(enumerate(tasks)))

@app.route('/delete/<int:index>')
def delete(index):
    tasks = r.lrange('tasks', 0, -1)
    if 0 <= index < len(tasks):
        r.lrem('tasks', 1, tasks[index])
    return redirect('/')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    tasks = r.lrange('tasks', 0, -1)
    if request.method == 'POST':
        new_task = request.form['task']
        if new_task and 0 <= index < len(tasks):
            r.lset('tasks', index, new_task)
        return redirect('/')
    return render_template('edit.html', index=index, task=tasks[index])

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)

