# Amazon Review Sentiment Analysis

## Introduction
This web application allows users to analyze sentiments of amazon.in reviews using a Naive Bayes model trained on 12K datapoints. By crawling amazon.in product same page latest reviews, it determines whether the sentiment is positive, negative or neutral and provides confidence scores for each prediction.

## Tech Used
- **FrameWork**: Flask
- **Web Scraping**: BeautifulSoup
- **Data Processing**: Pandas
- **Machine Learning**: Joblib, Naive Bayes Algorithm
- **Frontend**: HTML, CSS, JavaScript

## Features
- **Sentiment Analysis**: Classifies reviews as positive, negative or neutral with confidence scores.
- **Web Crawling**: Gathers reviews from specified Amazon product links.
- **Data Download**: Users can download the analyzed reviews in CSV format.
- **Request Limitation**: Restricts the number of requests to prevent abuse.
