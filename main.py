from datetime import timedelta

from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb

from form import about, home, auth, admin, orders

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

mysql = MySQL(app)


def create_connection(host, user, password, db):
    connection = False
    try:
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = password
        app.config['MYSQL_DB'] = db
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        print("Connection to MySQL DB successful")
        connection = True
        return connection

    except MySQLdb.OperationalError as e:
        print(f'MySQL server has gone away: {e}, trying to reconnect')
        raise e


connect_db = create_connection('localhost', 'root', 'admin', 'smartshop')
# connect_db = create_connection('enver41k.mysql.pythonanywhere-services.com', 'enver41k', 'server123', 'enver41k$smartshop')

app.add_url_rule('/', view_func=home.index)
app.add_url_rule('/static', view_func=home.index)

app.add_url_rule('/about', view_func=about.about)

# Auth forms
app.add_url_rule('/login', methods=['GET', 'POST'], view_func=auth.login)
app.add_url_rule('/logout', view_func=auth.logout)
app.add_url_rule('/register', methods=['GET', 'POST'], view_func=auth.register)


# Admin panel
app.add_url_rule('/admin', methods=['GET', 'POST'], view_func=admin.admin)

# ORDERS
app.add_url_rule('/orders', view_func=orders.orders)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select * from phonetype, phone where phone.phonetype_idphonetype = phonetype.idphonetype")
    phone = cursor.fetchall()
    return render_template("booking.html", phone=phone)


@app.route('/payment/<idphone>', methods=['GET', 'POST'])
def payment(idphone):
    if not session.get("username"):
        return redirect("/login")
    msg = ''
    cursor = mysql.connection.cursor()
    cursor.execute(f"select status from phone where idphone={idphone}")
    status = cursor.fetchone()
    cursor.execute(f"SELECT namephone FROM phone WHERE idphone={idphone}")
    namep = cursor.fetchone()

    if request.method == 'POST':
        f = request.form['name']
        l = request.form['lname']
        p = request.form['phone']
        e = request.form['email']
        a = request.form['address']
        try:
            cursor.execute(f''' INSERT INTO `trash` (`phone_idphone`, `account_idaccount`, `firstname`, `lastname`, `email`, `number`, `address`) 
            VALUES ('{idphone}','{session.get('id')}','{f}','{l}','{e}','{p}','{a}') ''')
            mysql.connection.commit()
            flash('Товар добавлен', category='success')
        except:
            flash('Товар не добавлен', category='danger')
        return redirect(url_for('.payment', idphone=idphone))
    cursor.close()

    return render_template('payment.html', msg=msg, namep=namep)


@app.route('/reviews')
def reviews():
    return render_template("reviews.html")


@app.route('/help')
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(debug=True)
