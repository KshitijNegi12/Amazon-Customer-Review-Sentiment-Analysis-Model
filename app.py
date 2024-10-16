import joblib
import pandas as pd
from flask import Flask, render_template, request, send_file, redirect
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from amazon.amazon.spiders.amspy import AmspySpider
from text_filter import my_review_filter
from datetime import datetime

model = None
vectorizer = None
req_count = 0
prev_req_day = datetime.now().date()

def init():
    global model,vectorizer
    model = joblib.load(r'./Model/trained_model.pkl')
    vectorizer = joblib.load(r'./Model/trained_vectorizer.pkl')

def calc():
    try:
        df1 = pd.read_csv('./data.csv')
        if df1.empty: return 0
        X = vectorizer.transform(df1['text'])
        sentiment = model.predict(X)
        probability = model.predict_proba(X)
        sentiment=sentiment.flatten().tolist()
        confidence=[]
        for i in range(len(sentiment)):
            if sentiment[i] == 1:
                sentiment[i] = 'Positive'
                confidence.append(round(100*probability[i][1],2))
            else:
                sentiment[i] = 'Negative'
                confidence.append(round(100*probability[i][0],2))
        df2=pd.DataFrame({'Sentiment':sentiment,'Confidence':confidence})
        df1['sentiment']=df2['Sentiment']
        df1['Confidence']=df2['Confidence']
        df1.to_csv('./data.csv', index=False)
        return 1
    except Exception as e:
        print(f"An Error occurred at parsing data of csv. : {e}")
        return 0

    
def crawl(link):
    process = CrawlerProcess(get_project_settings())
    process.crawl(AmspySpider, slink=link)
    process.start()
    process.join()


def check_limit():
    curr_date = datetime.now().date()
    global req_count, prev_req_day
    if curr_date != prev_req_day:
        req_count = 0
        prev_req_day = curr_date
    print(req_count)
    if req_count >= 3:
        return True
    else:
        req_count += 1
        return False
    


app = Flask(__name__)

@app.route('/')
def home():
    init()
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
                #empty the data.csv
                df=pd.DataFrame()
                df.to_csv('./data.csv', index=False)
                crawl_process = Process(target=crawl, args=(link,))
                crawl_process.start()
                crawl_process.join() 
                if calc():
                    return render_template('index.html', page='download')
                else:
                    return render_template('index.html', page='error')
            else:
                return render_template('index.html', page='wrong_link')
        except Exception as e:
            print(f"Error at result route. : {e}")
            return render_template('limit.html')
    else:
        return redirect('/')

@app.route('/download_data', methods=['POST','GET'])
def download_data():
    file_path = './data.csv'  
    return send_file(file_path, as_attachment=True)

# not fot production
# if __name__ == '__main__':
#       app.run(debug=True)
#     app.run(debug=False, host='0.0.0.0')