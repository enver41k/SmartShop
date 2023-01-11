from flask import Flask, render_template, session, redirect, request

from flask_mysqldb import MySQL

app = Flask(__name__)

mysql = MySQL(app)


def admin():
    if session['username'] != 'admin':
        return redirect('/')
    cursor = mysql.connection.cursor()
    msg = ''
    msgr = ''
    if request.method == 'POST':
        num = request.form['number']
        status = request.form['status']
        price = request.form['price']
        img = request.form['img']
        desc = request.form['desc']
        print(num, status, price, img, desc)
        # try:
        cursor.execute(f"SELECT * FROM phone WHERE namephone={num}")
        x = cursor.fetchone()
            # if x is None:
        cursor.execute(f'''INSERT INTO `phonetype` (`img`, `price`, `disctiption`)
                        VALUES ('{img}', '{price}', '{desc}')''')
        cursor.execute(f'''SELECT idphonetype from phonetype where disctiption='{desc}' ''')
        s = cursor.fetchone()
        cursor.execute(f'''INSERT INTO `phone` (`namephone`, `status`, `phonetype_idphonetype`) 
                        VALUES ('{num}', '{status}', '{s["idphonetype"]}')''')
        mysql.connection.commit()
        msgr = 'Товар успешно создан'
            # elif x['namephone'] == int(num):
            #     msg = 'Такой  уже существует'
        # except(Exception,):
        #     msg = 'Данные неверны'

    cursor.execute(f"SELECT * FROM guest")
    guest = cursor.fetchall()
    return render_template('admin.html', msg=msg, msgr=msgr, guest=guest)
