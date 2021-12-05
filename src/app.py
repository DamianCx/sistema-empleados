from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empleados'

UPLOADS = os.path.join('uploads')
app.config['UPLOADS'] = UPLOADS

mysql.init_app(app)
@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM empleados;"
   
    cursor.execute(sql)
    empleados = cursor.fetchall()
    

    conn.commit()

    return render_template('empleados/index.html',empleados=empleados)

@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store',methods=["POST"])
def store():
  
 nombre = request.form['txtNombre']
 correo = request.form['txtCorreo'] 
 foto = request.files['txtFoto'] 
 
 
 now = datetime.now()
 print(now)
 tiempo = now.strftime("%Y%H%M%S")
 print(tiempo)
 if foto.filename != '':
     nuevoNombreFoto = tiempo + '_'+ foto.filename
     foto.save("uploads/" + nuevoNombreFoto)

 sql = "INSERT INTO EMPLEADOS (nombre, correo, foto) values (%s,%s,%s);"
 datos = (nombre, correo, nuevoNombreFoto)

 conn = mysql.connect()
 
 cursor = conn.cursor()
 cursor.execute(sql, datos)
 conn.commit()

 return redirect('/')



@app.route('/delete/<int:id>')
def delete(id):
 sql= "DELETE FROM empleados WHERE id=%s"

 conn = mysql.connect()
 cursor = conn.cursor()
 cursor.execute(sql, id)
 conn.commit() 

 return redirect('/')

@app.route('/modify/<int:id>')
def modify(id):
 sql= "SELECT * FROM empleados WHERE id=%s"

 conn = mysql.connect()
 cursor = conn.cursor()
 cursor.execute(sql, id)
 empleado = cursor.fetchone()
 conn.commit() 

 return render_template('empleados/edit.html', empleado=empleado)


@app.route('/update', methods=['post'])
def update():
  nombre = request.form['txtNombre']
  correo = request.form['txtCorreo']
  foto = request.form['txtFoto']
  id = request.form['txtId']
  
  datos = (nombre, correo, id)

  conn =mysql.connect()
  cursor = conn.cursor()

  if foto.filename != '':
       now= datetime.now()
       tiempo = now.strftime("%Y%H%M%S")
       nuevoNombreFoto = tiempo + '_'+ foto.filename
       foto.save("uploads/" + nuevoNombreFoto)

  sql = f'SELECT foto FROM empleados WHERE id=(id)'
  cursor.execute(sql)

  nombreFoto = cursor.fetchome()[0] 

  os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))

  conn = mysql.connect()
  cursor = conn.cursor()
  sql =f'UPDATE empleados SET nombre=(nombre), correo=(correo) WHERE id=(id)'
  cursor.execute(sql)
  conn.commit()  


if __name__ == '__main__':
    app.run(debug=True)