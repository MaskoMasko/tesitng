from mylib import *
from flask import *
from flask_socketio import *

import mysql.connector
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def dbGet(username):
  connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
  if connection.is_connected():
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT name,surname,picture,followers,following,bio,objave,id FROM userssss WHERE username='{username}'")
    myresult = mycursor.fetchall()
    print(myresult)
    myresult = myresult[0]
    return myresult

@app.route('/')
def home():
  logStatus = request.cookies.get('logStat')
  username = request.cookies.get('User')
  return render_template("main.html",logStatus=logStatus,username=username)



@app.route('/tis')
def tis():
  return render_template("tis.html")

@app.route('/tisTry', methods = ['POST'])
def tisTry():
  if request.method == 'POST':
    lista = []
    upisano=request.form['data']
    print(upisano)
    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      mycursor.execute(f"SELECT username FROM userssss WHERE username LIKE '{upisano}%'")
      myresult = mycursor.fetchall()
      for i in range(len(myresult)):
        whatINeed = myresult[i]
        whatINeedMore = whatINeed[0]
        lista.append(whatINeedMore)
      print(myresult)
    return jsonify(result=lista)

@app.route('/doIFollow')
def doIFollow():
  whoDoIFollow = "nofollow"
  kiFollowa = request.args.get('a')
  kegaFollowa = request.args.get('b')
  connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
  if connection.is_connected():
    print("PRVI STEP")
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT followers FROM userssss WHERE id='{kegaFollowa}'")
    myresult = mycursor.fetchall()
    if myresult:
      print("DRUGI STEP")
      myresult = myresult[0]
      whoDoIFollow = myresult[0]
      if whoDoIFollow:
        whoDoIFollow = whoDoIFollow.split(" , ")
        if 'None' in whoDoIFollow:
          whoDoIFollow.remove('None')
        if '' in whoDoIFollow:
          whoDoIFollow.remove('')
      else:
        whoDoIFollow = ['']
      mycursor.execute(f"SELECT id FROM userssss WHERE username='{kiFollowa}'")
      myresult = mycursor.fetchall()
      myresult = myresult[0]
      myid = myresult[0]
      myid = str(myid)
      if myid in whoDoIFollow:
        print("FUCKING PARTY BIURCH")
        whoDoIFollow = "yesfollow"
  return jsonify(result=whoDoIFollow)
@app.route('/testtt/<id>')
def testtt(id):
  listaKogaPratis = []
  connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
  if connection.is_connected():
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT name,surname,picture,followers,following,bio,objave,username FROM userssss WHERE id='{id}'")
    myresult = mycursor.fetchall()
    print(myresult)
    myresult = myresult[0]
    whoDoIFollow = myresult[4]
    if whoDoIFollow:
      whoDoIFollow = whoDoIFollow.split(" , ")
      if 'None' in whoDoIFollow:
        whoDoIFollow.remove('None')
      if '' in whoDoIFollow:
        whoDoIFollow.remove('')
    else:
      whoDoIFollow = None
    if whoDoIFollow == None:
      whoDoIFollow = 'null'
    duzina = len(whoDoIFollow)
    for i in range(duzina):
      yes = str(whoDoIFollow[i])
      print(whoDoIFollow)
      mycursor.execute(f"SELECT username FROM userssss WHERE id='{yes}'")
      myresult = mycursor.fetchall()
      try:
        imeKeMiRabi = myresult[0][0]
        listaKogaPratis.append(imeKeMiRabi)
      except:
        pass
    print(myresult)
  return render_template("following.html",following=listaKogaPratis)

@app.route('/te/<id>')
def te(id):
  listaKogaPratis = []
  connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
  if connection.is_connected():
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT name,surname,picture,followers,following,bio,objave,username FROM userssss WHERE id='{id}'")
    myresult = mycursor.fetchall()
    print(myresult)
    myresult = myresult[0]
    whoDoIFollow = myresult[3]
    if whoDoIFollow:
      whoDoIFollow = whoDoIFollow.split(" , ")
      if 'None' in whoDoIFollow:
        whoDoIFollow.remove('None')
      if '' in whoDoIFollow:
        whoDoIFollow.remove('')
    else:
      whoDoIFollow = None
    if whoDoIFollow == None:
      whoDoIFollow = 'null'
    duzina = len(whoDoIFollow)
    for i in range(duzina):
      yes = str(whoDoIFollow[i])
      print(whoDoIFollow)
      mycursor.execute(f"SELECT username FROM userssss WHERE id='{yes}'")
      myresult = mycursor.fetchall()
      try:
        imeKeMiRabi = myresult[0][0]
        listaKogaPratis.append(imeKeMiRabi)
      except:
        pass
    print(myresult)
  return render_template("following.html",following=listaKogaPratis)

@app.route('/testTry')
def add_numbers():
  por = procitaj("poruke.json")
  duzina = len(por)
  return jsonify(result=por,duzina=duzina)

@app.route('/followTry')
def followTry():
  kiFollowa = request.args.get('a')
  kegaFollowa = request.args.get('b')
  connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
  if connection.is_connected():
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT following FROM userssss WHERE username='{kiFollowa}'")
    bivseSveKegaPrati = str(mycursor.fetchall()[0][0])
    sviKojePrati = bivseSveKegaPrati + " , " + kegaFollowa
    mycursor.execute(f"UPDATE userssss SET following = ('{sviKojePrati}') WHERE username='{kiFollowa}';")
    connection.commit()
    # OVO GORE DODA COVIKU KOJ ZELI FOLLOWAT U FOLLOWANE
    mycursor.execute(f"SELECT followers FROM userssss WHERE id='{kegaFollowa}'")
    bivseSveKiGaPrate = str(mycursor.fetchall()[0][0])
    mycursor.execute(f"SELECT id FROM userssss WHERE username='{kiFollowa}'")
    idOnogaKiFollowa = str(mycursor.fetchall()[0][0])
    sviKiGaFollowaju = bivseSveKiGaPrate + " , " + idOnogaKiFollowa
    mycursor.execute(f"UPDATE userssss SET followers = ('{sviKiGaFollowaju}') WHERE id='{kegaFollowa}';")
    connection.commit()
  print(kiFollowa)
  print(kegaFollowa)
  return jsonify(result="following",b=kegaFollowa)

@app.route('/unFollowTry')
def unFollowTry():
  kiFollowa = request.args.get('a')
  kegaFollowa = request.args.get('b')
  connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
  if connection.is_connected():
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT following FROM userssss WHERE username='{kiFollowa}'")
    bivseSveKegaPrati = str(mycursor.fetchall()[0][0])
    nesDrugo = bivseSveKegaPrati.split(' , ')
    if 'None' in nesDrugo:
      nesDrugo.remove('None')
    nesDrugo.remove(kegaFollowa)
    nesDrugoDrugo = " , ".join(nesDrugo)
    print(nesDrugo)
    mycursor.execute(f"UPDATE userssss SET following = ('{nesDrugoDrugo}') WHERE username='{kiFollowa}';")
    connection.commit()
    # OVO GORE DODA COVIKU KOJ ZELI FOLLOWAT U FOLLOWANE
    mycursor.execute(f"SELECT followers FROM userssss WHERE id='{kegaFollowa}'")
    bivseSveKiGaPrate = str(mycursor.fetchall()[0][0])
    mycursor.execute(f"SELECT id FROM userssss WHERE username='{kiFollowa}'")
    idOnogaKiFollowa = str(mycursor.fetchall()[0][0])
    nesTrece = bivseSveKiGaPrate.split(' , ')
    if 'None' in nesTrece:
      nesTrece.remove('None')
    nesTrece.remove(idOnogaKiFollowa)
    nesTreceTrece = " , ".join(nesTrece)
    mycursor.execute(f"UPDATE userssss SET followers = ('{nesTreceTrece}') WHERE id='{kegaFollowa}';")
    connection.commit()
  print(kiFollowa)
  print(kegaFollowa)
  return jsonify(result="not following",b=kegaFollowa)


@app.route('/mainTu')
def mainTu():
  logStatus = request.cookies.get('logStat')
  objaveKeTrebasViditi = []
  if logStatus == "Logged In":
    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      kaLista = []

      mycursor.execute(f"SELECT `image`,`opis`,`komentari`,`lajkova`,`osoba`,`imeLika`,`id` FROM objavee")
      myresult = mycursor.fetchall()
      #print(myresult)
      duzina = len(myresult)
      for i in range(duzina):
        temp = myresult[i]
        #print(temp)
        image = temp[0]
        opis = temp[1]
        komentari = temp[2]
        lajkova = temp[3] 
        osoba = temp[4]
        imeLikaa = temp[5]
        idd = temp[6]
        if komentari == None:
          komentari = 'null'
        if lajkova == None:
          lajkova = 'null'
        if opis == None:
          opis = 'null'
        k = {'slika':image,'opis':opis,'komentari':komentari,'lajkova':lajkova,'osoba':osoba,'imeLika':imeLikaa,'id':idd}
        kaLista.append(k)

      usernameOfGuyLookinAtThePage = request.cookies.get('User')
      mycursor.execute(f"SELECT following,id FROM userssss WHERE username='{usernameOfGuyLookinAtThePage}'")
      myresult = mycursor.fetchall()
      myresult = myresult[0]
      whoDoIFollow = myresult[0]
      if whoDoIFollow == '':
        whoDoIFollow = []
      myID = myresult[1]
      myID = str(myID)
      if whoDoIFollow:
        whoDoIFollow = whoDoIFollow.split(" , ")
        if 'None' in whoDoIFollow:
          whoDoIFollow.remove('None')
        if '' in whoDoIFollow:
          whoDoIFollow.remove('')
      if whoDoIFollow == None:
        whoDoIFollow = [myID]
      else:
        whoDoIFollow.append(myID)
      # DO TU DELA
      for i in kaLista:
        testRun = str(i.get('osoba'))
        print(f"followam nekog  {testRun}")

        if testRun in whoDoIFollow:
          print(f"followam nekog  {whoDoIFollow}")
          objaveKeTrebasViditi.append(i)
      print(objaveKeTrebasViditi)

    return render_template("main2.html",username=usernameOfGuyLookinAtThePage,objave=objaveKeTrebasViditi,tvojID = myID)
  else:
    return render_template("login.html")

@app.route('/chat')
def chat():
  logStatus = request.cookies.get('logStat')
  username = request.cookies.get('User')
  print(username)
  if logStatus != "Logged In":
    return redirect("/login")
  else:
    return render_template("chat.html",logStatus=logStatus,username=username)

@app.route('/signup')
def signup():
  return render_template("signup.html")

@app.route('/novaObjava')
def novaObjava():
  return render_template("novaObjava.html")

@app.route('/novaObjavaTry', methods = ['POST'])
def novaObjavaTry():
  if request.method == 'POST':
    username = request.cookies.get('User')
    slika = request.files['slika']
    opis = str(request.form.get('opis')) #dela
    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      mycursor.execute(f"SELECT objave,id FROM userssss WHERE username='{username}'")
      tup = mycursor.fetchall()[0]
      bivseObjave = str(tup[0])
      id = str(tup[1])
      mycursor.execute(f"SELECT MAX(id) FROM objavee")
      newImage = mycursor.fetchall()[0][0]
      if newImage == None:
        newImage = 0
      newImage +=1
      mycursor.execute(f"INSERT INTO objavee (image,osoba,opis,imeLika) VALUES ('{newImage}',{id},'{opis}','{username}')")
      connection.commit()
      # mycursor.execute(f"INSERT INTO objave (opis) VALUES ('{opis}')")
      # connection.commit()
      # mycursor.execute(f"SELECT LAST_INSERT_ID();")
      # id = str(mycursor.fetchall()[0][0])
      # mycursor.execute(f"SELECT objave FROM userssss WHERE username='{username}'")
      # bivseObjave = str(mycursor.fetchall()[0][0])
      newImage = str(newImage)
      sveObjave = bivseObjave + " , " + newImage
      mycursor.execute(f"UPDATE userssss SET objave = ('{sveObjave}') WHERE username='{username}';")
      connection.commit()
      pat = os.path.join("static/objave",newImage+".jpg") # LOS SOLUTION ZA OVO
      slika.save(pat)

    return redirect("/mainTu")

@app.route('/ttestt')
def ttestt():
  return render_template("ttestt.html")  

@app.route('/signout')
def signout():
  resp = make_response(redirect('/login'))
  resp.set_cookie('logStat', 'Signed Out')
  resp.set_cookie('User', "None")
  return resp      

@app.route('/login')
def login():
  logStatus = request.cookies.get('logStat')
  if logStatus == "Logged In":
    return redirect("/chat")
  else:
    return render_template("login.html")

"""@app.route('/profile')
def profile():
  logStatus = request.cookies.get('logStat')
  if logStatus == "Logged In":
    username = request.cookies.get('User')
    myresult = dbGet(username)
    print(myresult)
    name = myresult[0]
    surname = myresult[1]
    picture = myresult[2]
    followers = myresult[3]
    following = myresult[4]
    bio = myresult[5]
    objave = myresult[6]
    # sljedece je: CUSTOMZIANJE TJ DA UPISES ONO CA FALI UDATABAZI,
    # DA DISPLAYA TO MALO LIPSE, FOLLOWERE FOLOWERSE I OBJACE TREA COUNTAT NE DISPLAYAT
    # YEAH NO BIGGIE
    print(objave)
    if objave == None:
      brojObjava = 0
    else:
      brojObjava = objave.split(" , ")
      brojObjava = len(brojObjava) - 1
    print(brojObjava)
    return render_template("profile.html",username=username,name = name,surname = surname, picture=picture,followers=followers,following=following,bio=bio,objave=brojObjava)
  else:
    return render_template("login.html")"""


@app.route('/user/<id>')
def show_user_profile(id):
  connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
  if connection.is_connected():
    cookieUsername = request.cookies.get('User')
    mycursor = connection.cursor()
    mycursor.execute(f"SELECT name,surname,picture,followers,following,bio,objave,username FROM userssss WHERE id='{id}'")
    myresult = mycursor.fetchall()
    myresult = myresult[0]
    name = myresult[0]
    surname = myresult[1]
    picture = myresult[2]
    followers = myresult[3]
    following = myresult[4]
    bio = myresult[5]
    objave = myresult[6]
    username = myresult[7]
    print(followers)
    if objave == None:
      brojObjava = 0
    else:
      brojObjava = objave.split(" , ")
      if 'None' in brojObjava:
        brojObjava.remove('None')
      brojObjava = len(brojObjava)


    if (followers == None) or (followers == ''):
      brojfollowera = 0
    else:
      brojfollowera = followers.split(" , ")
      if 'None' in brojfollowera:
        brojfollowera.remove('None')
      if '' in brojfollowera:
        brojfollowera.remove('')
      brojfollowera = len(brojfollowera)


    if (following == None) or (following == ''):
      brojFollowa = 0
      flw = brojFollowa
    else:
      brojFollowa = following.split(" , ")
      flw = brojFollowa
      if 'None' in flw:
        flw.remove('None')
      if '' in brojFollowa:
        brojFollowa.remove('')
      brojFollowa = len(flw)


    usernameOfGuyLookinAtThePage = request.cookies.get('User')
    mycursor.execute(f"SELECT name,surname,picture,followers,following,bio,objave,id FROM userssss WHERE username='{usernameOfGuyLookinAtThePage}'")
    myresult = mycursor.fetchall()
    myresult = myresult[0]
    whoDoIFollow = myresult[4]
    if whoDoIFollow:
      whoDoIFollow = whoDoIFollow.split(" , ")
      if 'None' in whoDoIFollow:
        whoDoIFollow.remove('None')
    else:
      whoDoIFollow = None
    if whoDoIFollow == None:
      whoDoIFollow = 'null'
    # 19.5 11:27 PM, NEZNAM STA RADIM NITI STO SAM NAPRAVIO ALI DELA
    # NEMOREN VISE GREN SPIT, ZA SUTRA AKO TI VBEC PRATIS TOG USERA NESMIJE
    # PISAT DA GA OPET ZAPRATIS JER MI SE NEDA TO HANDLEAT HVALA LIPA
    # AKO HOCES JOS HUSTLEA NAPRAVI DA AK GA PRATIS MOZES ODPRATIT
    # LKNC
    kaLista = []
    if objave:
      objave = objave.split(" , ")
      if 'None' in objave:
        objave.remove('None')
      for i in objave:
        mycursor.execute(f"SELECT `image`,`opis`,`komentari`,`lajkova`,id FROM objavee WHERE id='{i}'")
        myresult = mycursor.fetchall()
        myresult = myresult[0]
        image = myresult[0]
        opis = myresult[1]
        komentari = myresult[2]
        lajkova = myresult[3]
        if komentari == None:
          komentari = 'null'
        if lajkova == None:
          lajkova = 'null'
        if opis == None:
          opis = 'null'
        k = {'slika':image,'opis':opis,'komentari':komentari,'lajkova':lajkova}
        kaLista.append(k)
    if objave == None:
      objave = 'null'
    cookieUsername = cookieUsername.lower()
    username = username.lower()
    print(followers)
    if followers == '':
      print("waeeeooo")
    if picture == None:
      picture = 'cover3'
    if cookieUsername != username:
      return render_template("tudiProfile.html",username=username,name = name,surname = surname, picture=picture,followers=brojfollowera,following=brojFollowa,bio=bio,objave=brojObjava,id=id,doFollow=whoDoIFollow,objaveobjave=objave,posts=kaLista)
    else:
      return render_template("profile.html",username=username,name = name,surname = surname, picture=picture,followers=brojfollowera,following=brojFollowa,bio=bio,objave=brojObjava,id=id,doFollow=whoDoIFollow,objaveobjave=objave,posts=kaLista)



@app.route('/cust')
def cust():
  logStatus = request.cookies.get('logStat')
  if logStatus == "Logged In":
    username = request.cookies.get('User')
    myresult = dbGet(username)
    name = myresult[0]
    surname = myresult[1]
    picture = myresult[2]
    followers = myresult[3]
    following = myresult[4]
    bio = myresult[5]
    objave = myresult[6]
    # sljedece je: CUSTOMZIANJE TJ DA UPISES ONO CA FALI UDATABAZI,
    # DA DISPLAYA TO MALO LIPSE, FOLLOWERE FOLOWERSE I OBJACE TREA COUNTAT NE DISPLAYAT
    # YEAH NO BIGGIE
    return render_template("customize.html",username=username,name = name,surname = surname, picture=picture,followers=followers,following=following,bio=bio,objave=objave)
  else:
    return render_template("login.html")

@app.route('/custo', methods = ['POST'])  
def custo():
  if request.method == 'POST':
      slika = request.files['slika']
      name = request.form.get('name') #dela
      surname = request.form.get('surname') #dela
      username = request.form.get('username') #dela
      bio = request.form.get('bio') #dela
      usernam = request.cookies.get('User')
      myresult = dbGet(usernam)
      listaZaUpdateat = [{'picture':slika},{'name':name},{'surname':surname},{'username':username},{'bio':bio}]
      if slika == '':
        del listaZaUpdateat[0]
      if name == '':
        del listaZaUpdateat[-4]
      if surname == '':
        del listaZaUpdateat[-3]
      if username == '':
        del listaZaUpdateat[-2]
      if bio == '':
        del listaZaUpdateat[-1]

      id = str(myresult[7])
      pat = os.path.join("static/profilePics",id+".jpg") # LOS SOLUTION ZA OVO
      slika.save(pat)
      # STAO SAM OVDJE 16.5, ZNACI DOBIO SAM VALUE TREBAM IH SADA STAVI/UPDATEAT U DATABASSU GL SOLDIER
      connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
      if connection.is_connected():
        mycursor = connection.cursor()
        print("yeah yeah")
        print(id)
        #mycursor.execute(f"UPDATE userssss SET picture='{id}', name='{name}', surname='{surname}', bio='{bio}'  WHERE id='{id}';")
        # TREBA DODAT PROTEKCIJU PROTIV DUPOLIH USERNAMEOVA
        connection.commit()
        for i in listaZaUpdateat:
          temp = i.keys()
          temp = list(temp)
          temp = temp[0]
          if temp == 'picture':
            temp1 = id
          else:
            temp1 = i.get(temp)
          print(temp)
          print(temp1)
          mycursor.execute(f"UPDATE userssss SET {temp}='{temp1}'  WHERE id='{id}';")
      # OVAJ DIO GORE NE DELA, 16.5 GREN SPIT
      return redirect('/signout')

@app.route('/signupTry', methods = ['POST'])  
def signupTry():
  if request.method == 'POST':
    name = request.form.get('name') #dela
    username = request.form.get('username') #dela
    email = request.form.get('email') #dela
    password = request.form.get('password') #dela
    surname = request.form.get('surname') #dela

    val = (username,password,email,name,surname)
    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      sql = "INSERT INTO userssss (username,password,email,name,surname) VALUES (%s, %s,%s,%s,%s)"           
      mycursor.execute(f"SELECT email FROM userssss WHERE email='{email}'")
      myresult = mycursor.fetchall()
      duzina = len(myresult)
      mycursor.execute(f"SELECT username FROM userssss WHERE username='{username}'")
      myresult2 = mycursor.fetchall()
      duzina2 = len(myresult2)
      if duzina == 0:     # NEMA VEC U DATABAZI
        mycursor.execute(f"SELECT username FROM userssss WHERE username='{username}'")
        myresult2 = mycursor.fetchall()
        duzina2 = len(myresult2)
        if duzina2 == 0:
          print(myresult)
          mycursor.execute(sql, val)
          print("dodano u databasusu ")
          connection.commit()
          mycursor.close()
          connection.close()
          print("MySQL connection is closed")
          return redirect('/')
        elif duzina2 > 0:
          heresult = myresult2[0][0]
          print(heresult+" already exists")
          connection.commit()
          mycursor.close()
          connection.close()
          print("MySQL connection is closed")
          return render_template("login.html",error = "A user with this username already exists, would you like to log in")

      elif duzina > 0: # VEC IMA U DATABAZI
        myresult = myresult[0][0]
        print(myresult+" already exists")
        connection.commit()
        mycursor.close()
        connection.close()
        print("MySQL connection is closed")
        return render_template("login.html",error = "A user with this email already exists, would you like to log in")

@app.route('/loginTry', methods = ['POST'])  
def loginTry():
  if request.method == 'POST':
    username = request.form.get('name') #dela
    password = request.form.get('password') #dela

    connection = mysql.connector.connect(host='localhost',database='electronics',user='root',password='password')
    if connection.is_connected():
      mycursor = connection.cursor()
      mycursor.execute(f"SELECT password FROM userssss WHERE username='{username}'")
      myresult = mycursor.fetchall()
      duzina = len(myresult)
      if duzina == 0:
        print("That username does not exist")
        return render_template("signup.html",error = "A user with that name does not exist, would you like to sign up")
      elif duzina > 0:
        myresult = myresult[0][0]
        if password == myresult:
          resp = make_response(redirect('/'))
          resp.set_cookie('logStat', 'Logged In')
          print(username)
          resp.set_cookie('User', username)
          return resp      
        else:
          flash("Wrong password")
          return redirect('/login')
    print(username, password,myresult)
    return redirect('/')




@socketio.on('message')
def handle_message(data):
  logStatus = request.cookies.get('logStat')
  username = request.cookies.get('User')
  print('received message: ' + data)
  data = data +"///"+ str(username)
  emit('announcements', data,broadcast=True) # OVAKO SALJEMO I DI SALJEMO
  dodajNaKraj("poruke.json",data)




if __name__ == '__main__':
    
    socketio.run(app)