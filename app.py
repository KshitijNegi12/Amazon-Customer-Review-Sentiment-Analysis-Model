import joblib
import pandas as pd
from flask import Flask, request, render_template, redirect, send_file
from text_filter import my_review_filter
from scraper import AmazonScraper
from datetime import datetime

model = None
vectorizer = None
req_count = 0
prev_req_date = datetime.now().date()

def init():
    global model,vectorizer
    model = joblib.load(r'Model/trained_model.pkl')
    vectorizer = joblib.load(r'Model/trained_vectorizer.pkl')

def startScraping(link):
    scraper = AmazonScraper(link)
    return scraper.run()

def check_limit():
    curr_date = datetime.now().date()
    global req_count, prev_req_date
    if curr_date != prev_req_date:
        req_count = 0
        prev_req_date = curr_date
    if req_count >= 3:
        return True
    else:
        return False

def sentimentSuccess():
    try:
        df1 = pd.read_csv(r'data.csv')
        if df1.empty:
            print("Error: data.csv is empty.")
            return False
        
        X = vectorizer.transform(df1['Review'])
        sentiment = model.predict(X)
        probability = model.predict_proba(X)
        sentiment=sentiment.flatten().tolist()

        confidence=[]
        for i in range(len(sentiment)):
            if sentiment[i] == 1:
                sentiment[i] = 'Positive'
                confidence.append(round(100*probability[i][2],2))
            elif sentiment[i] == 0:
                sentiment[i] = 'Neutral'
                confidence.append(round(100*probability[i][1],2))
            else:
                sentiment[i] = 'Negative'
                confidence.append(round(100*probability[i][0],2))

        df2=pd.DataFrame({'Sentiment':sentiment,'Confidence':confidence})
        df1['Sentiment']=df2['Sentiment']
        df1['Confidence']=df2['Confidence']
        df1.to_csv(r'data.csv', index=False)
        print("Sentiment Analysis Successfull.")
        return True
    except Exception as e:
        print(f"An Error occurred at parsing data of csv. : {e}")
        return False


# Flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST','GET'])
def result():
    if(model==None):init()
    if request.method == 'POST':
        try:
            link = request.form['link']
            if len(link) > 0 and link.startswith('https://www.amazon.in/'):
                if check_limit():
                    return render_template('limit.html')
                # empty the data.csv
                df=pd.DataFrame()
                df.to_csv(r'data.csv', index=False)
                # start scraping and get result
                if startScraping(link) and sentimentSuccess():
                    global req_count, prev_req_date
                    req_count += 1
                    print(f'Count and date: {req_count}, {prev_req_date}')
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
    
@app.route('/download_data', methods=['GET'])
def download_data():
    file_path = './data.csv'
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run()
