import requests
from bs4 import BeautifulSoup


def get_pages(url):
  response = requests.get(
      url,
      headers={
          "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
      })
  soup = BeautifulSoup(response.content, "html.parser")
  page_num = soup.find_all("a",class_="pagination-link")[-1].text

  return page_num


def scraper(url, all_jobs):
  response = requests.get(
      url,
      headers={
          "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
      })

  soup = BeautifulSoup(response.content, "html.parser")

  jobs = soup.find("div", class_="column opportunity-list").find_all("a", class_="tile is-child white-box opportunity")


  for job in jobs:

    link = ""
    title = ""
    activities = ""
    duration = ""



    link = job["href"].strip()


    if (job.find("h3", class_="title")):
      title = job.find("h3", class_="title").text.strip()


    if (job.find("div", class_="activities")):
      activities = job.find("div", class_="activities").text.strip()


    if (job.find("div", class_="duration")):
      duration = job.find("div", class_="duration").text.strip()


    if(link !="" and title !="" and activities !=""):
      job = {
          "link": link,
          "title": title,
          "activities": activities,
          "duration": duration
      }

      all_jobs.append(job)



def searching(page_number):
  all_jobs = []
  
  scraper(f"https://www.volunteerconnector.org/page-{page_number}/?so=Proximity&md=50&pc=V6P", all_jobs)

  return all_jobs


page_numbers = get_pages(f"https://www.volunteerconnector.org/")

page_numbers = int(page_numbers)
total_num = range(page_numbers)

for page_number in total_num:
  searching(page_number+1)


