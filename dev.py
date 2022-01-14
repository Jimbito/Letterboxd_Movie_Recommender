from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

class WebDriver():
    def __init__(self, url) -> None:
        self.url = url

    def open_the_webpage(self) -> None:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.accept_all_cookies()
    
    
    def accept_all_cookies(self) -> None:

        sleep(1) 
        try: 
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="tyche_cmp_modal"]/div/div/div/div[5]/div[2]/a')
            accept_cookies_button.click()
        except:
            print(f'Cannot click accept cookies button.')


    
    def open_item(self):
        film_container = self.driver.find_element(By.XPATH, '//*[@id="films-browser-list-container"]/ul') 
        film_list = film_container.find_elements(By.XPATH, './li')
        link_list = []
        
        for film in film_list:
            a_tag = film.find_element(By.TAG_NAME, 'a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        print(f'There are {len(link_list)} films in this page')
        print(link_list)
                
        
class StoreData():
    '''
    This class is used to interact with the S3 Bucket and store the scraped images and features
    '''
    def __init__(self) -> None:
        pass

    def upload_image_to_datalake(self):
        pass



def run_scraper():
    URL = "https://letterboxd.com/films/popular/"
    driver = WebDriver(URL)
    driver.open_the_webpage()
    driver.open_item()
     

if __name__ == '__main__':
    run_scraper()


