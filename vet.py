
#imports (standard flask and mysqlconnector)
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

#connecting to local database. This is obvs terrible security. ( discussed as part of lead in to U7)
vetdb = mysql.connector.connect(user='vet', password='vet123',
                            host='127.0.0.1', database='vets',
                            auth_plugin='mysql_native_password')


#Code runs if index.html called (root)
@app.route('/', methods=['GET', 'POST'])
def index():

    if "owner" in request.form:
        return render_template('/owner.html')
    elif "viewpets" in request.form:
        return render_template('/viewpets.html', data=viewpets())
    elif "viewowner" in request.form:
        return render_template('/viewowner.html', data=viewowner()) 
    elif "viewvisit" in request.form:
        return render_template('/viewvisit.html', data=viewvisit()) 
    elif "addvisit" in request.form:
        return render_template('/addvisit.html', data1=getowner(), data2=getpet()) 
    elif "addpet" in request.form:
        return render_template('/addpet.html')       
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
          cur = vetdb.cursor()
          cur.execute("INSERT INTO owner(Surname, FirstName, Address, Address2, Phone) VALUES (%s, %s,%s, %s,%s)", (Surname, FirstName, Address, Address2,Phone))
          vetdb.commit()
          cur.close()
          
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')


#Code runs if adding a new visit
@app.route('/addvisit', methods=['GET', 'POST'])
def addchar():
  #Takes details from form and crafts a sql statement  
  if "submit" in request.form:
          details = request.form
          personID = getpersonID(details['owner'])
          petID = getpetID(details['pet'])
          int_personID = personID[0]
          int_personID = int(int_personID[0])
          int_petID = petID[0]
          int_petID = int(int_petID[0])
          owing = details['owing']
          date = details['date']
          cur = vetdb.cursor()
          cur.execute("INSERT INTO visit(OwnerID, PetID, Date, Owing) VALUES (%s, %s,%s, %s)", (int_personID, int_petID, date, owing))
          vetdb.commit()
          cur.close()
          
  elif "cancel" in request.form:
        pass
  return render_template('/index.html')




def viewpets():
    cur = vetdb.cursor()
    cur.execute("SELECT owner.FirstName, owner.Surname, PetName, PetType, PetAge FROM owner, pet where pet.OwnerID=owner.OwnerID;")
    data = cur.fetchall()
    return data


def viewowner():
    cur = vetdb.cursor()
    cur.execute("SELECT * FROM owner;")
    data = cur.fetchall()
    return data


def viewvisit():
    cur = vetdb.cursor()
    cur.execute("SELECT * FROM visit;")
    data = cur.fetchall()
    return data


def getowner():
    cur = vetdb.cursor()
    cur.execute("SELECT FirstName FROM owner")
    data = cur.fetchall()
    return data   


def getpet():
    cur = vetdb.cursor()
    cur.execute("SELECT PetName FROM pet")
    data = cur.fetchall()
    return data     



#Gets Primary key # of persons name selected from drop down so it can be inserted into table
def getpersonID(name):
    cur = vetdb.cursor()
    query = ("SELECT OwnerID FROM owner WHERE FirstName='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data

#Gets Primary key # of pet name selected from drop down so it can be inserted into table
def getpetID(name):
    cur = vetdb.cursor()
    query = ("SELECT PetID FROM pet WHERE PetName='"+name+"'")
    cur.execute(query)
    data = cur.fetchall()
    return data    



if __name__ == '__main__':
    app.run(debug=True)
    #app.run()
