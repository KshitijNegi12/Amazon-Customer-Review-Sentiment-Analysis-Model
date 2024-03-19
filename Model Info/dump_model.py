import pandas as pd
import numpy as np
import joblib
from text_filter import my_review_filter
from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

df1 = pd.read_csv(r'Dataset\neg_label.csv',encoding='latin-1')
df2 = pd.read_csv(r'Dataset\pos_label.csv',encoding='latin-1')
df = pd.concat([df1,df2], ignore_index=True)

vector =cv(analyzer=my_review_filter, dtype=np.uint8)
X = vector.fit_transform(df['Comment'])
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=5)

NB_classifier = MultinomialNB()
NB_classifier.fit(X_train, y_train)

joblib.dump(NB_classifier, 'trained_model.pkl')
joblib.dump(vector, 'trained_vectorizer.pkl')
