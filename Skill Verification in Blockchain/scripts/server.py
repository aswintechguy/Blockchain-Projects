import sqlite3
import sys
from datetime import datetime
sys.path.append("scripts")
from flask import render_template, Flask, request, session, redirect, url_for
from deploy import *

skillVerify = deploySkillVerify()
account = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
app = Flask(__name__)
app.secret_key = 'skillified'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    skill, proficiency, learning_id, project_id = skillVerify.retrieve(
        session['empId'])
    conn = sqlite3.connect('Skillified.db')
    cur=conn.cursor()
    cur.execute("SELECT  EmpName,EmailId, WorkExp FROM Employee where EmpID=?",[session['empId']])
    temp_emp=cur.fetchall()
    name, email, work_exp = temp_emp[0]
    emp_id = session['empId']
    data = []
    if skill:        
        for sk, p, learn, proj in zip(skill, proficiency, learning_id, project_id):
            query_sk = "SELECT skillID, skill1, skill2, Skill3, skill4 FROM Skills where skillID=%s" % (
                sk)
            cur = conn.cursor()
            cur.execute(query_sk)
            temp = cur.fetchall()
            data.append(list(temp[0]))
            data[-1].append(p)

            cur = conn.cursor()
            cur.execute("SELECT CourseName FROM LearningCourses where CourseID=?",[learn])
            temp = cur.fetchall()[0][0]
            data[-1].append(temp)

            cur = conn.cursor()
            cur.execute("SELECT ProjectName FROM Projects where ProjectID=?",[proj])
            temp = cur.fetchall()[0][0]
            data[-1].append(temp)

        conn.close()
    return render_template('profile.html', **locals())


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    session['empId'] = request.form['emp_id']
    name, emp_id, work_exp, email, password = request.form['name'], request.form['emp_id'], request.form['work_exp'], request.form['email'], request.form['password']
    global skillVerify
    # register in the database

    conn = sqlite3.connect('Skillified.db')
    cur=conn.cursor()
    cur.execute("INSERT INTO Employee (EmpId,EmpName,Password,EmailId,WorkExp) values(?,?,?,?,?)", [emp_id,name,password,email,work_exp])
    conn.commit()
    cur.close()
    conn.close()
    skillVerify.register(emp_id, {"from": account})
    return render_template('profile.html', **locals())

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    emp_id = request.form['empId']
    password = request.form['password']
    session['empId'] = emp_id
    data = []
    try:
        conn = sqlite3.connect('Skillified.db')
        cur = conn.cursor()
        cur.execute("SELECT Password from Employee where EmpID=?",[emp_id])
        _password=cur.fetchall()[0][0]
        print(_password)
        
        if _password == password:

            cur=conn.cursor()
            cur.execute("SELECT  EmpName,EmailId, WorkExp FROM Employee where EmpID=?",[session['empId']])
            temp_emp=cur.fetchall()
            name, email, work_exp = temp_emp[0]

            skill, proficiency, learning_id, project_id = skillVerify.retrieve(
                session['empId'])
            if skill:
                for sk, p, learn, proj in zip(skill, proficiency, learning_id, project_id):
                    query = "SELECT skillID, skill1, skill2, Skill3, skill4 FROM Skills where skillID=%s" % (
                        sk)
                    cur = conn.cursor()
                    cur.execute(query)
                    temp = cur.fetchall()
                    data.append(list(temp[0]))
                    data[-1].append(p)
                    cur = conn.cursor()
                    cur.execute("SELECT CourseName FROM LearningCourses where CourseID=?",[learn])
                    temp = cur.fetchall()[0][0]
                    data[-1].append(temp)
                    cur = conn.cursor()
                    cur.execute("SELECT ProjectName FROM Projects where ProjectID=?",[proj])
                    temp = cur.fetchall()[0][0]
                    data[-1].append(temp)
                conn.close()
            return render_template('profile.html', **locals())
        else:
            print('Password is wrong')
    except:
        print('''<script> alert('%s: User does not exist'); </script>''' % (emp_id))
        print("User does not exist")
    
    return render_template('index.html')


@app.route('/sentrequests', methods=['GET', 'POST'])
def sentrequests():
    global skillVerify
    srLength = skillVerify.getSentRequestsLength(session['empId'])
    data = []
    conn = sqlite3.connect('Skillified.db')
    if srLength > 0:
        for i in range(srLength):
            temp = []
            skill_id, proficiency, learning_id, project_id, date, verdict = skillVerify.retrieveSentRequests(
                session['empId'], i)
            temp.append(skill_id)
            
            query_sk = "SELECT skill1, skill2, Skill3, skill4 FROM Skills where skillID=%s" % (
                skill_id)
            cur = conn.cursor()
            cur.execute(query_sk)
            temp_sk = cur.fetchall()
            temp.extend(list(temp_sk[0]))

            temp.append(proficiency)
            
            cur = conn.cursor()
            cur.execute("SELECT CourseName FROM LearningCourses where CourseID=?",[learning_id])
            learn = cur.fetchall()[0][0]
            temp.append(learn)
            
            cur = conn.cursor()
            cur.execute("SELECT ProjectName FROM Projects where ProjectID=?",[project_id])
            proj = cur.fetchall()[0][0]
            temp.append(proj)
            temp.append(datetime.fromtimestamp(date))
            temp.append(verdict)
            
            data.append(temp)
        return render_template('sentrequests.html', **locals())
    else:
        return redirect(url_for('profile'))

@app.route('/receivedrequests', methods=['GET', 'POST'])
def receivedrequests():
    global skillVerify
    rrLength = skillVerify.getReceivedRequestsLength(session['empId'])
    data = []
    if rrLength > 0:
        conn = sqlite3.connect('Skillified.db')
        for i in range(rrLength):
            temp = []
            senderId, skill_id, proficiency, learning_id, project_id, date, verdict = skillVerify.retrieveReceivedRequests(
                session['empId'], i)

            cur = conn.cursor()
            cur.execute("SELECT EmpName from Employee where EmpID=?",[senderId])
            name=cur.fetchall()[0][0]
            temp.append(i)
            temp.append(name)
            temp.append(skill_id)

            query_sk = "SELECT skill1, skill2, Skill3, skill4 FROM Skills where skillID=%s" % (
                skill_id)
            cur = conn.cursor()
            cur.execute(query_sk)
            temp_sk = cur.fetchall()
            temp.extend(list(temp_sk[0]))

            temp.append(proficiency)
            cur = conn.cursor()
            cur.execute("SELECT CourseName FROM LearningCourses where CourseID=?",[learning_id])
            learn = cur.fetchall()[0][0]
            temp.append(learn)

            cur = conn.cursor()
            cur.execute("SELECT ProjectName FROM Projects where ProjectID=?",[project_id])
            proj = cur.fetchall()[0][0]
            temp.append(proj)

            temp.append(datetime.fromtimestamp(date))
            temp.append(verdict)
            data.append(temp)
        conn.close()
        return render_template('receivedrequests.html', **locals())
    else:
        return redirect(url_for('profile'))
    
@app.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    global skillVerify
    skill_id, proficiency, learning_id, project_id, reviewer_ids = request.form['skill_id'], request.form['proficiency'], request.form['learning_id'], request.form['project_id'], skillVerify.getEmployeeIds()
    reviewer_ids = list(reviewer_ids)
    reviewer_ids.remove(session['empId'])
    skillVerify.initiateRequest(
        session['empId'], skill_id, proficiency, learning_id, project_id, reviewer_ids, {"from": account})
    return redirect(url_for('profile'))


@app.route('/validate', methods=['GET', 'POST'])
def validate_request():
    global skillVerify
    index, verdict = request.form['index'], request.form['verdict']
    skillVerify.validateRequest(
        int(verdict), session['empId'], index, {"from": account})
    return profile()

@app.route('/logout')
def logout():
   # remove the empId from the session if it is there
   session.pop('empId', None)
   return redirect(url_for('index'))

def main():
    app.run(debug=True)

