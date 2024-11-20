import requests
from bs4 import BeautifulSoup
from latest_user_agents import get_random_user_agent
import pandas as pd

class AmazonScraper:
    def __init__(self, search_url):
        self.search_url = search_url
        self.headers = {
            'User-Agent': get_random_user_agent() 
        }

    def fetch_reviews(self):
        try:
            response = requests.get(self.search_url, headers=self.headers)
            if response.status_code == 200:
                print("Data fetched Successfull.")
                return response.text
            else:
                print(f"Failed to fetch page. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Request error: {e}")
            return False

    def parse_reviews(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        data = soup.select('div.a-row.a-spacing-small.review-data > span > div > div.a-expander-content.reviewText.review-text-content.a-expander-partial-collapse-content > span')
        reviews = []
        for feed in data:
            review = feed.get_text(strip=True)
            if review and review not in ('', 'NaN', None):
                reviews.append(review)
        print("Data Parsed Successfull.")
        # cant go on next page because of auth
        # link = soup.select('#reviews-medley-footer > div.a-row.a-spacing-medium > a')
        return reviews

    def save_to_csv(self, reviews):
        filename = 'data.csv'
        try:
            df = pd.DataFrame(reviews, columns=['Review'])
            df.to_csv(filename, index=False)
            print("Data saved to CSV successfully.")
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False


    def run(self):
        html_content = self.fetch_reviews()
        if html_content:
            reviews = self.parse_reviews(html_content)
            if reviews:
                return self.save_to_csv(reviews)
            else:
                print("No reviews get.")
                return False
        else:
            return False