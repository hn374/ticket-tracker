from selenium import webdriver
from selenium.webdriver.support.select import Select
from smsAPI import SmsAPI
import time
import re
import os
from datetime import date

## Store the parking website url
phillyParkingUrl = "https://onlineserviceshub.com/ParkingPortal/Philadelphia"

# Store your license plate
hondaCivicLicensePlate = os.environ.get("hoangLicensePlate")

# Access the driver
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("chromeDriverPath"), chrome_options=chrome_options)

# Access the parking website
driver.get(phillyParkingUrl)

# Pause to load
time.sleep(1)

# Select the search dropdown and select the license plate option
searchDropdown = Select(driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div/div[2]/div[1]/select"))
searchDropdown.select_by_value("plate")

# Select the license plate input and enter the license plate
licensePlateInput = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div/div[2]/div[2]/div[1]/input")
licensePlateInput.send_keys(hondaCivicLicensePlate)

# Select the state dropdown and enter the state
stateDropdown = Select(driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div/div[2]/div[2]/div[3]/select"))
stateDropdown.select_by_value("PA")

# Pause to load, wait for all values to be entered
time.sleep(1)

# Click on the search button after all the values have been entered
searchButton = driver.find_element_by_xpath("/html/body/div[2]/div[2]/form/div/div[3]/button")
searchButton.click()

# Wait for the search
time.sleep(1)

# Grab the page source and use a regular expression to search the site and see if a ticket was given
pageSource = driver.page_source
ticketTextFound = re.search(r"A payment has already been entered for this ticket.", pageSource)
searchTextFound = re.search(r"Search Results", pageSource)

# Create smsHelper object to send texts
smsHelper = SmsAPI(os.environ.get("twilioAccountSID"), os.environ.get("twilioAuthenticationToken"))

# Define the send and receive numbers
sendToNumber = os.environ.get("hoangPhoneNumber")
sendFromNumber = os.environ.get("twilioSendFromNumber")

today = date.today().strftime("%B %d, %Y")
# If text is not found, probably have a parking ticket (or they changed the text for some reason), also check for text if parking ticket was found
if not ticketTextFound and searchTextFound:
    ticketAlert = "Looks like you got another frickin parking ticket. Check the website. Date: " + today
    print(ticketAlert)
    smsHelper.sendText(sendToNumber, sendFromNumber, )
else:
    noTicketAlert = "No ticket as of: " + today
    print(noTicketAlert)
    smsHelper.sendText(sendToNumber, sendFromNumber, noTicketAlert)