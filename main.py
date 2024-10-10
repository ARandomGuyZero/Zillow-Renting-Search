"""
Zillow Renting Search

Author: Alan
Date: October 10th

Searches renting places in areas and submits them in a Google Form
"""

from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
import lxml

URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "Your form from google"

def get_zillow_data():
    """
    Get the data from the zillow clone page
    Specifically the addresses, the prices and the links
    :return: Return a list of strings with the addresses, the prices and the links
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    # Gets the page HTML
    webpage = get(url=URL, headers=headers).text

    # New BeautifulSoup object
    soup = BeautifulSoup(webpage, "lxml")

    # Gets a list with all the addresses
    address_search = soup.find(name="address")
    address_list = [address.text.strip() for address in address_search]

    # Gets a list with all the prices
    prices_search = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
    price_list = [price.text.replace("+","").replace("/mo", "").split(" ")[0] for price in prices_search]

    # Gets a list with all the links
    links_search = soup.find_all(name="a", class_="property-card-link")
    link_list = [link.get("href") for link in links_search]

    # Returns said lists
    return address_list, price_list, link_list

def answer_forms(address_list, price_list, link_list):
    """
    Selenium clicks on every form input and fills it with the zillow data
    :param address_list: List of addresses
    :param price_list: List of prices
    :param link_list: List of links
    :return:
    """

    # Keeps the page open
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    # New webdriver to do the tinkering
    driver = webdriver.Chrome(options=options)
    driver.get(FORM_URL)

    # For each iteration in a range that it's as long as any of the lists
    for i in range(len(address_list)):

        # Fills the question with an address
        address_question = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address_question.send_keys(address_list[i])

        # Fills the price with an address
        price_question = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price_question.send_keys(price_list[i])

        # Fills the link with an address
        link_question = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_question.send_keys(link_list[i])

        # CLicks on the submit form
        submit_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        submit_form.click()

        # CLicks on the new answer form to send it again
        new_answer = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
        new_answer.click()

    # Closes the browser
    driver.close()
    driver.quit()

# Gets the lists of data from zillow
addresses, prices, links = get_zillow_data()

# Gets the form of Google and fills it with the data
answer_forms(addresses, prices, links)
