from fileinput import filename
import mimetypes
from operator import index, itemgetter
from tracemalloc import Snapshot
from colorama import Cursor
from werkzeug.utils import secure_filename
from flask import Flask, redirect,render_template, request
from flask_mysqldb import MySQL
from io import BytesIO
import base64
from base64 import b64encode
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import io 
import os
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'snaptalk'
mysql = MySQL(app)

# def write_file(data, filename):
#     # Convert binary data to proper format and write it on Hard Disk
#     with open(filename, 'wb') as file:
#         file.write(data)
global usernamel
class Snaptalk():
    def Getwall():
        cursor = mysql.connection.cursor()
        resultt = cursor.execute(f"SELECT * FROM `walldata`")
        data=cursor.fetchall()
        index=0
        newdata=[]
        for row in data:
            row=list(row)
            image = row[4]
            image=b64encode(image).decode("utf-8")
            im = Image.open(BytesIO(row[4]))
            index += 1
            im.save(f'static/imgw/result{index}.png')
            row[4]=f'/imgw/result{index}.png'
            newdata.append(row)
     
        newdata=sorted(newdata, key=itemgetter(0), reverse=True)
        cursor.close()
        return newdata
    def dlike(index):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `walldata` WHERE `indexu`= '{index}'")
        datai=cursor.fetchone()
        likec=datai[1]
        username=datai[2]
        likec=int(likec)
        likec=likec+1
        cursor.execute(f"UPDATE walldata set `Likec`={likec} WHERE `indexu`='{index}'")
        mysql.connection.commit()
        return username
    def deletep(index):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `walldata` WHERE `indexu`= '{index}'")
        datai=cursor.fetchone()
        username=datai[2]
        cursor.execute(f"DELETE FROM `walldata` WHERE `indexu`='{index}'")
        mysql.connection.commit()
        return username
    def userlist():
        newuser=[]
        cursor = mysql.connection.cursor()
        nresultt = cursor.execute(f"SELECT uname FROM `nsnaptalk`")
        datai=cursor.fetchall()
        for lis in datai:
            lis=list(lis)
            nlis=lis[0].split('@')
            nlis[0]=nlis[0].title()
            newuser.append(nlis[0])
        cursor.close()
        return newuser
    def getmsg(cusernamel):
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `privatemess` where `senuser` = '{cusernamel}' or recuser='{cusernamel}' ")
        pmessd=cursor.fetchall()
        reciveu=[]
        dict={}
        for uname in pmessd:
            if uname[1] !=f"{cusernamel}":
                if uname[1] not in reciveu:
                    reciveu.append(uname[1])
            elif uname[2] !=f"{cusernamel}":
                if uname[2] not in reciveu:
                    reciveu.append(uname[2])
        index=0
        for i in range(len(reciveu)):
            fchat=[]
            for uname in pmessd:
                if uname[1]==reciveu[index] and  uname[2]==f"{cusernamel}" :
                    fchat.append(f"{uname[1]}: {uname[3]}")
                elif uname[1]==f"{cusernamel}"and  uname[2]==reciveu[index]:
                    fchat.append(f"{uname[1]}: {uname[3]}")
            dict[reciveu[index]]=fchat
            index +=1
        return dict



@app.route('/', methods = ['POST', 'GET'])
def page():
    return render_template("login.html")

@app.route('/createuser', methods = ['POST', 'GET'])
def createuser():
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        emaill = request.form['emaill']
        passs = request.form['passs']
        uage = request.form['uage']
        ucity = request.form['ucity']
        ugen = request.form['ugen']
        ugen=ugen.title()
        if ugen=="Male" or ugen=="Female" or ugen=="Other":
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO nsnaptalk(uname, upass, uage,ucity,ugender) VALUES (%s, %s,%s,%s,%s)", (emaill, passs,uage,ucity,ugen))
            mysql.connection.commit()
            cursor.close()
            message="Your Account Has Been Created Login To Continue"
            return render_template("login.html",message=message)
        else:
            message="Input a legit gender"
            return render_template("signup.html",message=message)

# ############################# Login #########################

@app.route('/Login', methods = ['POST', 'GET'])
def Login():
    emp=os.listdir('static/imgw')
    for file in emp:
        os.remove(f'static/imgw/{file}')
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        emaill = request.form['emaill']
        passs = request.form['passs']
        cursor = mysql.connection.cursor()
        result = cursor.execute(f"SELECT * FROM `nsnaptalk` WHERE `uname`= '{emaill}'")
        if result == 1:
            resultt = cursor.execute(f"SELECT * FROM `nsnaptalk` WHERE `uname`= '{emaill}' and `upass`='{passs}'")
            if resultt != 0:
                emaill=emaill.title()
                global usernamel
                username=emaill.split('@')
                usernamel=username[0]
                print(usernamel)
                newdata=Snaptalk.Getwall()
                userl=Snaptalk.userlist()
                cursor.execute(f"SELECT * FROM `snapmess`" )
                messd=cursor.fetchall()
                return render_template("wall.html",dataa=newdata,usernamem=usernamel,users=userl,messd=messd)
            else:
                cursor.close()
                messagep="Your password is incorrect"
                return render_template("login.html",messagep=messagep)
        else:
            cursor.close()
            message="There is no account with this username"
            return render_template("login.html",message=message)


@app.route('/ChatRoom', methods = ['POST', 'GET'])
def ChatRoom():
    if request.method == 'POST':
        cuser = request.form['cuser']
        dict=Snaptalk.getmsg(usernamel)       
        return render_template("chat.html",usernamem=usernamel,mydict=dict,chatuser=cuser)
    if request.method == 'GET':
        dict=Snaptalk.getmsg(usernamel)       
        return render_template("chat.html",usernamem=usernamel,mydict=dict)

@app.route('/PersonalChats', methods = ['POST', 'GET'])
def PersonalChats():
    if request.method == 'POST':
        recuser = request.form['recuser']
        recuser=recuser.title()
        mess = request.form['mess']
        username = request.form['username']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO privatemess(senuser, recuser, messagec) VALUES (%s, %s,%s)", (username,recuser,mess))
        mysql.connection.commit()
        cursor.close()
        dict=Snaptalk.getmsg(username)
        return render_template("chat.html",usernamem=username,mydict=dict)
@app.route('/DeleteChat', methods = ['POST', 'GET'])
def DeleteChat():
    if request.method == 'POST':
        recuser = request.form['recuser']
        recuser=recuser.title()
        username = request.form['username']
        print(username)
        cursor = mysql.connection.cursor()
        cursor.execute(f"DELETE FROM `privatemess` WHERE `senuser`='{username}' and `recuser`='{recuser}'")
        mysql.connection.commit()
        cursor.execute(f"DELETE FROM `privatemess` WHERE `senuser`='{recuser}' and `recuser`='{username}'")
        mysql.connection.commit()
        dict=Snaptalk.getmsg(username)
        return render_template("chat.html",usernamem=username,mydict=dict)



@app.route('/postmsg', methods = ['POST', 'GET'])
def postmsg():
    message = request.form['message']
    username = request.form['username']
    print(username)
    cursor = mysql.connection.cursor()
    cursor.execute(f"INSERT INTO snapmess(cuser, cmess) VALUES ('{username}', '{message}')")
    mysql.connection.commit()
    cursor.execute(f"SELECT * FROM `snapmess`" )
    messd=cursor.fetchall()
    cursor.close()
    data=Snaptalk.Getwall()
    ifiles = os.listdir('static/imgw')
    ifiles = ['imgw/' + file for file in ifiles]
    userl=Snaptalk.userlist()
    # print(usernamel)
    return render_template("wall.html",dataa=data,usernamem=username,ifiles=ifiles,users=userl,messd=messd)

@app.route('/Refreshlogin', methods = ['POST', 'GET'])
def Refreshlogin():
    if request.method == 'POST':
        username = request.form['username']
        print(username)
        newdata=Snaptalk.Getwall()
        userl=Snaptalk.userlist()
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `snapmess`" )
        messd=cursor.fetchall()
        cursor.close()
        # print(usernamel)
        return render_template("wall.html",dataa=newdata,usernamem=username,users=userl,messd=messd)

# ############################# Create Post #########################

@app.route('/createpost', methods = ['POST', 'GET'])
def createpost():
    if request.method == 'POST':
        udesc = request.form['udesc']
        uimage = request.files['uimage']
        username = request.form['username']
        print(uimage)
        print(uimage.filename)
        if str(uimage) == "<FileStorage: '' ('application/octet-stream')>":
            # print(uimage.filename)
            print("hey")
            # uimage="<FileStorage: '/static/def/Snaptalk.png' ('image/png')>"
            # filename="Snaptalk.png"
        filename=secure_filename(uimage.filename)
        mimetype= uimage.mimetype
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO walldata (username, udesc, uimage,mimetype) VALUES (%s, %s, %s,%s)", (username,udesc, uimage.read(),mimetype))
        mysql.connection.commit()
        data=Snaptalk.Getwall()
        message="Your Post has been successfully posted"
        ifiles = os.listdir('static/imgw')
        ifiles = ['imgw/' + file for file in ifiles]
        print(usernamel)
        userl=Snaptalk.userlist()
        cursor.execute(f"SELECT * FROM `snapmess`" )
        messd=cursor.fetchall()
        cursor.close()
        return render_template("wall.html",message=message,dataa=data,usernamem=usernamel,ifiles=ifiles,users=userl,messd=messd)
        
@app.route('/like', methods = ['POST', 'GET'])
def like():
    if request.method == 'POST':
        index = request.form['index']
        username=Snaptalk.dlike(index)
        data=Snaptalk.Getwall()
        ifiles = os.listdir('static/imgw')
        ifiles = ['imgw/' + file for file in ifiles]
        print(usernamel)
        userl=Snaptalk.userlist()
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM `snapmess`" )
        messd=cursor.fetchall()
        cursor.close()
        return render_template("wall.html",dataa=data,usernamem=usernamel,ifiles=ifiles,users=userl,messd=messd)

@app.route('/deletepost', methods = ['POST', 'GET'])
def deletepost():
    if request.method == 'POST':
        index = request.form['index']
        cursor = mysql.connection.cursor()
        username=Snaptalk.deletep(index)
        print(username)
        resultt = cursor.execute(f"SELECT * FROM `walldata` WHERE `username`= '{username}' ")
        data=cursor.fetchall()
        index=0
        newdata=[]
        for row in data:
            row=list(row)
            image = row[4]
            image=b64encode(image).decode("utf-8")
            im = Image.open(BytesIO(row[4]))
            index += 1
            im.save(f'static/imgw/result{index}.png')
            row[4]=f'/imgw/result{index}.png'
            newdata.append(row)
        newdata=sorted(newdata, key=itemgetter(0), reverse=True)
        nresultt = cursor.execute(f"SELECT * FROM `nsnaptalk` WHERE `uname`= '{username}@gmail.com' ")
        datai=cursor.fetchone()
  
        ifiles = os.listdir('static/imgw')
        ifiles = ['imgw/' + file for file in ifiles]
        userl=Snaptalk.userlist()
        print(usernamel)
        if usernamel != username:
            ddbut="dbut"
        else:
            ddbut=""
        cursor.execute(f"SELECT * FROM `snapmess`" )
        messd=cursor.fetchall()
        cursor.close()
        return render_template("wall.html",dataa=newdata,usernamem=usernamel,ifiles=ifiles,infor=datai,dbut=ddbut,users=userl,messd=messd)

@app.route('/Homepage', methods = ['POST', 'GET'])
def Homepage():
    if request.method == 'POST':
        emp=os.listdir('static/imgw')
        for file in emp:
            os.remove(f'static/imgw/{file}')
        usernamee = request.form['username']
        cursor = mysql.connection.cursor()
        resultt = cursor.execute(f"SELECT * FROM `walldata` WHERE `username`= '{usernamee}' ")
        data=cursor.fetchall()
        index=0
        newdata=[]
        for row in data:
            row=list(row)
            image = row[4]
            image=b64encode(image).decode("utf-8")
            im = Image.open(BytesIO(row[4]))
            index += 1
            im.save(f'static/imgw/result{index}.png')
            row[4]=f'/imgw/result{index}.png'
            newdata.append(row)
        newdata=sorted(newdata, key=itemgetter(0), reverse=True)
        nresultt = cursor.execute(f"SELECT * FROM `nsnaptalk` WHERE `uname`= '{usernamee}@gmail.com' ")
        datai=cursor.fetchone()
        cursor.execute(f"SELECT * FROM `snapmess`" )
        messd=cursor.fetchall()
        cursor.close()
        print(usernamel)
        userl=Snaptalk.userlist()
        if usernamel != usernamee:
            ddbut="dbut"
        else:
            ddbut=""
        return render_template('wall.html',dataa=newdata,usernamem=usernamel,infor=datai,dbut=ddbut,users=userl,messd=messd)



if __name__ == "__main__":
  app.run(debug=True,port=8000)