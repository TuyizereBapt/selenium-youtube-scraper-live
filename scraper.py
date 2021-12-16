from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# import pandas as pd
import smtplib
import os
import json

YOUTUBE_TRENDING_URL = 'https://www.youtube.com/feed/trending'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_videos(driver):
    # Getthing the video divs
    VIDEO_TAG = 'ytd-video-renderer'
    # Fetching the page
    driver.get(YOUTUBE_TRENDING_URL)
    videos = driver.find_elements(By.TAG_NAME, VIDEO_TAG)
    return videos


def parse_video(video):
    title_tag = video.find_element(By.ID, 'video-title')
    title = title_tag.text

    url = title_tag.get_attribute('href')

    thumbnail_url = video.find_element(By.TAG_NAME, 'img').get_attribute('src')

    channel_name = video.find_element(By.CLASS_NAME, 'ytd-channel-name').text

    description = video.find_element(By.ID, 'description-text').text

    return {
        'title': title,
        'url': url,
        'thumbnail_url': thumbnail_url,
        'channel': channel_name,
        'description': description
    }

def send_email(body):
  try:
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()

    sender_email = os.environ['GMAIL_PASSWORD']
    receiver_email = [sender_email]
    subject = 'YouTube top 10 trending videos'
    email_text = f"""
    From: {sender_email}
    To: {receiver_email}
    Subject: {subject}

    {body}
    """

    sender_password = os.environ['GMAIL_PASSWORD']
    server_ssl.login(sender_email, sender_password)
    server_ssl.sendmail(sender_email, receiver_email, email_text)
    server_ssl.close()

  except:
    print('Something went wrong...')




if __name__ == '__main__':
    # Creating driver
    driver = get_driver()

    videos = get_videos(driver)
    print(f'Found {len(videos)} videos')

    # Parsing top 10 videos
    videos_data = [parse_video(video) for video in videos[:10]]

    # Save the data to csv
    # videos_df = pd.DataFrame(videos_data)
    
    # videos_df.to_csv('trending.csv', index=None)

    body = json.dumps(videos_data, indent=2)

    # Sending an email with results
    send_email(body)
