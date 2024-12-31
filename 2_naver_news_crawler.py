import requests
import time 
import random
import pandas as pd

from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

prompts = """
추출하려고 하는 뉴스 카테고리 시리얼넘버를 아래를 확인하시고 입력해주세요.

정치: 100
사회: 102
생활/문화: 103 
세계: 104
IT/과학: 105
"""

print()
serial_number = input("뉴스 시리얼넘버를 입력하세요: ")

url = f"https://news.naver.com/section/{serial_number}"
results = {}

# HTTP 요청을 보냅니다
response = requests.get(url, headers=headers)

# 응답으로부터 HTML을 파싱합니다
soup = BeautifulSoup(response.text, 'html.parser')

# 'sa_item_flex' 클래스를 가진 모든 <div> 태그를 찾습니다
headline_elements = soup.find_all('div', class_='sa_item_flex')

counter = 1
for element in headline_elements:
    news_data = []  # 각 기사의 데이터를 저장할 리스트
    
    # 기사 링크 추출
    a_tag = element.find('a', attrs={'data-imp-url': True})
    if a_tag:
        news_data.append(a_tag['data-imp-url'])
    
    # 기사 제목 추출
    img_tag = element.find('img', attrs={'alt': True})
    if img_tag:
        news_data.append(img_tag['alt'])
        news_data.append(img_tag['data-src'])  # 썸네일 이미지 URL 추출
    
    # 발행언론 추출
    publisher_tag = element.find('div', class_='sa_text_press')
    if publisher_tag:
        news_data.append(publisher_tag.text.strip())
    
    results[counter] = news_data  # 리스트를 results에 추가
    
    counter += 1

print(results)


for key, value in results.items():
    news_url = value[0]
    response = requests.get(news_url, headers=headers)
    time.sleep(random.uniform(0.3, 0.8))

    # 응답으로부터 HTML을 파싱합니다
    soup = BeautifulSoup(response.text, 'html.parser')

    # 'sa_item_flex' 클래스를 가진 모든 <div> 태그를 찾습니다
    contents = soup.find_all('article', id='dic_area')[0].text.replace('\n','').replace('\t','')

    results[key].append(contents)


print(results)

"""
1. 기사링크URL
2. 기사제목
3. 기사썸네일URL
4. 기사발행사
5. 기사내용 
"""
df = pd.DataFrame.from_dict(results, orient='index', columns=['Link URL', 'Title', 'Thumbnail URL', 'Publisher', 'Content'])

# DataFrame을 CSV 파일로 저장
df.to_csv('news_data.csv', index=False)

print("CSV 파일이 저장되었습니다.")
