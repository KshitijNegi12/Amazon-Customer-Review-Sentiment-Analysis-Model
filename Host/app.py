import joblib
import pandas as pd
from flask import Flask, render_template, request, send_file
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from amazon.amazon.spiders.amspy import AmspySpider
from text_filter import my_review_filter

model = None
vectorizer = None

def init():
    global model,vectorizer
    model = joblib.load(r'Host/Model/trained_model.pkl')
    vectorizer = joblib.load(r'Host/Model/trained_vectorizer.pkl')


def calc():
    try:
        df1 = pd.read_csv('data.csv')
        X = vectorizer.transform(df1['text'])
        sentiment = model.predict(X)
        prob = model.predict_proba(X)
        sentiment=sentiment.flatten().tolist()
        conf=[]
        for i in range(len(sentiment)):
            if sentiment[i] == 1:
                sentiment[i] = 'Positive'
                conf.append(round(100*prob[i][1],2))
            else:
                sentiment[i] = 'Negative'
                conf.append(round(100*prob[i][0],2))
        df2=pd.DataFrame({'Sentiment':sentiment,'Confidence':conf})
        df1['sentiment']=df2['Sentiment']
        df1['Confidence']=df2['Confidence']
        df1.to_csv('data.csv')
    except Exception as e:
        print(f"AN ERROR OCCURED: {e}")

    
def crawl(link):
    process = CrawlerProcess(get_project_settings())
    process.crawl(AmspySpider, slink=link)
    process.start()
    process.join()


app = Flask(__name__)

@app.route('/')
def home():
    init()
    return render_template('index.html')

@app.route('/result', methods=['POST','GET'])
def result():
    res = ""
    confidence = -1
    if request.method == 'POST':
        input = request.form['inputType']
        if input == 'text':
            txt = request.form['text']
            if len(txt)>0:
                X = vectorizer.transform([txt])
                n = model.predict(X)
                prob = model.predict_proba(X)
                if n == 1:
                    res = 'POSITIVE'
                    confidence = prob[0][1]
                else:
                    res = 'NEGATIVE'
                    confidence = prob[0][0]
                return render_template('index.html', page=1, prediction_text = res, confidence = round(100*confidence,2))
            else:
                return render_template('index.html', page=-1)
        else:
            link = request.form['link']
            if len(link) > 0 and 'https://www.amazon.in/' in link:
                crawl_process = Process(target=crawl, args=(link,))
                crawl_process.start()
                crawl_process.join() 

                calc()
                return render_template('index.html', page=0)
            else:
                return render_template('index.html', page=-1)

@app.route('/download_data', methods=['POST','GET'])
def download_data():
    file_path = '../data.csv'  
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
