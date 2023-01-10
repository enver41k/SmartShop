from flask import Flask, render_template, session, request, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)

mysql = MySQL(app)
def orders():
    if session:
        cursor = mysql.connection.cursor()
        cursor.execute(f'''SELECT * FROM trash, phone where account_idaccount = {session.get('id')} 
        and phone_idphone = idphone''')
        phones = cursor.fetchall()
        print(phones)
        return render_template('orders.html', phones=phones)
    return render_template('orders.html')