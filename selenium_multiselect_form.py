from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
import time
import random


def multiselect(driver, xpath_text, labels):
    select = Select(driver.find_element_by_xpath(xpath_text))
    for label in labels:
        select.select_by_visible_text(label)


first_page = "http://www.nla.gov.au/apps/libraries/?action=LibSearch&adv=1"
driver = webdriver.Firefox()
driver.get(first_page)

multiselect(driver, '//select[contains(@name,"libtype")]',
            ['National', 'Public', 'School (K-12)', 'State/Territory'])
driver.find_element_by_xpath('//input[contains(@name,"dosearch")]').click()

page_no = '0'
WebDriverWait(driver, 30).until(
    staleness_of(driver.find_element_by_tag_name('html')))

while int(page_no) < 123:

    time.sleep(3 + random.random() * 2)
    response = Selector(text=driver.page_source)
    page_no = response.xpath('//p/b/text()')[0].extract()

    with open("pages/" + str(page_no) + ".html", 'wb') as f:
        f.write(driver.page_source.encode('utf-8'))

    driver.find_element_by_xpath('//p/b/following::input').click()

driver.quit()
