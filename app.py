from flask import Flask, render_template, request, send_file, redirect
import pandas as pd
import requests
import json
from datetime import datetime

req_count = 0
prev_req_day = datetime.now().date()

def check_limit(initChk):
    curr_date = datetime.now().date()
    global req_count, prev_req_day
    if curr_date != prev_req_day:
        req_count = 0
        prev_req_day = curr_date
    if req_count >= 3:
        return True
    else:
        if not initChk:
            req_count += 1
            print(prev_req_day, req_count)
        return False

def genCsv(data):
    review = []
    sentiment = []
    confidence = []
    try:
        for ele in data:
            review.append(ele['Review'])
            sentiment.append(ele['Sentiment'])
            confidence.append(ele['Confidence'])
        df = pd.DataFrame({'Review':review,'Sentiment':sentiment,'Confidence':confidence})
        df.to_csv('./data.csv', index=False)
        return True
    except Exception as e:
        print(f"An Error occurred at parsing data of csv. : {e}")
        return False


app = Flask(__name__)

@app.route('/')
def home():
    requests.get('https://kshitijnegi12-amazon-customer-review.onrender.com')
    return render_template('index.html')

@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == 'POST':
        try:
            link = request.form['link']
            if len(link) > 0 and link.startswith('https://www.amazon.in/'):
                if check_limit(True):
                    return render_template('limit.html')
                svLink = 'https://kshitijnegi12-amazon-customer-review.onrender.com/get-amazon-reviews'
                response = requests.post(svLink, data = {'link' : link})
                if(response.status_code == 502):
                    return render_template('index.html', page='server_not_responding')
                if response.status_code == 200 and genCsv(json.loads(response.text)):
                    if check_limit(False):
                        return render_template('limit.html')
                    return render_template('index.html', page='download')
                else:
                    return render_template('index.html', page='error')
            else:
                return render_template('index.html', page='wrong_link')
        except Exception as e:
            print(f"Error when processing Link: {e}")
            return render_template('limit.html')
    else:
        return redirect('/')

@app.route('/download_data', methods=['POST','GET'])
def download_data():
    file_path = './data.csv'
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
      app.run()