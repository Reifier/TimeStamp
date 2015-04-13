#!/usr/bin/env python2


"""
This is a simple script that automates filling in of Kimai reports for me.

To use the script attach it to the cron job on your device.

Requirements:
Firefox,Python 2, Selenium WebDriver.
"""
from selenium import webdriver


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import sys
import urllib2
import time
import config


PROMPT = '>'
#Description is set to this string by default
DESCRIPTION = "General Administrative Tasks"
INPUT = ''
#Default times to use
TIME_IN = '10:00:00'
TIME_OUT = '13:30:00'

display = Display(visible=0, size=(800, 600))


def internet_on():

    try:
        urllib2.urlopen('http://74.125.228.100', timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

while internet_on() != True:
    print "No internet connection"
    time.sleep(600)


display.start()
fp = webdriver.FirefoxProfile()
fp.add_extension(extension=config.firefoxExtensions['firebug'])
fp.add_extension(extension=config.firefoxExtensions['selenium'])

driver = webdriver.Firefox(fp)

driver.get("http://spirit0.linuxcertified.com/kimai/")

print driver.title
try:
    inputElement = driver.find_element_by_name("name")
except:
    print "Can't access the website, check if the network connection is present."
    sys.exit(1)

# Prompt me for the tasks that I've been doing. If no input just defaults to DESCRIPTION variable
INPUT = raw_input(PROMPT)

if INPUT:
    DESCRIPTION = INPUT

#Proceed with website clicking after giving your own input
inputElement.send_keys(config.userCredentials['user'])
inputElement = driver.find_element_by_name("password")
inputElement.send_keys(config.userCredentials['password'])
inputElement.submit()

try:
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.left"))
    )
except:
    print "The exception was raised"
else:
    print "Went Through"


addEntry = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/div/a').send_keys(Keys.RETURN)

try:
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "edit_in_time"))
    )
except:
    print "The exception was raised"
else:
    print "Went Through"

# Click on the time, clear whatever value is in there and input 10:00
timeInEntry = driver.find_element(By.ID, 'edit_in_time')
timeInEntry.clear()
timeInEntry.send_keys(TIME_IN)

# Click on the time, clear whatever value is in there and input 13:30
timeOutEntry = driver.find_element(By.XPATH, '//*[@id="edit_out_time"]')
timeOutEntry.click()
timeOutEntry.clear()
timeOutEntry.send_keys(TIME_OUT)

# Go to Advanced tab and click on comment field
driver.find_element(By.XPATH, '/html/body/div[6]/div/div[3]/ul/li[2]/a/span[2]').click()

comment = driver.find_element(By.ID, 'comment')
comment.click()
comment.send_keys(DESCRIPTION)


# Click ok
okButton = driver.find_element(By.XPATH, '/html/body/div[6]/div/form/div[2]/input[2]')
okButton.click()

display.stop()
driver.quit()


