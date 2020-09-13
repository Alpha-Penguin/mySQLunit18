
#imports (standard flask and mysqlconnector)
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

#connecting to local database. This is obvs terrible security. ( discussed as part of lead in to U7)
#vetdb = mysql.connector.connect(user='vet', password='vet123',
                          #    host='127.0.0.1', database='vet',
                           #   auth_plugin='mysql_native_password')


#Code runs if index.html called (root)
@app.route('/', methods=['GET', 'POST'])
def index():
    if "owner" in request.form:
        return render_template('/owner.html')
    elif "changeme" in request.form:
        return render_template('/changeme.html')
    elif "changeme" in request.form:
        return render_template('/changeme.html') 
    elif "changeme" in request.form:
        return render_template('/changeme.html') 
    else:
        return render_template('/index.html')


#Code runs if adding a new owner (submit pressed on owner.html page)
@app.route('/owner', methods=['GET', 'POST'])
def owner():
  #Takes details from form and crafts a sql statement  
  if "submit" in request.form:
          details = request.form
          Surname = details['Surname']
          FirstName = details['FirstName']
          Address = details['Address']
          Address2 = details['Address2']
          Phone = details['Phone']
          cur = vet.cursor()
          cur.execute("INSERT INTO owner(Surname, FirstName, Address, Address2, Phone) VALUES (%s, %s,%s, %s,%s)", (Surname, FirstName, Address, Address2,Phone))
          vet.commit()
          cur.close()
          
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')



if __name__ == '__main__':
    app.run(debug=True)
    #app.run()
