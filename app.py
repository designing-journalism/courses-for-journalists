from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import pandas as pd
import json
import os
import quiz as qz
import scoring as sc
import filtering as fl

load_dotenv()
app = Flask(__name__)

# Assuming you have a file named 'data.csv'
DATA_FILE = 'data/Elearnings.xlsx'
#df = pd.read_csv(DATA_FILE, delimiter=';')
df = pd.read_excel(DATA_FILE,sheet_name='AI - Elearning')
df['Tijdsinvestering'] = df['Tijdsinvestering'].astype(float)
df['Niveau'] = df['Niveau'].astype(int)
df['Link'] = df['Link'].fillna("Not available")

# Serve all elearnings
@app.route('/')
def serve_elearning_page():
    return render_template('elearnings.html')

#view results after quiz
@app.route('/elearning')
def elearning():
    # Extract the score from the query parameter, default to 0 if not provided
    score = request.args.get('score', default=0, type=int)
    topic = request.args.get('topic', default=None)
    time = request.args.get('time', default=None, type = float)
    
    # Fetch categories based on the score (this part is up to you to implement)
    # For demonstration, this will just pass the score to the template
    return render_template('elearnings.html', score=score, topic=topic, time=time)

# route for getting all data via API
@app.route('/data', methods=['GET'])
def get_elearnings():
    level = sc.get_score(request.args.get('score', default=0, type=int))
    topics = request.args.get('topic', '').split(',')  # Split the comma-separated string into a list
    time = request.args.get('time', default=None, type = float)
    category = request.args.get('category', default=None)

    result = fl.get_filtered_data(df, category, topics, time, level)
    return result
    
#
#@app.route('/tmp', methods=['GET'])
#def filter_results():
#    level = sc.get_score(request.args.get('score', default=0, type=int)) #is kolom 'niveau' in de excel
#    category = request.args.get('category', default=None) #is kolom 'type' in de excel
#    topic = request.args.get('topic', default=None) # is kolom 'onderwerp' in de excel
#    time = request.args.get('time', default=None) # is kolom 'tijdsinvestering' in de excel
#    result = fl.get_filtered_data(category, topic, time, level) 
#    return result
  
@app.route('/quiz')
def quiz():
    # Assuming you have a quiz.html in your templates directory
    return render_template('quiz.html')

@app.route('/quiz/question/<int:question_id>')
def quiz_question(question_id):
    # Use the imported get_question function
    question_data = qz.get_question(question_id)
    return jsonify(question_data)


if __name__ == '__main__':
    #app.run(debug=True)
    #host = os.getenv('HOST', '0.0.0.0')
    #port = int(os.getenv('PORT', os.environ.get('PORT', 10000)))
    app.run(host='0.0.0.0', port=10000)  # Bind to 0.0.0.0 and port 5000
    #app.run(port=port, debug=True)
