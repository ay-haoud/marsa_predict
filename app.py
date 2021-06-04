from flask import Flask, render_template, request, session, url_for, g, redirect
import jsonify
import requests
import pickle
import numpy as np
import pandas as pd
import sklearn
import matplotlib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Anthony', password='password'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Carlos', password='somethingsimple'))

app = Flask(__name__)


app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('admin'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')


df = pd.read_csv("HR_comma_sep.csv")
feats = ['sales','salary']
df_final = pd.get_dummies(df,columns=feats ,drop_first=True)
X = df_final.drop(['left'],axis=1).values
y = df_final['left'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

svc_wo_linear_kernel = SVC()
svc_wo_linear_kernel.fit(X_train, y_train)

@app.route('/', methods=['GET'])
def Home():
    return render_template('layout.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        Satisfaction = float(request.form['Satisfaction'])
        Évaluation = float(request.form['Évaluation'])
        nb_Projets = int(request.form['nb_Projets'])
        Heures = int(request.form['Heures'])
        Temps = int(request.form['Temps'])
        Accident = int(request.form['Accident'])
        Promotion = int(request.form['Promotion'])
        profession = request.form['profession']
        if(profession == 'Techniciens engins de levage'):
            Tech_eng_lev = 1
            Chef_descale= 0
            Agent_parc = 0
            Chef_déquipe = 0
            Chef_zone = 0
            Magasinier = 0
            Repos_pointeur = 0
            Tech_parc = 0
            Agent_manutention = 0
            
            
                
        elif(profession == 'Chef d’escale'):
            Tech_eng_lev = 0
            Chef_descale= 1
            Agent_parc = 0
            Chef_déquipe = 0
            Chef_zone = 0
            Magasinier = 0
            Repos_pointeur = 0
            Tech_parc = 0
            Agent_manutention = 0
        
        elif(profession == 'Agent de parc'):
            Tech_eng_lev = 0
            Chef_descale= 0
            Agent_parc = 1
            Chef_déquipe = 0
            Chef_zone = 0
            Magasinier = 0
            Repos_pointeur = 0
            Tech_parc = 0
            Agent_manutention = 0
        
        elif(profession == 'Chef d’équipe'):
            Tech_eng_lev = 0
            Chef_descale= 0
            Agent_parc = 0
            Chef_déquipe = 1
            Chef_zone = 0
            Magasinier = 0
            Repos_pointeur = 0
            Tech_parc = 0
            Agent_manutention = 0
        
        elif(profession == 'Chef de zone'):
            Tech_eng_lev = 0
            Chef_descale= 0
            Agent_parc = 0
            Chef_déquipe = 0
            Chef_zone = 1
            Magasinier = 0
            Repos_pointeur = 0
            Tech_parc = 0
            Agent_manutention = 0
        
        elif(profession == 'Magasinier'):
            Tech_eng_lev = 0
            Chef_descale= 0
            Agent_parc = 0
            Chef_déquipe = 0
            Chef_zone = 0
            Magasinier = 1
            Repos_pointeur = 0
            Tech_parc = 0
            Agent_manutention = 0
        
        elif(profession == 'Repos pointeur'):
            Tech_eng_lev = 0
            Chef_descale= 0
            Agent_parc = 0
            Chef_déquipe = 0
            Chef_zone = 0
            Magasinier = 0
            Repos_pointeur = 1
            Tech_parc = 0
            Agent_manutention = 0
        
        elif(profession == 'Techniciens parc'):
            Tech_eng_lev = 0
            Chef_descale= 0
            Agent_parc = 0
            Chef_déquipe = 0
            Chef_zone = 0
            Magasinier = 0
            Repos_pointeur = 0
            Tech_parc = 1
            Agent_manutention = 0
        
        else:
            Tech_eng_lev = 0
            Chef_descale= 0
            Agent_parc = 0
            Chef_déquipe = 0
            Chef_zone = 0
            Magasinier = 0
            Repos_pointeur = 0
            Tech_parc = 0
            Agent_manutention = 1
            
        salaire = request.form['salaire']
        if(salaire == 'Faible'):
            salaire_faib = 1
            salaire_moye = 0
        else:
            salaire_faib = 0
            salaire_moye = 1
        prediction = svc_wo_linear_kernel.predict([[Satisfaction,Évaluation,nb_Projets,Heures,Temps,Accident,Promotion,Tech_eng_lev,Chef_descale,Agent_parc,Chef_déquipe,Chef_zone,Magasinier,Repos_pointeur,Tech_parc,Agent_manutention,salaire_faib,salaire_moye]])
        if (prediction > 0.5):
             return render_template('layout.html',prediction_text="L'employé quittera marsa maroc")
        else:
             return render_template('layout.html',prediction_text="L'employé ne quittera pas marsa maroc")

                
if __name__=="__main__":
    app.run(debug=True)