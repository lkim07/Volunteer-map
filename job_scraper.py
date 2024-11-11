from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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

def get_location(url):
  response = requests.get(
      url,
      headers={
          "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
      })
  soup = BeautifulSoup(response.content, "html.parser")
  
  location=""

  if(soup.find("div", class_= "location")):
    location = soup.find("div", class_= "location").text.strip()[0:-5].strip()


  return location

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
    location = ""


    link = job["href"].strip()


    if (job.find("h3", class_="title")):
      title = job.find("h3", class_="title").text.strip()


    if (job.find("div", class_="activities")):
      activities = job.find("div", class_="activities").text.strip()


    if (job.find("div", class_="duration")):
      duration = job.find("div", class_="duration").text.strip()

    link = f"https://www.volunteerconnector.org{link}"
    location = get_location(link)


    if(link !="" and title !="" and activities !="" and location != ""):
      job = {
          "link": link,
          "title": title,
          "activities": activities,
          "duration": duration,
          "location": location 
      }


      all_jobs.append(job)



def searching(page_number):
  all_jobs = []
  scraper(f"https://www.volunteerconnector.org/page-{page_number}/?so=Proximity&md=50&pc=V6P", all_jobs)

  return all_jobs


# page_numbers = get_pages(f"https://www.volunteerconnector.org/")
# page_numbers = int(page_numbers)
# total_num = range(page_numbers)

db={
  "North Vancouver": [],
  "West Vancouver": [],
  "Vancouver": [],
  "Richmond": [],
  "Burnaby": []
}

# for page_number in total_num:
#   jobs = searching(page_number+1)
#   for job in jobs:
#     location = job["location"].lower()
#     if ("north vancouver" in location):
#         db["North Vancouver"].append(job)
#     elif ("west vancouver" in location):
#         db["West Vancouver"].append(job)
#     elif ("richmond" in location):
#         db["Richmond"].append(job)
#     elif ("burnaby" in location):
#         db["Burnaby"].append(job)
#     elif("vancouver" in location):
#         db["Vancouver"].append(job)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    page_numbers = get_pages("https://www.volunteerconnector.org/")
    page_numbers = int(page_numbers)
    total_num = range(page_numbers)

    for page_number in total_num:
        jobs = searching(page_number + 1)
        for job in jobs:
            location = job["location"].lower()
            if "north vancouver" in location:
                db["North Vancouver"].append(job)
            elif "west vancouver" in location:
                db["West Vancouver"].append(job)
            elif "richmond" in location:
                db["Richmond"].append(job)
            elif "burnaby" in location:
                db["Burnaby"].append(job)
            elif "vancouver" in location:
                db["Vancouver"].append(job)

    return jsonify(db)

if __name__ == '__main__':
    app.run(debug=True, port=5000)