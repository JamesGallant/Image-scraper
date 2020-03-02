from selenium import webdriver
import os
import time
from urllib import request as wget
import tqdm as tqdm
import argparse
'''

wd = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'utils\\chromedriver.exe'))
wd.get('https://google.com')
search = wd.find_element_by_css_selector('input.gLFyf')
search.send_keys('')

'''

class ScraperBot():
    def __init__(self):
        self.wd = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver.exe'))
        self.urlbase = "https://google.com/search?tbm=isch&q={}"

    def _initiateSession(self, key):
        self.wd.get(self.urlbase.format(key))

    def _acceptCookies(self):
        try:
            self.wd.execute_script("document.getElementsByClassName('USRMqe')[0].style.display = 'none';")
        except:
            pass

    def _endOfPage(self):
        try:
            self.wd.find_element_by_class_name('OuJzKb Yu2Dnd')
            print("no more files")
        except:
            pass

        try:
            self.wd.find_element_by_class_name('mye4qd').click()
            time.sleep(1)
            self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            self.wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    def _deduplicate(self, listOfurls):
        try:
            inputList = list(set(listOfurls))
            return inputList
        except:
            pass

    def _checkOpenTabs(self):
        browserTabs = self.wd.window_handles
        if len(browserTabs) > 1:
            self.wd.switch_to.window(browserTabs[1])
            self.wd.close()
            self.wd.switch_to.window(browserTabs[0])

    def _getURL(self):
        thumbs = self.wd.find_elements_by_css_selector('img.Q4LuWd')
        urls = []
        for thumbImg in thumbs:
            try:
                thumbImg.click()
                actualImg = self.wd.find_elements_by_css_selector('img.n3VNCb')

                for imageData in actualImg:
                    if 'https' in imageData.get_attribute('src'):
                        urls.append(imageData.get_attribute('src'))

                self._checkOpenTabs()
            except:
                pass
        return urls

    def _totalImages(self, dir):
        count = 0
        for filename in os.listdir(dir):
            if filename.endswith('.jpg'):
                count += 1
            else:
                continue
        return count

    def _downloader(self, data, key, out_dir):
        key = key.replace(" ", "_")
        DIR1 = os.path.join(out_dir, key)

        try:
            os.mkdir(DIR1)
        except:
            pass

        for idx in tqdm.tqdm(range(len(data))):
            filename = "{}-{}.jpg".format(key, idx)
            PATH = os.path.join(DIR1, '{}'.format(filename))

            try:
                print("downloading next batch")
                wget.urlretrieve(str(data[idx]), PATH)
            except:
                pass


    def scrape(self, search, min_image_count, directory):
        self._initiateSession(key=search)
        self._acceptCookies()

        totalImageCount = 0
        while totalImageCount < min_image_count:
            urlList = self._deduplicate(self._getURL())
            self._downloader(data=urlList,
                             key=search,
                             out_dir=directory)
            urlList.clear()
            totalImageCount = self._totalImages(os.path.join(os.getcwd(), search.replace(" ", "_")))
            print("current Image count: {}".format(totalImageCount))
            self._endOfPage()
            time.sleep(2)

        if totalImageCount >= min_image_count:
            self.wd.quit()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chrome 80 web scraper for google images")
    parser.add_argument('--search', default='Images', type=str, required=True,
                        help='The keyword to search in the browser')

    parser.add_argument('--min_image_count', default=1, type=int, required=True,
                        help='Minimum number of images, it can overshoot')

    parser.add_argument('--out_directory', default=os.getcwd(),
                        help='The full path to the output directory')

    args = parser.parse_args()

    SEARCH = args.search
    IMAGECOUNT = args.min_image_count
    OUTDIR= args.out_directory

    scraperBot = ScraperBot()
    scraperBot.scrape(search=SEARCH, min_image_count=IMAGECOUNT, directory=OUTDIR)