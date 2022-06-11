##you can find the documentation of this code in this link : https://www.codexpace.ml/2022/06/python-code-to-scrap-images-from-google.html
import bs4
import requests
from selenium import webdriver
import os
import time

download_failed = 0

def download_image(url ,folder_name ,num):
    #write image to a file
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name ,str(num)+".jpg") ,"wb") as file:
            file.write(response.content)

to_search = input("enter the topic : ")

folder_name = to_search
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

chrome_driver_path = r'/Users/saransh/scraper_for_data_set_gen/chromedriver'
driver  = webdriver.Chrome(chrome_driver_path)

search_url = "https://www.google.com/search?q=" + to_search + "&rlz=1C5CHFA_enIN987IN987&source=lnms&tbm=isch&sa=X&ved=2ahUKEwign5_Cy-73AhXVH7cAHXj0AisQ_AUoA3oECAMQBQ"
driver.get(search_url)

for scroll_indx in range(0 ,5):
    driver.execute_script("window.scrollTo(0, 10000)")

page_html = driver.page_source

page_soup = bs4.BeautifulSoup(page_html ,'html.parser')
containers = page_soup.find_all('div' ,{'class':"isv-r PNCib MSM1fd BUooTd"})

len_containers = len(containers)
print("[+] Found %s image containers"%(len(containers)))



for indx in range(1 ,len_containers+1):
    if indx%25 == 0:
        continue
    
    x_path = """//*[@id="islrg"]/div[1]/div[%s]"""%indx
    preview_image_xpath = """//*[@id="islrg"]/div[1]/div[2]/a[1]/div[1]/img"""
    preview_image_element = driver.find_element_by_xpath(preview_image_xpath)
    preview_image_url = preview_image_element.get_attribute("src")

    ##click on the image container
    driver.find_element_by_xpath(x_path).click()

    time_started = time.time()

    while True:
        image_element = driver.find_element_by_xpath("""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img""")
        image_url = image_element.get_attribute("src")

        if image_url != preview_image_url:
            break
        else:
            ##timeout if the full res image can't be loaded
            current_time = time.time()
            if current_time - time_started > 10:
                print("[-] Timed-out ,loading low resolution image")
                break
        
    ##downloading image
    try:
        download_image(image_url ,folder_name ,indx)
        print("[+] Downloaded images %s out of %s"%(indx ,len_containers+1 ))
        print("[+] Download link : %s"%image_url)
    except:
        print("[-] couldn't download an %s image ,continuing dowloading the next "%indx)
        download_failed += 1
print("Total downloaded %d out of %s"%(len_containers - download_failed - 1 ,len_containers))
