from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Add enumerate to the Jinja2 globals
app.jinja_env.globals.update(enumerate=enumerate)

FILE_NAME = "expenses.json"

def load_expenses():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file)

@app.route('/')
def index():
    expenses = load_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    expenses = load_expenses()
    expense = {
        "date": request.form['date'],
        "category": request.form['category'],
        "amount": float(request.form['amount']),
        "description": request.form['description']
    }
    expenses.append(expense)
    save_expenses(expenses)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_expense(index):
    expenses = load_expenses()
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(expenses)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
