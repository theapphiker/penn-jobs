"""penn_jobs.py, this program extracts Pennylvania government jobs of interest and sends an email to my Gmail account with the results."""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import os
from dotenv import load_dotenv
import smtplib
from datetime import date
import concurrent.futures

def main():
    """
    Scrapes jobs of interest from Pennylvania government job search website and then emails the jobs to my Gmail account.
    
    """
    # set up Firefox
    options = Options()
    firefox_binary_path = "/usr/bin/firefox-esr"
    options.binary_location = firefox_binary_path
    options.add_argument(
        "--headless"
    )  # prevents Firefox browser from obviously opening
    options.add_argument("--disable-dev-shm-usage")
    # Recommended for stability in Docker
    options.add_argument("--no-sandbox")

    # add more searches to this list as needed
    job_links = [
    "https://www.governmentjobs.com/careers/pabureau?keywords=intelligence",
    "https://www.governmentjobs.com/careers/pabureau?keywords=investigator",
    "https://www.governmentjobs.com/careers/pabureau?keywords=python",
    "https://www.governmentjobs.com/careers/pabureau?keywords=sql",
    "https://www.governmentjobs.com/careers/pabureau?keywords=analyst"
]
    results_dict = {}

    print("Getting Penn jobs...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_html, url, options): url for url in job_links}
        for future in concurrent.futures.as_completed(future_to_url):
            results_dict[future_to_url[future].replace("%20","_").split("=")[1]] = future.result()

    # adding text for email
    print("Writing email with jobs...")
    results_text = write_jobs_text(results_dict)

    # adding job search information and current date
    today = date.today()
    formatted_date = today.strftime("%m/%d/%Y")
    results_text = "Penn Government Jobs for " + formatted_date + "\n\n" + results_text

    # change email in .env file as needed
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL_ADDRESS')
    receiver_email = os.getenv('RECEIVER_EMAIL_ADDRESS')
    pw = os.getenv('APP_PASSWORD')
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, pw)
    s.sendmail(sender_email, receiver_email, str(results_text).encode('utf-8'))
    s.quit()
    print("Email sent!")

def get_html(job_search, options):
    """
    Fetches the HTML content of a provided Pennylvania government job search URL using a headless Firefox browser.

    Args:
    job_search (str): The URL of the Pennylvania government job search.

    Returns:
    str: The inner HTML content of the retrieved webpage.
    """
    browser = webdriver.Firefox(options=options)
    browser.get(job_search)
    sleep(5) # sleep for 5 seconds to allow time for the JavaScript to load
    inner_html = browser.execute_script("return document.body.innerHTML")
    browser.quit()
    jobs = parse_html(inner_html)
    return jobs

def parse_html(html):
    """
    Parses the HTML content of a Pennylvania government job search page and extracts relevant job details.

    Args:
    html (str): The HTML content of the job search page.

    Returns:
    list: A list of lists, where each inner list contains details for a single job posting
    (job title, job URL, date of job posting).
    """
    results = []
    soup = BeautifulSoup(html, "html5lib")
    if soup.find('div', class_="search-results-grid-container") is None:
        results.append([])
    else:
        for e in soup.find('div', class_="search-results-grid-container").select('tr'):
            temp_results = []
            if "data-job-id" in str(e):
                temp_results.append((e.select("a")[0].getText()))
                temp_results.append(
                    "https://www.governmentjobs.com" + e.find("a").get("href")
                )
            if "job-table-posted" in str(e):
                if e.find("td",class_="job-table-posted hidden-sm hidden-xs"):
                    temp_results.append("Posted: " + e.find("td",class_="job-table-posted hidden-sm hidden-xs").get_text())
                if e.find("td",class_="job-table-closing"):
                    temp_results.append("Closing: " + e.find("td",class_="job-table-closing").get_text())
            results.append(temp_results)
    return results


def write_jobs_text(results_dict):
    """
    Formats a dictionary containing extracted job details into a text string suitable for email notification.

    Args:
    results_dict (dict): A dictionary containing job search terms as keys and lists of job details as values.

    Returns:
    str: A formatted text string containing job titles, URLs, and dates of job posting for relevant jobs.
    """
    results_text = """"""
    for k in results_dict.keys():
        results_text += k.upper() + " JOBS"
        results_text += "\n"
        if results_dict[k] == [[]]:
            results_text += "No jobs found."
            results_text += "\n"
            results_text += "\n"
        else:
            for v in results_dict[k]:
                if v != []:
                    for value in v:
                        results_text += value
                        results_text += "\n"
                    results_text += "\n"
    results_text += "\n"
    return results_text

if __name__ == "__main__":
    main()