from playwright.sync_api import sync_playwright
#sync는 playwright를 작동시키는 방법 중 하나이다.
import time
#time module은 대기시간을 생성해준다
from bs4 import BeautifulSoup 
import csv
#쉼표로 구분된 csv파일을 작성하는데 도움을 주는 module이다.

p = sync_playwright().start()
#sync_playwright함수는 클래스를 인스턴스화, 초기화 한다. 즉 playwright를 초기화 하는 코드 

browser = p.chromium.launch(headless=False)
#browser만들기 // 뒤에 launch라고 적으면 브라우저를 초기화 시켜준다
#headless=True 브라우저가 존재하지만 눈에 보이지 않는 상태 // False로 바꾸면 브라우저를 보여줌
#headless=True는 keyword argument이다.

page = browser.new_page()
#browser에서 새로운 탭 만들기 // 이건 우리가 브라우저에서 실제로 새로운 탭을 만드는 것과 같다. 

page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")
#goto를 사용해서 url로 이동시킬 수 있다.


"""
아래는 공부 목적


time.sleep(5)
#몇초 정도 대기시간을 둘 것인지 설정 // playwright 클릭 속도가 굉장히 빨라 실행이 잘 되는지 확인이 어려워 이를 사용한다.

page.click("button.Aside_searchButton__Xhqq3")
#CSS selector기능을 사용하여 버튼 가져오기 

time.sleep(5)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
#검색창 부분의 placeholder를 가져오고 검색창에 flutter라 검색
#placeholder를 가져오는 이유는 추후 웹사이트가 개발자에 의해 변경될 때 class명이 변경될 소지가 있으나 검색창의 placeholder는 변경될 소지가 적음 

time.sleep(5)

page.keyboard.down("Enter")
#Enter키 누르기 

time.sleep(5)

page.click("a#search_tab_position")
#페이지의 포지션 부분 클릭하기 

"""

for x in range(5):
    time.sleep(5)
    page.keyboard.down("End")    

content = page.content()
#페이지 소스 갖고오기 

p.stop()

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__FqChn")

jobs_db = []

for job in jobs:
#여기서 job의 의미는 각각의 div를 의미한다 
    link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title__ddkwM").text
    company_name = job.find("span", class_="JobCard_companyContent__zUT91").text
    reward = job.find("span", class_="JobCard_reward__sdyHn").text
    job = {
        "title": title,
        "company_name": company_name,
        "reward": reward,
        "link": link
    }
    jobs_db.append(job)

file = open("jobs.csv", "w")
#open은 파이썬에서 파일을 열어주는 함수이다. 파일이 없다면 만들어준다. 디폴트는 읽기전용으로 되어있으므로 수정을 하기 위해서는 코드를 수정해줘야 한다. 
# r: 읽기전용모드 // w: 수정가능 
writer = csv.writer(file)
#이걸로 csv파일에 행을 추가할 수 있게 됨 
writer.writerow([
    "Title", "Company", "Reward", "Link"
])
# writerow를 활용해 csv형태로 첫번째 행을 만들었다 다음으로 jobs라는 데이터베이스 안에 있는 각각의 job dictionary를 살펴보자 

for job in jobs_db:
    writer.writerow(job.values())
# dictionary에서 값(value)만 가져와서 리스트를 만들때는? dictionary method의 values를 활용한다

"""
def plus(a, b):
    return a+b

plus(1,2)
#1,2는 positional argument이다. 인자(argument)값의 위치가 영향을 가지기 때문에 positional이라고 부른다.
#하지만 positional은 인자값이 많아지면 오류가 발생할 확률이 높다 
#2개가 초과되는 argument는 positional로 사용하지 않는다. 대신 이름을 사용해서 어떤 인자값이 어떤 것인지 하나씩 구체화 할 수 있다.
plus(b=1, a=1) #이를 keyword argument라 한다.
#처음에 keyword argument를 호출했다면, 뒤에 가서 postional argument를 사용할 수 없다. 다만 그 반대의 경우는 가능하다.
"""