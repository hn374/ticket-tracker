from selenium import webdriver
from selenium.webdriver.support.select import Select
from smsAPI import SmsAPI
import time
import re
import config

## Store the parking website url
phillyParkingUrl = "https://onlineserviceshub.com/ParkingPortal/Philadelphia"

# Store your license plate
hondaCivicLicensePlate = config.hoangLicensePlate

# Access the driver
driver = webdriver.Chrome(executable_path=config.chromeDriverPath)

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
smsHelper = SmsAPI(config.twilioAccountSID, config.twilioAuthenticationToken)

# Define the send and receive numbers
sendToNumber = config.hoangPhoneNumber
sendFromNumber = config.twilioSendFromNumber

# If text is not found, probably have a parking ticket (or they changed the text for some reason), also check for text if parking ticket was found
if not ticketTextFound and searchTextFound:
    smsHelper.sendText(sendToNumber, sendFromNumber, "Looks like you got another frickin parking ticket. Check the website.")