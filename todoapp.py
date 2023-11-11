from flask import Flask, render_template, request, redirect, url_for
import pickle

app = Flask(__name__)

# Load the To Do List from a file if it exists
try:
    with open('todo_list.pkl', 'rb') as f:
        to_do_items = pickle.load(f)
except FileNotFoundError:
    to_do_items = []

@app.route('/', methods=['GET', 'POST'])
def view_todo_items():
    for i, item in enumerate(to_do_items):
        item['id'] = i
    return render_template('todo.html', items=to_do_items)

@app.route('/submit', methods=['POST'])
def submit_todo_item():
    # Receive form data
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    # Validate data
    if not "@" in email or priority not in ['Low', 'Medium', 'High']:
        # Redirect to home page if validation fails
        return redirect(url_for('view_todo_items'))

    # Add new item to the list if validation passes
    to_do_items.append({'task': task, 'email': email, 'priority': priority})
    
    # Redirect back to the main controller
    return redirect(url_for('view_todo_items'))

@app.route('/clear', methods=['POST'])
def clear_todo_list():
    # Clear the list of To Do items
    to_do_items.clear()

    # Redirect back to the main controller
    return redirect(url_for('view_todo_items'))

@app.route('/save', methods=['POST'])
def save_todo_list():
    with open('todo_list.pkl', 'wb') as f:
        pickle.dump(to_do_items, f)
    return redirect(url_for('view_todo_items'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_todo_item(item_id):
    to_do_items.pop(item_id)
    return redirect(url_for('view_todo_items'))

if __name__ == '__main__':
    app.run()
