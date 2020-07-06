"""
Based upon https://gist.github.com/zenwalker/0037fff3be1fbdb889bb

Automatic migration of subscriptions to another
YouTube account with Python and Selenium.

Tested on YouTube as of 2020-07-06 with:
 - selenium 3.141.0
 - firefox 78.0.1
 - python 3.8.3
 - fedora 32

 1. Install selenium from pypi:
    $ pip install selenium

 2. Go to the down of page https://www.youtube.com/subscription_manager
    and download your current subscriptions feed.
    Save file as subscription_manager.xml.

 4. Run script, enter your credentials and go to drink coffee.
    It will take some time.

Note YouTube will temporary block you if you have more that 80 subscriptions.
Just restart the script in a few hours.
"""

from collections import namedtuple
from selenium import webdriver
from xml.dom import minidom
from getpass import getpass
import time
import re


def main():
	driver = webdriver.Firefox()
	sign_in(driver)
	for channel in subs():
		result = subscribe(driver, channel)
		if result is not None and result == "too many":
			print("Manual intervention required - too many subscriptions hit.")
			break
	driver.close()


def sign_in(driver):
    email, password = input('Email: '), getpass()

    driver.get('https://www.youtube.com')
    driver.find_element_by_xpath("//yt-formatted-string[@class='style-scope ytd-button-renderer style-suggestive size-small']").click()
    time.sleep(1)

    driver.find_element_by_id('identifierId').send_keys(email)
    driver.find_elements_by_xpath("//span[contains(text(), 'Next')]")[0].click()
    time.sleep(1)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_elements_by_xpath("//span[contains(text(), 'Next')]")[0].click()
    time.sleep(1)


def subs():
    xmldoc = minidom.parse('subscription_manager.xml')
    itemlist = xmldoc.getElementsByTagName('outline')
    channel_id_regexp = re.compile('channel_id=(.*)$')
    Channel = namedtuple('Channel', ['id', 'title'])
    subscriptions = []

    for item in itemlist:
        try:
            feed_url = item.attributes['xmlUrl'].value
            channel = Channel(id=channel_id_regexp.findall(feed_url)[0],
                              title=item.attributes['title'].value)
            subscriptions.append(channel)
        except KeyError:
            pass

    return subscriptions


def subscribe(driver, channel):
	channel_url = 'https://www.youtube.com/channel/' + channel.id
	driver.get(channel_url)
	time.sleep(1)

	driver.find_elements_by_xpath("//yt-formatted-string[contains(text(), 'Subscribe')]")[0].click()
	if len(driver.find_elements_by_xpath("//*[contains(text(), 'Too many subscriptions')]")):
		return "too many"

	print('{:.<50}{}'.format(channel.title, 'done'))
	time.sleep(1)


if __name__ == '__main__':
    main()
