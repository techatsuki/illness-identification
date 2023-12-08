from flask import Blueprint, render_template, request,Flask,make_response, redirect,flash, url_for, render_template,request,session,jsonify, send_file
from flask_login import login_required, current_user
from .models import User, details
from . import db 
from reportlab.pdfgen import canvas
import io,sqlite3
from io import BytesIO
import csv
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("index.html", user=current_user)

@views.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    return render_template("about.html", user=current_user)

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    return render_template("contact.html", user=current_user)

@views.route('/disease', methods=['GET', 'POST'])
@login_required
def disease():
    return render_template("doctor.html", user=current_user)
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
        # detail = details.query.filter_by(id=id).first()
        # email = details.email
        # fname = details.fname
        # lname = details.lname
        # diseases =details.diseases
        # city = details.city
        # address = details.address
        # phone = details.phone
        # dob=details.dob
        #,email=email,fname=fname,lname=lname,diseases=diseases,city=city,address=address,phone=phone,dob=dob
        return render_template("profile.html", user=current_user)
@views.route('/profile-edit', methods=['GET', 'POST'])
@login_required
def profileedit():
    if request.method == 'POST':
        print("POST METHOD MOVING")
        email = request.form.get('email')
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        diseases = request.form.get('diseases')
        city = request.form.get('location')
        address = request.form.get('address')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        #detail=details.query.filter_by(email=email).first()
        new_user = details(email=email, fname=fname,lname=lname, diseases=diseases, city=city, address=address,phone=phone, dob=dob,user_id=current_user.id)
        #print(new_user)
        db.session.add(new_user)
        db.session.commit()
        flash('Details Updated', category='success')
        return redirect(url_for('views.profileedit'))
   
    return render_template("profileedit.html",user=current_user)

@views.route('/cal_h', methods=['GET', 'POST'])
def cal_h():
    if request.method == "POST":
        age=request.form["age"]
        sex=request.form["sex"]
        cp=request.form["cp"]
        trestbps=request.form["trestbps"]
        chol=request.form["chol"]
        fbs=request.form["fbs"]
        restecg=request.form["restecg"]
        thalach=request.form["thalach"]
        oldpeak=request.form["oldpeak"]
        import numpy as np
        features = np.array([[age,	sex, cp, trestbps, chol , fbs, restecg, thalach, oldpeak]])
        import pandas as pd
        dataset=pd.read_csv('website\dataset\heart.csv')
        dataset=dataset.drop(['exang'],axis=1)
        dataset=dataset.drop(['slope'],axis=1)
        dataset=dataset.drop(['ca'],axis=1)
        dataset=dataset.drop(['thal'],axis=1)
        X=dataset.iloc[:,:-1].values
        y=dataset.iloc[:, -1].values
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=1729)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        from sklearn import metrics
        accuracy = metrics.accuracy_score(y_test, y_pred)
        accuracy=round(accuracy*100)
        prediction = classifier.predict(features)
        print("Prediction: {}".format(prediction))
        
        if prediction == [0]:
           return render_template("success.html", accuracy=accuracy)
        else:
            return render_template("sorry.html", accuracy=accuracy)                     
    else:
        return render_template("heart.html",user=current_user)

    
@views.route('/cal_d', methods=['GET', 'POST'])
def cal_d():
    if request.method == "POST":
        Pregnancies=request.form["Pregnancies"]
        Glucose=request.form["Glucose"]
        Insulin=request.form["Insulin"]
        BMI=request.form["BMI"]
        Age=request.form["Age"]
        BloodPressure=request.form["BloodPressure"]
        SkinThickness=request.form["SkinThickness"]
        import numpy as np
        import pandas as pd
        dataset=pd.read_csv('website\dataset\diabetes.csv')
        dataset=dataset.drop(['DiabetesPedigreeFunction'],axis=1)
        X=dataset.iloc[:,:-1].values
        y=dataset.iloc[:, -1].values
        from sklearn.model_selection import train_test_split
        X_train, X_test , y_train , y_test  = train_test_split(X, y ,test_size = 0.3, random_state  = 41 )
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=1529)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        from sklearn import metrics
        accuracy = metrics.accuracy_score(y_test, y_pred)
        accuracy=round(accuracy*100)
        import numpy as np
        features = np.array([[Pregnancies,	Glucose,	BloodPressure,	SkinThickness	,Insulin,	BMI,	Age]])
        prediction = classifier.predict(features)
        print("Prediction: {}".format(prediction))
        if prediction == [0]:
           return render_template("success.html", accuracy=accuracy)
        else:
            return render_template("sorry.html", accuracy=accuracy)                     
    else:
        return render_template("diabetes.html",user=current_user)




@views.route('/cal_s', methods=['GET', 'POST'])
def cal_s():
    if request.method == "POST":
        
        import pandas as pd
        import numpy as np
        df=pd.read_csv('website\dataset\stroke.csv')
        df.dropna(axis=0, inplace=True)
        from sklearn.preprocessing import LabelEncoder, OneHotEncoder
        label_encoder = LabelEncoder()
        df['gender'] = label_encoder.fit_transform(df['gender'])
        df['ever_married'] = label_encoder.fit_transform(df['ever_married'])
        df['work_type'] = label_encoder.fit_transform(df['work_type'])
        df['Residence_type'] = label_encoder.fit_transform(df['Residence_type'])
        df['smoking_status'] = label_encoder.fit_transform(df['smoking_status'])
        df=df.drop(['id'],axis=1)
        df=df.drop(['heart_disease'],axis=1)
        X=df.iloc[:,:-1].values
        y=df.iloc[:, -1].values
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
        from sklearn.ensemble import RandomForestClassifier
        classifier = RandomForestClassifier(n_estimators=10, criterion="entropy", random_state=1329)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        from sklearn import metrics
        accuracy = metrics.accuracy_score(y_test, y_pred)
        accuracy=round(accuracy*100)
        gender=request.form["gender"]
        age=request.form["age"]
        hypertension=request.form["hypertension"]
        ever_married=request.form["ever_married"]
        work_type=request.form["work_type"]
        Residence_type=request.form["Residence_type"]
        avg_glucose_level=request.form["avg_glucose_level"]
        bmi=request.form["bmi"]
        smoking_status=request.form["smoking_status"]
        import numpy as np
        features = np.array([[gender,age,	hypertension,ever_married,work_type,Residence_type,avg_glucose_level,bmi,smoking_status]])
        print(features)
        prediction = classifier.predict(features)
        print("Prediction: {}".format(prediction))
        if prediction == [0]:
           return render_template("success.html", accuracy=accuracy)
        else:
            return render_template("sorry.html", accuracy=accuracy)                     
    else:
        return render_template("stroke.html",user=current_user)


@views.route('/success')
def success():
    return render_template("success.html",user=current_user)

@views.route('/sorry')
def sorry():
    return render_template("sorry.html",user=current_user)
user_details = {
    "name": "Saran",
    "email": "Saran152004s@gmail.com",
    "age": 18,     
    "address": "theni"
}

def details():
      # Connect to the database
    conn = sqlite3.connect('database.db')
    
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Execute a SELECT query
    cursor.execute('SELECT * FROM users')
    
    # Fetch all results
    data = cursor.fetchall()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    return render_template('index.html', data=data)

@views.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    response = make_response(create_pdf())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=user_details.pdf'
    return response
def create_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    # Set font and font size
    p.setFont("Helvetica", 12)
    
    # Write user details to PDF
    for key, value in user_details.items():
        p.drawString(100, 700, f"{key}: {value}")
        p.translate(0, -20)  # Move down for the next line
    
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
@views.route('/download')
def index():
    return render_template('download.html')
@views.route('/bmi')
def bmi():
    return render_template('bmi.html')
@views.route('/def')
def definition():
    return render_template('definition.html')