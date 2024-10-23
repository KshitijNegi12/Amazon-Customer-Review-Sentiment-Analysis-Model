# Amazon Review Sentiment Analysis

## Introduction
This web application allows users to analyze sentiments of Amazon reviews using a trained Naive Bayes model. By crawling product latest same page reviews, it determines whether the sentiment is positive or negative and provides confidence scores for each prediction.

You can check it [here](https://kshitij-amazon-customer-review.onrender.com).

## Tech Used
- **FrameWork**: Flask
- **Web Scraping**: Scrapy
- **Data Processing**: Pandas
- **Machine Learning**: Joblib, Naive Bayes Algorithm
- **Frontend**: HTML, CSS, JavaScript

## Features
- **Sentiment Analysis**: Classifies reviews as positive or negative with confidence scores.
- **Web Crawling**: Gathers reviews from specified Amazon product links.
- **Data Download**: Users can download the analyzed reviews in CSV format.
- **Request Limitation**: Restricts the number of requests to prevent abuse.
