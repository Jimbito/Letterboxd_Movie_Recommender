from cProfile import run
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import urllib
import urllib.request
import tempfile
import json
import re as regex


class WebDriver():
    '''
    This class is used to control the webdriver and scraper
    Attributes:
        url (str): The URL of the home webpage to navigate to
        driver (selenium.webdriver): The webdriver object
    '''

    def __init__(self, url) -> None:
        '''
        See help(WebDriver) for accurate signature
        '''
        self.url = url


    def open_the_webpage(self) -> None:
        '''
        This function is used to open the webpage to the URL defined in the instance attribute and close any pop-ups
        Returns:
            None
        '''
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options=Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.driver.maximize_window() #maximised window helps reduce the frequency of unclickable elements
        self.accept_cookies()
        self.what_to_scrape()
    
    def accept_cookies(self, css: str = '#tyche_cmp_modal > div > div > div > div:nth-of-type(5) > div:nth-of-type(2) > a') -> None:
        '''
        This function is used to close the accept cookies pop-up
        Returns:
            None
        '''
        accept_cookies_css = css
        button = self.driver.find_element(By.CSS_SELECTOR, accept_cookies_css)
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button)).click()
    

    def what_to_scrape(self, 
    css1: str = '#html > body > ul:first-of-type',
    css2: str = '#html > body > ul:nth-of-type(3)',
    css3: str = '#html > body > ul:nth-of-type(4)'):
        
        
        year_css = css1
        popularity_css = css2
        genre_css = css3
        

        year_container = self.driver.find_element(By.CSS_SELECTOR, year_css)
        container_items = year_container.find_elements(By.TAG_NAME, 'li')
        items = {}
        for item in container_items[1:]:
            a_tag = item.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            outer_html = item.get_attribute('outerHTML')
            option_key = regex.search('">(.*)</a>', outer_html).group(1)
            key_value = {option_key:href}
            items.update(key_value)
        print(items)
        

    def next_page(self, xpath: str='//*[@id="films-browser-list-container"]/div/div[2]/a') -> None:
        '''
        This function waits for the pressence of the 'load_more' button and clicks using actionchains to avoid 
        "Element is not clickable" error.
        Returns:
            None
        '''
        next_page_xpath = xpath
        try:
            button = self.driver.find_element(By.XPATH, next_page_xpath)
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(button)).click()
        except:
            pass


    def obtain_poster_hrefs(self, xpath: str='//*[@id="films-browser-list-container"]/ul') -> list:
        '''
        This function locates all posters in the poster_list container and itterates through, obtaining 
        all poster hrefs. Poster hrefs are then appended to href_list. 

        Returns:
            List
        '''
        href_list = []
        poster_list_xpath = xpath
        poster_list = self.driver.find_element(By.XPATH, poster_list_xpath)
        posters = poster_list.find_elements(By.TAG_NAME, 'li')

        for poster in posters:
            a_tag = poster.find_element(By.TAG_NAME, 'a')
            href = a_tag.get_attribute('href')
            href_list.append(href)
        return href_list

    def obtain_film_name(self, xpath: str='//*[@id="featured-film-header"]/h1') -> str:
        '''
        
        '''
        film_xpath = xpath
        element = self.driver.find_element(By.XPATH, film_xpath)
        outer_html = element.get_attribute('outerHTML')
        film = regex.search('>(.*)</h1>', outer_html).group(1)
        return film
        
    def obtain_film_date(self, xpath: str='//*[@id="featured-film-header"]/p/small/a') -> str:
        '''
        
        '''
        date_xpath = xpath
        try:

            element = self.driver.find_element(By.XPATH, date_xpath)
            outer_html = element.get_attribute('outerHTML')
            date = regex.search('>(.*)</a>', outer_html).group(1)
        except:
            pass
        return date 

    
    def obtain_film_tagline(self, xpath: str='//*[@id="film-page-wrapper"]/div[2]/section[2]/section/div[1]/h4') -> str:
        '''
        
        '''
        tagline_xpath = xpath
        try:
            element = self.driver.find_element(By.XPATH, tagline_xpath)
            outer_html = element.get_attribute('outerHTML')
            unformatted_tagline = regex.search('>(.*)</h4>', outer_html).group(1)
            tagline = unformatted_tagline.replace('&nbsp;', ' ')
        except:
            tagline = None
        return tagline


    def obtain_film_description(self, xpath: str='//*[@id="film-page-wrapper"]/div[2]/section[2]/section/div[1]/div/p') -> str:
        '''
        
        '''
        description_xpath = xpath
        try:
            element = self.driver.find_element(By.XPATH, description_xpath)
            outer_html = element.get_attribute('outerHTML')
            unformatted_description = regex.search('<p>(.*)</p>', outer_html).group(1)
            description = unformatted_description.replace('&nbsp;', ' ')
        except:
            # film has no description.
            pass
        return description


    def obtain_director(self, xpath: str='//*[@id="featured-film-header"]/p/a/span') -> str:
        '''
        
        '''
        director_xpath = xpath
        try:
            element = self.driver.find_element(By.XPATH, director_xpath)
            outer_html = element.get_attribute('outerHTML')
            director = regex.search('>(.*)</span>', outer_html).group(1)
        except:
            # no director listed.
            pass
        return director

    
    def obtain_film_genres(self, xpath: str='//*[@id="tab-genres"]/div/p') -> list:
        '''
        
        '''
        genre_xpath = xpath
        genre_list =[]
        genre_container = self.driver.find_element(By.XPATH, genre_xpath)
        genres = genre_container.find_elements(By.TAG_NAME, 'a')
        
        for genre in genres:
            try:
                outer_html = genre.get_attribute('outerHTML')
                genre = regex.search('>(.*)</a>', outer_html).group(1)
                genre_list.append(genre)
            except:
                # genre error
                pass
        return genre_list


    def obtain_film_cast(self, xpath: str='//*[@id="tab-cast"]/div/p') -> list:
        '''
        
        '''
        cast_xpath = xpath
        cast_list = []
        cast = self.driver.find_element(By.XPATH, cast_xpath)
        actors = cast.find_elements(By.TAG_NAME, 'a')

        for actor in actors:
            try:
                outer_html = actor.get_attribute('outerHTML')
                actor_name = regex.search('>(.*)</a>', outer_html).group(1)
                cast_list.append(actor_name)
            except:
                # actor_name error
                pass
        return cast_list


    def obtain_film_poster(self, xpath: str='//*[@id="js-poster-col"]/section[1]/div/div/img') -> str:
        '''

        '''
        poster_xpath = xpath
        

    def scrape_film(self) -> dict:
        '''
        
        '''
        self.accept_cookies()
        film_name = self.obtain_film_name()
        film_date = self.obtain_film_date()
        film_tagline = self.obtain_film_tagline()
        film_description = self.obtain_film_description()
        film_director = self.obtain_director()
        film_cast = self.obtain_film_cast()
        film_genres = self.obtain_film_genres()
        film_dict = {"Film":film_name, "Release date": film_date, "Tagline": film_tagline, "Description":film_description,
        "Director":film_director, "Cast":film_cast, "Genres":film_genres}
        return film_dict    


    def scrape_page(self) -> dict:
        '''
        
        '''
        page_dict = {}
        href_list = self.obtain_poster_hrefs()
        for href in href_list:
            self.driver.get(href)
            film_dict = self.scrape_film() 
            film_name = film_dict.get('Film')
            page_dict.update({film_name:film_dict})
        return page_dict
    

    def film_dict_to_json(self):
        '''
        
        '''
        film_dict = self.scrape_film()
        film_name = film_dict.get('Film')

        with open(f"{film_name}.json", 'w') as fp:
            json.dump(film_dict, fp)
            
        
    
    def page_dict_to_json(self):
        '''
        
        '''
        page_dict = self.scrape_page()
        with open(f"page_dict.json", 'w') as fp:
            json.dump(page_dict, fp)



def run_scraper():
    
    URL = "https://letterboxd.com/films/"
    driver = WebDriver(URL)
    driver.open_the_webpage()
    #driver.close_down()

if __name__ == '__main__':
    run_scraper()