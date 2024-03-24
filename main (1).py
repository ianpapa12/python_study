

import requests
from bs4 import BeautifulSoup

all_jobs = []

def scrape_page(url):
  print(f"Scraping {url}......")
  response = requests.get(url)

  soup = BeautifulSoup(response.content, "html.parser")
  #BeautifulSoup에게 response.content로 파일을 넘겨주고 이 파일이 html파일이라는 것을 "html.parser"로 알려준다
  #BeautifulSoup은 이러한 복잡한 html파일의 내부를 탐색하도록 도와준다

  jobs = soup.find("section", class_="jobs").find_all("li")[1:-1]
  #job listing(내가 스크립 할 부분)되어 있는 section의 id명 category-2 부분을 가져오기
  #class 명도 가져올 수 있다 다만 유의할 점은 "class_"로 명명하고 가져오기 
  #class jobs에서 모든 li(job listing 되어 있는 리스트)를 가져온다.즉 section의 내부를 탐색한다.
  #[1:-1] 리스트의 두번째(첫번째는 0)부터 마지지막 전까지 불러오기 (즉, 첫번째와 마지막은 제외)

  for job in jobs:
    title = job.find("span", class_="title").text
    company, position, region = job.find_all("span", class_="company")
    url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
    job_data = {
      "title": title,
      "company": company.text,
      "position": position.text,
      "region": region.text,
      "url": f"https://weworkremotely.com{url}",
    }
    all_jobs.append(job_data)
#scrape_page는 페이지를 스크래핑해서 일자리들을 찾고, all_jobs에 일자리들을 추가할 것이다.

def get_pages(url):
  response = requests.get(url)
  #첫번째 페이지 만을 요청

  soup = BeautifulSoup(response.content, "html.parser")
  #첫번째 페이지에 있는 html문서 가져오기 

  return len(soup.find("div", class_="pagination").find_all("span", class_="page"))
  #class_ = pagination에 몇개의 버튼이 있는지 알아 내기 
  #pagination에 있는 모든 버튼을 가지고 for loop구문으로 버튼 갯수에 맞게 실행시켜준다.

#get_pages: 페이지수를 가져오는 부분을 함수로 만들었다,.
  
total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")


for x in range(total_pages):
  url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
  scrape_page(url)

print(len(all_jobs))
#모든 일자리 갯수 알아내기 

