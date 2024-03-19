import joblib
from text_filter import my_review_filter

model = joblib.load(r'Host/Model/trained_model.pkl')
vectorizer = joblib.load(r'Host/Model/trained_vectorizer.pkl')

l=['Hello my name is hero. XD', 'for real?', 'holy moly', '#you are fool dumb wit', 'nice', 'good game','stupid']
X_input = vectorizer.transform(l)
prediction = model.predict(X_input)
confidence_scores = model.predict_proba(X_input)

for i in range(len(l)):
    print(f"The predicted value for {l[i]} is: ", end="")
    n = prediction[i]
    if n == 1:
        print(f'POSITIVE (confidence: {100*confidence_scores[i][1]:.2f})')
    else:
        print(f'NEGATIVE (confidence: {100*confidence_scores[i][0]:.2f})')