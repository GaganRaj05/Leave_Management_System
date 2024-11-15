from flask import Flask, render_template, flash, redirect, url_for,session
from forms import LoginForm, WriteALeave, viewLetter,editStudent,editstaff,AddStudent,AddStaff
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)
app.config['SECRET_KEY'] = '152255'
app.config['MYSQL_DB'] = "leave_management"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Wanderer89"



@app.route("/", methods=["GET", "POST"])
def login():#----------------------------------------------------------------------------------------------------
    form = LoginForm()
    session['user_id']=None
    session['username']=None
    if form.validate_on_submit() :
        usern = form.username.data
        passw = form.password.data
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, Password FROM Admin WHERE id = %s AND Password = %s", (usern, passw))
        admin = cursor.fetchone()
        if admin:
            session['user_id']=admin[0]
            flash(f"Logged in successfully as Admin", "success")
            return redirect(url_for("admin"))
        else:
            cursor.execute("SELECT id,Student_name,Password FROM STUDENT WHERE id = %s AND Password = %s", (usern, passw))
            student = cursor.fetchone()
            if student:
                session['user_id']=student[0]
                session['username']=student[1]
                return redirect(url_for("home", username = student[1] ))
            else:
                cursor.execute("SELECT id,F_name, Password FROM TEACHERS WHERE id = %s AND Password = %s", (usern, passw))
                teacher = cursor.fetchone()
                if teacher:
                    session['user_id']=teacher[0]
                    session['username']=teacher[1]
                    name = teacher[1]
                    return redirect(url_for("teacher", name = name))
                else:
                    cursor.execute("select F_name from WARDON where id = %s and Password=%s",(usern, passw))
                    wardon = cursor.fetchone()
                    if wardon:
                        session['user_id']=form.username.data
                        session['username']=wardon[0]
                        return redirect(url_for("wardon", username = wardon[0]))
                    else:
                        flash(f"Log in Unsuccessfull","danger")
                    
    return render_template("login.html", form=form)

@app.route("/photos")#------------------------------------------------------------------------------------------------------
def photos():
    if session.get('user_id')==None or session.get('username')==None:
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    return render_template("photos.html")



@app.route("/leave",methods=['GET','POST'])#-----------------------------------------------------------------------------
def leave():
    if session.get('user_id')==None or session.get('username')==None:
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    sid=session.get('user_id')
    sname=session.get('username')
    form = WriteALeave()
    if(form.cancel.data):
        flash(f"Letter discarded","danger")
        return redirect(url_for('home'))
    elif(form.submit.data):
        cursor = mysql.connection.cursor()
        dateFrom = form.dFrom.data
        dateTill = form.dTo.data
        username = form.by.data
        userId = form.to.data
        reg_no = form.roll_no.data        
        sub = form.subject.data
        res = form.bodyL.data
        cursor.execute("Select id from TEACHERS where id=%s ",(userId,))
        teacher = cursor.fetchone()
        if teacher:
            cursor.execute("select max(Application_id) from Letters ")
            appId = cursor.fetchone()
            newAppId = ""
            if appId[0] is not None:
                newAppId = appId[0]+1
            else:
                newAppId = 1
            status='0'
            cursor.execute("insert into Letters values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userId,dateFrom,dateTill,username,reg_no,sub,res,newAppId,status))
            mysql.connection.commit()
            cursor.execute("select L_count from LettersCount where id = %s",(userId,))
            val = cursor.fetchone()
            if val is not None:
                newCount = val[0]+1
                cursor.execute("update LettersCount set L_count = %s where id = %s",(newCount,userId))
                mysql.connection.commit()
            else:
                cursor.execute("update LettersCount set values= %s where id=%s",(1,userId))
                mysql.connection.commit()
            
            flash(f"Letter submited successfully","success")
            return redirect(url_for("home",username=sname))
        else:
            flash(f"Please enter a valid id","danger")
            return redirect(url_for("leave",sid=sid))
    
    return render_template("leave.html", form = form,sid=sid,sname=sname)

@app.route("/logout")
def logout():
    session.pop('user_id',None)
    flash(f"Logged out successfully","success")
    return redirect(url_for('login'))

@app.route("/home/<username>")
@app.route("/home")#-----------------------------------------------------------------------------
def home(username=None):
    stid=session.get('user_id')
    if stid is None or session.get('username')!=username:
        session.pop('user_id',None)
        session.pop('username',None)
        flash(f"Login required","dark")
        return redirect(url_for('login'))
    else:
        if username is not None:
            cursor = mysql.connection.cursor()
            cursor.execute("select id from STUDENT where Student_name = %s",(username,))
            sid=cursor.fetchone()
            return render_template("Home.html", username=username,sid=sid[0])
        else:
            flash(f"Your name is not in the Ledger","danger")
            return redirect(url_for('login'))


@app.route("/admin")#----------------------------------------------------------------------------
def admin():
    if session.get('user_id') == None :
        flash("Login required","danger")
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("select count(id) from STUDENT")
    stCount = cursor.fetchone()
    
    cursor.execute("select count(id) from TEACHERS")
    tCount = cursor.fetchone()
    
    cursor.execute("select * from LettersApproved")
    data=cursor.fetchall()
    
    cursor.execute("select sum(L_count) from LettersCount")
    sL = cursor.fetchone()
    
    
    return render_template("admin.html", title = "Admin",stCount=stCount,tCount=tCount,data=data, sL=sL)

@app.route("/teacher/<name>")#--------------------------------------------------------------------
@app.route("/teacher")#ind->teacher's id,lcount->Letter's Count,sname->Student name,sid->Student id
def teacher(name = None):
    if session.get('user_id') == None or session.get('username')!= name:
        session.pop('user_id',None)
        session.pop('username',None)
        flash(f"Login required","danger")
        return redirect(url_for('login'))
    if name is not None:
        cursor = mysql.connection.cursor()
        cursor.execute("select id from TEACHERS where F_name = %s ",(name,))
        ind = cursor.fetchone()
        if ind:
            cursor.execute("select L_count from LettersCount where id = %s",(ind[0],))
            count = cursor.fetchone()[0]
            cursor.execute("select Name from Letters where id=%s and status=0",(ind[0],))
            sname = cursor.fetchall()
            cursor.execute("select Letters_approved from lettersstatus where tId = %s ",(ind[0],))
            approved = cursor.fetchone()
            cursor.execute("select Letters_declined from lettersstatus where tId= %s",(ind[0],))
            declined = cursor.fetchone()
            cursor.execute("select Reg_no from Letters where id=%s and status =0",(ind[0],))
            sid = cursor.fetchall()
            
            cursor.execute("select application_id from letters where id=%s and status = 0",(ind[0],))
            appId = cursor.fetchall()
            return render_template("teacher.html",name = name, count=count, sid = sid, sname = sname,approved=approved,declined=declined, appId=appId, ind=ind[0])
        else:
            flash(f"Invalid Username ")
            return redirect(url_for("login"))
        
    return render_template("teacher.html", name="Lecturer")
    
    
    
    
@app.route("/wardon/<username>")
@app.route("/wardon")#---------------------------------------------------------------------
def wardon(username = None):
    if session.get('user_id') == None or session.get('username')!=username:
        session.pop('user_id',None)
        session.pop('username',None)
        flash(f"Login required","danger")
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()
    
    cursor.execute("select Name,Reg_no,DateFrom,DateTo from Lettersapproved")
    data = cursor.fetchall()
    return render_template("wardon.html",data=data,username=username)

@app.route("/contact")#-------------------------------------------------------------------
def contact():
    return render_template("contact.html")

@app.route("/tracking")#------------------------------------------------------------------
def tracking():
    if session.get('user_id')==None or session.get('username')==None:
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    sid=session.get("user_id")
    cursor=mysql.connection.cursor()
    cursor.execute("select * from lettersapproved where Reg_no=%s",(sid,))
    data=cursor.fetchall()
    cursor.execute("select application_id, id, Name, Reg_no, DateFrom, DateTo from Letters where Reg_no=%s",(sid,))
    sentData = cursor.fetchall()
    
    cursor.execute("select application_id, tId, Name, Reg_no,DateFrom, DateTo from LettersDeclined where Reg_no=%s",(sid,))
    decData=cursor.fetchall()
    return render_template("tracking.html",sid=sid,data=data,sentData=sentData,decData=decData)

@app.route("/view/<sid>/<appId>/",methods=["GET","POST"])#---------------------------------
@app.route("/view",methods=["GET","POST"])
def view(sid = None, appId=None):
    if session.get('user_id')==None or session.get('username')==None:
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    form = viewLetter()
    tName=""
    cursor = mysql.connection.cursor()
    if (form.approve.data):
        cursor.execute('select Name from Letters where Reg_no = %s and application_id=%s',(sid,appId))
        name = cursor.fetchone()
        print("Student name",name)
        cursor.execute('select id from Letters where Reg_no = %s and Application_id=%s',(sid,appId))
        tid = cursor.fetchone()
        print("Teachers id",tid)
        cursor.execute("select DateFrom from Letters where Reg_no=%s and Application_id=%s",(sid,appId))
        dateFro = cursor.fetchone()
        print("Date From",tid)
        cursor.execute("select DateTo from Letters where Reg_no=%s and application_id=%s",(sid,appId))
        dateTo=cursor.fetchone()
        print("Date to",dateTo)
        cursor.execute('select F_name from TEACHERS where id = %s',(tid,))
        tName = cursor.fetchone()
        print("Teachers name",tName)
        cursor.execute("select letters_approved from Lettersstatus where tId=%s",(tid,))
        appCount=cursor.fetchone()
        print("This is application count:",appCount)
        if appCount[0] is not None:
            newCount =appCount[0]+1        
            cursor.execute("update LettersStatus set Letters_approved = %s where tId=%s",(newCount,tid))
            mysql.connection.commit()
        else:
            newCount =1        
            cursor.execute("update LettersStatus set Letters_approved = %s where tId=%s",(newCount,tid))
            mysql.connection.commit()
        state =1
        cursor.execute("update LETTERS set status= %s where id =%s and Application_id=%s",(state,tid,appId))
        mysql.connection.commit()
        cursor.execute("insert into LettersApproved values(%s,%s,%s,%s,%s,%s)",(tid,sid,name,dateFro,dateTo,appId))
        mysql.connection.commit()
        flash(f"Letters approved succesfully","success")
    elif(form.decline.data):
        cursor.execute('select Name from Letters where Reg_no = %s and Application_id=%s',(sid,appId))
        name = cursor.fetchone()
        print("this",name)
        cursor.execute('select id from Letters where Reg_no = %s and application_id=%s',(sid,appId))
        tid = cursor.fetchone()
        print("this",tid)
        cursor.execute('select F_name from TEACHERS where id = %s',(tid,))
        tName = cursor.fetchone()
        print("this",tName)
        cursor.execute("select DateFrom from Letters where Reg_no=%s and Application_id=%s",(sid,appId))
        dateFro = cursor.fetchone()
        print("This is",dateFro)
        cursor.execute("select DateTo from Letters where Reg_no=%s and application_id=%s",(sid,appId))
        dateTo=cursor.fetchone()
        print("this",dateTo)
        cursor.execute("select letters_declined from Lettersstatus where tId=%s",(tid,))
        decCount=cursor.fetchone()
        print(decCount)
        if decCount[0] is not None:
            newCount =decCount[0]+1        
            cursor.execute("update LettersStatus set Letters_declined = %s where tId=%s",(newCount,tid))
            mysql.connection.commit()
        else:
            newCount =1        
            cursor.execute("update LettersStatus set Letters_declined = %s where tId=%s",(newCount,tid))
            mysql.connection.commit()
        state =1
        cursor.execute("update LETTERS set status= %s where id =%s and Application_id=%s",(state,tid,appId))
        mysql.connection.commit()
        cursor.execute("insert into LettersDeclined values(%s,%s,%s,%s,%s,%s)",(tid,name,sid,dateFro,dateTo,appId))
        mysql.connection.commit()
        state =1
        cursor.execute("update LETTERS set status= %s where id =%s and Application_id=%s",(state,tid,appId))
        mysql.connection.commit()
        flash(f"Letters declined successfully","danger") 
    else:
        cursor.execute('select id from Letters where Reg_no = %s',(sid,))
        tid = cursor.fetchone()
        print(appId)
        cursor.execute('select F_name from TEACHERS where id = %s',(tid,))
        tName = cursor.fetchone()
        if sid is not None:
            cursor.execute("select subject from Letters where Reg_no=%s and status=0",(sid,))
            sub = cursor.fetchone()

            cursor.execute("select reason from Letters where Reg_no=%s and status =0",(sid,))
            res = cursor.fetchone()
            cursor.execute("select dateFrom from Letters where Reg_no = %s and status =0",(sid,))
            dF = cursor.fetchone()[0]

            cursor.execute("select dateTo from Letters where Reg_no = %s",(sid,))
            dTo = cursor.fetchone()[0]
            
            cursor.execute("select Name from Letters where Reg_no = %s and status=0",(sid,))
            name = cursor.fetchone()

            return render_template("view.html",dF=dF,dTo=dTo,sub=sub,res=res, form=form, name=name, appId=appId)
        else:
            flash(f"Some error occured try again later")
    return redirect(url_for('teacher',name=tName[0]))

@app.route("/addStudent",methods=['GET','POST'])
def addStudent():
    if session.get('user_id')==None :
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    form = AddStudent()
    if form.cancel.data:
        flash(f"Student not added","success")
        return redirect(url_for('admin'))
    elif form.submit.data:
        
        sname=form.Name.data
        sid=form.RegNo.data
        sbranch=form.Branch.data
        sPassword=form.Password.data
        cursor=mysql.connection.cursor()
        cursor.execute("select id from STUDENT where id=%s",(sid,))
        check=cursor.fetchone()
        if check is not None:
            flash(f"The user id is taken please enter a new Id","danger")
            return redirect(url_for('addStudent'))
        cursor.execute("insert into STUDENT values(%s,%s,%s,%s)",(sname,sid,sPassword,sbranch))
        mysql.connection.commit()
        flash(f"Student added successfully","success")
        return redirect(url_for('admin'))
    return render_template("AddStudent.html",form=form)

@app.route("/addStaff",methods=['GET','POST'])
def addStaff():
    if session.get('user_id')==None :
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    form=AddStaff()
    
    if form.cancel.data:
        flash(f"staff not added","success")
        return redirect(url_for('admin'))
    elif form.submit.data:
        staffName=form.Name.data
        staffId=form.StaffId.data
        staffPassword=form.Password.data
        staffBranch=form.Branch.data
        
        cursor=mysql.connection.cursor()
        cursor.execute("select id from TEACHERS where id=%s",(staffId,))
        check=cursor.fetchone()
        if check is not None:
            flash(f"The user id is taken please enter a new Id","danger")
            return redirect(url_for('addStudent'))
        
        cursor.execute("insert into TEACHERS(F_name,id,Password,Branch) values(%s,%s,%s,%s)",(staffName,staffId,staffPassword,staffBranch))
        mysql.connection.commit()
        flash(f"Staff added successfully","success")
        return redirect(url_for('admin'))
    return render_template("AddStaff.html",form=form)


@app.route("/viewStudentDetails")
def viewSTD():
    if session.get('user_id')==None :
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    cursor=mysql.connection.cursor()
    cursor.execute("select Student_Name from STUDENT")
    STNAME=cursor.fetchall()
    cursor.execute("select id from STUDENT")
    ID=cursor.fetchall()
    cursor.execute("select Branch from STUDENT")
    BRANCH=cursor.fetchall()
    return render_template("viewDetails.html", BRANCH=BRANCH,ID=ID,STNAME=STNAME)
    

@app.route("/viewStaffDetails")
def viewSD():
    if session.get('user_id')==None:
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    cursor = mysql.connection.cursor()
    cursor.execute("select F_name,id,Branch from TEACHERS")
    data = cursor.fetchall()
    return render_template("viewSDetails.html",data=data)
    
    
@app.route("/Declined")
def declined():
    if session.get('user_id')==None or session.get('username')==None:
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    tid = session.get("user_id")
    cursor=mysql.connection.cursor()
    cursor.execute("select Name, Reg_no,DateFrom,DateTo,Application_id from Lettersdeclined where tId=%s",(tid,))
    data = cursor.fetchall()
    cursor.execute("select F_name from TEACHERS where id=%s",(tid,))
    tname=cursor.fetchone()[0]
    return render_template("declined.html",data=data,tname=tname)

@app.route("/edit/<id>",methods=['GET','POST'])
def edit(id=None):
    if session.get('user_id')==None :
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    form = editStudent()
    if form.cancel.data:
        return redirect(url_for('viewSTD'))
    elif form.submit.data:
        pId=id
        sid=form.RegNo.data
        sname=form.Name.data
        sPassword=form.Password.data
        sBranch = form.Branch.data
        
        cursor=mysql.connection.cursor()
        cursor.execute("UPDATE STUDENT SET Student_name=%s, Password=%s, Branch=%s WHERE id=%s", (sname, sPassword, sBranch, pId))
        mysql.connection.commit()
        cursor.execute("update LETTERS set name=%s where Reg_no=%s",(sname,pId))
        mysql.connection.commit()
        cursor.execute("update LETTERSapproved set name=%s where Reg_no=%s",(sname,pId))
        mysql.connection.commit()
        cursor.execute("update LettersDeclined set name=%s where Reg_no=%s",(sname,pId))
        mysql.connection.commit()
        return redirect(url_for('viewSTD'))
    else:
        return render_template("edit.html", sid=id, form=form)

@app.route("/delete/<id>")
def delete(id= None):
    cursor=mysql.connection.cursor()
    cursor.execute("delete from STUDENT where id=%s",(id,))
    mysql.connection.commit()
    return redirect(url_for('viewSTD'))

@app.route('/Approved')
def approved():
    if session.get('user_id')==None or session.get('username')==None:
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    tid = session.get('user_id')
    cursor = mysql.connection.cursor()
    cursor.execute("select Name, Reg_no,DateFrom,DateTo,Application_id from LettersApproved where tId=%s",(tid,))
    data=cursor.fetchall()
    cursor.execute("select F_name from TEACHERS where id=%s",(tid,))
    tname=cursor.fetchone()[0]
    return render_template("approved.html",data=data,tname=tname)

@app.route("/edit-Staff/<id>",methods=['GET','POST'])
def editStaff(id=None):
    if session.get('user_id')==None :
        flash(f"Login required","danger")
        return redirect(url_for('login')) 
    form = editstaff()
    staffId = id
    cursor=mysql.connection.cursor()
    if form.cancel.data:
        flash(f"Staff Details not edited","danger")
        return redirect(url_for('viewSD'))
    elif form.submit.data:
        staffName=form.Name.data
        staffPassword=form.Password.data
        staffBranch=form.Branch.data
        
        cursor.execute("update TEACHERS set F_name=%s,Password=%s,Branch=%s where id=%s ",(staffName,staffPassword,staffBranch,staffId))
        mysql.connection.commit()
        
        return redirect(url_for('viewSD'))
    else:
        return render_template("editStaff.html",form=form,staffId=staffId)
    
@app.route("/delete-Staff/<id>")
def deleteStaff(id = None):
    staffId=id
    cursor=mysql.connection.cursor()
    cursor.execute("delete from TEACHERS where id=%s",(staffId,))
    mysql.connection.commit()
    return redirect(url_for('viewSD'))
    
if __name__ == '__main__':
    app.run(debug=True)
