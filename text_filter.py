import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopw = stopwords.words('english')
stopw.extend(list(string.ascii_lowercase))
stopw.extend(['0','1','2','3','4','5','6','7','8','9'])
punctuation_ = string.punctuation + '1234567890Â©á»áº¯ÄÃ' + '¢`~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿×÷¢£¤¥¦§©´µ¶·¸¹º€£¥₹₽₿₣₱₩₨₫₮₭₣₢₥₦₠₡₧₤₮₯₰₲₱₴₵₸₹₺₻₼₽₿'

def my_review_filter(review):
    list=[ch for ch in review if ch not in punctuation_]
    review = ''.join(list)
    list = [word for word in review.split() if word.lower() not in stopw]
    return list