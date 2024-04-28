import joblib
import pandas as pd
from flask import Flask, render_template, request, send_file
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from amazon.amazon.spiders.amspy import AmspySpider
model = None
vectorizer = None

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
        print(f"AN ERROR OCCURED: {e}")
        return 0

    
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
    if(model==None):init()
    if request.method == 'POST':
        input = request.form['inputType']
        if input == 'text':
            txt = request.form['text']
            if len(txt)>0:
                X = vectorizer.transform([txt])
                predict_val = model.predict(X)
                prob = model.predict_proba(X)
                if predict_val == 1:
                    predict_res = 'POSITIVE'
                    confidence = prob[0][1]
                    return render_template('index.html', page='text', prediction_text = predict_res, confidence = round(100*confidence,2), bg='green')
                else:
                    predict_res = 'NEGATIVE'
                    confidence = prob[0][0]
                    return render_template('index.html', page='text', prediction_text = predict_res, confidence = round(100*confidence,2), bg='red')
            else:
                return render_template('index.html', page='empty')
        else:
            link = request.form['link']
            if len(link) > 0 and link.startswith('https://www.amazon.in/'):
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

@app.route('/download_data', methods=['POST','GET'])
def download_data():
    file_path = './data.csv'  
    return send_file(file_path, as_attachment=True)

# not fot production
# if __name__ == '__main__':
#       app.run(debug=True)
#     app.run(debug=False, host='0.0.0.0')