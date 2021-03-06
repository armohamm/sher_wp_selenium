#! /usr/bin/env python3.6
# Script for codingbee python automation
# 2017 July 03;
# configure_widget.py is dependend on selenium
# pip3 install -U selenium
# headless starting of program with xvfb-run python3.6 configure-widget.py s sher password ruby python nav_menu-5 20

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import random
import time
import html
import os
import re
import sys
import codecs

# computer can be 'l' for local testing or any other value like 's' for digitalocean server

computer = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
menu_name = sys.argv[4]
menu_value = sys.argv[5]
dropdown_menu_html_id = sys.argv[6]
category_html_id = sys.argv[7]

now = str(datetime.datetime.now())[:16]

# do not forget to change dir_in values, also few lines bellow geckodriverexecutablePath
if computer == 'l':
    dir_in = "/data/upwork/Sher_Chowdhury/"
else:
    dir_in = "/root/"

log = codecs.open(dir_in + "configure-widget-log.txt", "a", "utf-8")

print('*' * 50)
print(computer)
log.write(now + ' ' + computer + os.linesep)
print(username)
log.write(now + ' ' + username + os.linesep)
print(password)
log.write(now + ' ' + password + os.linesep)
print(menu_name)
log.write(now + ' ' + menu_name + os.linesep)
print(menu_value)
log.write(now + ' ' + menu_value + os.linesep)
print(dropdown_menu_html_id)
log.write(now + ' ' + dropdown_menu_html_id + os.linesep)
print(category_html_id)
log.write(now + ' ' + category_html_id + os.linesep)
print('*' * 50)

timeout = 10
# using geckodriver
# set value to integer 1 (with 0 selenium will try to work with default firefox browser)
# newest geckodriver executable can be downloaded from https://github.com/mozilla/geckodriver/releases
# unpacked and placed in some directory, where in next line full absolute path to geckodriver executable will be set
if computer == 'l':
    geckodriverexecutablePath = "/data/Scrape/geckodriver"
else:
    geckodriverexecutablePath = "/usr/bin/geckodriver"
usegecko = True
time1 = time.time()
driver = None
wait = None

def open_tag_by_css(css_selector):
    '''function to click item based on css selector'''
    driver.find_element_by_css_selector(css_selector).click()

def open_tag_by_xpath(xpath):
    '''function to click item based on xpath'''
    driver.find_element_by_xpath(xpath).click()

def enter_in_tag_by_css(css_selector, text):
    '''function to enter text based on css selector'''
    driver.find_element_by_css_selector(css_selector).send_keys(text)

def enter_in_tag_by_xpath(xpath, text):
    '''function to enter text based on xpath'''
    driver.find_element_by_xpath(xpath).send_keys(text)

def save_response_to_file(text):
    '''temporary function to analyse html response'''
    with codecs.open(dir_in + "rawresponse.txt", "w", "utf-8") as fresp:
        fresp.write(html.unescape(text))

def waitForLoadbyCSS(CSS_SELECTOR):
    '''function to wait until web element is available via css check'''
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTOR)))

def waitForLoadbyXpath(xpath):
    '''function to wait until web element is available via xpath check'''
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except:
        return False

def openurl(url):
    '''function to open url using selenium'''
    try:
        driver.get(url)
        print('loading ' + url)
    except Exception as e:
        log.write(now + ' ' + str(e) + os.linesep)
        print(str(e))

def setbrowser():
    ''' function for preparing browser for automation '''
    print("Preparing browser")
    global driver
    global wait
    capabilities = DesiredCapabilities.FIREFOX
    capabilities['acceptInsecureCerts'] = True
    if usegecko:
        capabilities["marionette"] = True
    profile = webdriver.firefox.firefox_profile.FirefoxProfile()
    profile.default_preferences["webdriver_assume_untrusted_issuer"] = False
    profile.update_preferences()
    driver = webdriver.Firefox(firefox_profile=profile,
                               capabilities = capabilities,
                               executable_path = geckodriverexecutablePath)
    driver.implicitly_wait(timeout)
    wait = WebDriverWait(driver, timeout)

def scroll_down(sbypx):
    '''function for scrolling down by px'''
    driver.execute_script("window.scrollBy(0, %d);" % (sbypx))
    time.sleep(0.3)
    
def scroll_topbottom():
    '''function for scrolling top to bottom'''
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.3)

def is_element_present(xpath):
    '''checking is element present based on xpath'''
    try:
        driver.find_element_by_xpath(xpath)
        bprocess = True
    except:
        bprocess = False
    return bprocess

def login():
    '''function to log on page'''
    url = "http://codingbee.net/wp-login.php"
    openurl(url)
    time.sleep(1)
    xpath = "//input[@id='user_login']"
    waitForLoadbyXpath(xpath)
    el = driver.find_element_by_xpath(xpath)
    el.click()
    el.clear()
    el.send_keys(username)
    xpath = "//input[@id='user_pass']"
    el = driver.find_element_by_xpath(xpath)
    el.click()
    el.clear()
    el.send_keys(password)
    xpath = "//input[@id='wp-submit']"
    el = driver.find_element_by_xpath(xpath)
    el.click()
    time.sleep(3)
    # make sure that page is loaded
    xpath = "//a[contains(.,'Codingbee')]"
    waitForLoadbyXpath(xpath)
    if is_element_present(xpath):
        print('login successful')
        log.write(now + ' ' + 'login successful' + os.linesep)
    else:
        print('problems with login...')
        log.write(now + ' ' + 'problems with login...')
        sys.exit()


def setwidget():
    '''this is main function for setting widget'''
    url = "http://codingbee.net/wp-admin/widgets.php"
    openurl(url)
    time.sleep(2)
    scroll_topbottom()

    # Select Custom Menu: $menu_name
    xpath = "//h3[contains(.,'Custom Menu:') and contains(.,'%s')]" % menu_name
    el = driver.find_element_by_xpath(xpath)
    el.click()
    print(xpath + ' clicked')
    log.write(now + ' ' + xpath + ' clicked' + os.linesep)
    time.sleep(1)

    # choose $menu_value from first drop down menu
    xpath = "//select[contains(@id, 'widget-%s')]" % dropdown_menu_html_id
    value = menu_value
    el = Select(driver.find_element_by_xpath(xpath))
    el.select_by_visible_text(value)
    print(xpath + ' clicked')
    log.write(now + ' ' + xpath + ' clicked' + os.linesep)
    print(value + ' set')
    log.write(now + ' ' + value + ' set' + os.linesep)
    time.sleep(1)

    # Show on checked pages
    xpath = "//select[contains(@name,'extended_widget_opts-%s')]" % dropdown_menu_html_id
    value = "Show on checked pages"
    el = Select(driver.find_element_by_xpath(xpath))
    el.select_by_visible_text(value)
    print(xpath + ' clicked')
    log.write(now + ' ' + xpath + ' clicked' + os.linesep)
    print(value + ' set')
    log.write(now + ' ' + value + ' set' + os.linesep)
    time.sleep(1)

    #scroll_down(200)
    #click on taxonomies
    xpath = "//a[contains(@href,'%s-tax')]" % dropdown_menu_html_id
    el = driver.find_element_by_xpath(xpath)
    el.click()
    print(xpath + ' clicked')
    log.write(now + ' ' + xpath + ' clicked' + os.linesep)
    time.sleep(0.5)

    #click on $category_html_id
    xpath = "//input[contains(@id, '%s') and contains(@id, 'categories-%s')]" % (dropdown_menu_html_id, category_html_id)
    el = driver.find_element_by_xpath(xpath)
    el.click()
    print(xpath + ' clicked')
    log.write(now + ' ' + xpath + ' clicked' + os.linesep)
    time.sleep(1)

    # save
    xpath = "//input[contains(@id,'%s-savewidget')]" % dropdown_menu_html_id
    el = driver.find_element_by_xpath(xpath)
    print(xpath + ' clicked')
    log.write(now + ' ' + xpath + ' clicked')
    el.click()

def calculate_time():
    '''function to calculate elapsed time'''
    time2 = time.time()
    hours = int((time2-time1)/3600)
    minutes = int((time2-time1 - hours * 3600)/60)
    sec = time2 - time1 - hours * 3600 - minutes * 60
    print("processed in %dh:%dm:%ds" % (hours, minutes, sec))

if __name__ == '__main__':
    setbrowser()
    login()
    setwidget()
    calculate_time()
    log.close()
    driver.close()
    print('Done.')
