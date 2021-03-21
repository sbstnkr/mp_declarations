from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests


class MP:
    def __init__(self, id, first_name, last_name, club):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.club = club

    def get_declaration(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('/Users/chromedriver', options=chrome_options)

        driver.get(f'https://www.sejm.gov.pl/Sejm9.nsf/posel.xsp?id={self.id:03d}&type=A')

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        actionChains = ActionChains(driver)
        declarations = driver.find_element_by_xpath('//*[@id="osw"]')
        actionChains.click(declarations).perform()

        time.sleep(2)

        declaration_button = driver.find_element_by_xpath('(//*[@id="view:_id1:_id2:facetMain:_id191:holdMajatekInner"]/table/tbody/tr)[last()]')\
            .find_element_by_tag_name('a')

        declaration_url = declaration_button.get_attribute('href')
        print(declaration_url)

        declaration_date = declaration_button.text
        print(declaration_date)

        response = requests.get(declaration_url)

        with open(f'declarations/{self.id:03d}.pdf', 'wb') as pdf_file:
            pdf_file.write(response.content)
            pdf_file.close()

        driver.close()

        return declaration_date






