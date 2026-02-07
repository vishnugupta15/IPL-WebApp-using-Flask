from flask import Flask,render_template,redirect,request,session,jsonify
import requests
from db import Database
import api

app = Flask(__name__)
app.secret_key = "213456" 

dbo = Database()
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration',methods=['post'])
def perform_registration():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    response = dbo.insert(name,email,password)
    if response:
        return render_template('login.html',success_message='Registration successful. Kindly proceed to login')
    else:
        return render_template('login.html',error_message = 'Email already Exists. Kindly Login')


@app.route('/perform_login',methods = ['post'])
def perform_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    response = dbo.search(email,password)
    
    if response == 0:
        return render_template('register.html',error_message = 'User not found. Kindly Register first')
    elif response == 1:
        session['logged_in'] = 1 
        return redirect('/dashboard')
    elif response == 2:
        return render_template('login.html', error_message='Wrong Password. Try again')
    
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in') == 1:
        return render_template('dashboard.html')
    else: 
        return redirect('/')

# all teams data
@app.route('/api/teams')
def api_teams():
    data = api.teamsAPI()
    return jsonify(data)

@app.route('/teams')
def teams_page():
    if session.get('logged_in') == 1:
        return render_template('teams.html')
    else: 
        return redirect('/')
    
# show the team stat
@app.route('/api/team-stats')
def api_team_stats():
    team = request.args.get('team')  # e.g., /api/team-stats?team=Mumbai%20Indians
    if not team:
        return jsonify({"error": "Please provide a team name"}), 400
    
    data = api.allRecordAPI(team)  # returns JSON string
    return data  # already JSON serialized

@app.route('/team-stats')
def team_stats_page():
    if session.get('logged_in') == 1:
        return render_template('team_stats.html')
    else:
        return redirect('/')

# batsman names

@app.route('/api/batsmen')
def api_batsmen():
    # Get unique batsmen from the balls dataset
    batsmen = sorted(api.batter_data['batter'].unique())  # sort alphabetically
    return jsonify({"batsmen": batsmen})

# batsman stat
@app.route('/api/batsman-stats')
def api_batsman_stats():
    batsman = request.args.get('batsman')
    if not batsman:
        return jsonify({"error": "Please provide a batsman name"}), 400

    data = api.batsmanAPI(batsman)
    print(type(data))
    return jsonify(data)

@app.route('/batsman-stats')
def batsman_stats_page():
    if session.get('logged_in') == 1:
        return render_template('batsman_stats.html')
    else:
        return redirect('/')

#bowler name
@app.route('/api/bowlers')
def api_bowlers():  
    # Get unique bowler from the balls dataset
    bowler = sorted(api.bowler_data['batter'].unique())  # sort alphabetically
    return jsonify({"bowler": bowler})

# bowler stat
@app.route('/api/bowler-stats')
def api_bowler_stats():
    bowler = request.args.get('bowler')
    if not bowler:
        return jsonify({"error": "Please provide a bowler name"}), 400

    data = api.bowlerAPI(bowler)
    return jsonify(data)

@app.route('/bowler-stats')
def bowler_stats_page():
    if session.get('logged_in') == 1:
        return render_template('bowler_stats.html')
    else:
        return redirect('/')

# team vs team stat
@app.route('/api/teamvteam')
def api_teamvteam():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    
    result = api.teamVteamAPI(team1,team2)
    response = jsonify(result)
    return response

@app.route('/team-vs-team')
def team_vs_team_page():
    if session.get('logged_in') == 1:
        return render_template("teamvteam.html")
    else: 
        return redirect('/')

# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)