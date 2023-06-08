from bs4 import BeautifulSoup      # 크롤링 사이트의 값을 가져오는 함수
import requests

save1 = []   # 관련 값 다 저장하기

code = '530053'

url = f"https://finance.naver.com/item/frgn.naver?code={code}"
req = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
soup = BeautifulSoup(req.text, "lxml")  # html에 대하여 접근할 수 있도록

value_a = soup.find_all("span", {"class": "tah p11"})

for title in value_a:
    save1.append(title.get_text())


print(save1)

a9 = save1[0]  # 풋 값
c9 = save1[2]  # 풋 증가량

print(a9)