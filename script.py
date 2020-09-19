import argparse
from tabulate import tabulate
import pickle
from selenium import webdriver
from selenium.webdriver.chrome import service
from links_file import dictionary_of_links
from links_file import subject_list
from links_file import tt
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import datetime

#my important variables
class_time = 50*60
end_class_before_how_many_seconds_of_next_class = 600
cookie_file1 = "/home/array/Documents/cookie1.data"
cookie_file2 = "/home/array/Documents/cookie2.data"
week_days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

parser = argparse.ArgumentParser(description="Meets automator Script\n"+str(subject_list)+"\nMake sure you use right index to start class.", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-s", "--start", help="Start the specified class.",action="store",type=str)
parser.add_argument("-l","--links", help="Show Links.", action="store_true")
parser.add_argument("--saveCookie", help="saves cookie to local file, make sure you have a cookie file to prevent login issues for class.",action="store_true")
parser.add_argument("-a","--auto",help="Automates all 4 classes, based on day and timetable.",action="store_true")
parser.add_argument("-t","--timetable", help="Shows timetable", action="store_true")

def attend_class(class_link):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://accounts.google.com/login")
    cookies = pickle.load(open(cookie_file1,"rb"))
    for i in cookies:
        if 'expiry' in i:
            i['expiry'] = int(i['expiry'])
        driver.add_cookie(i)
    driver.get(class_link)
    cookies = pickle.load(open(cookie_file2,"rb"))
    for i in cookies:
        driver.add_cookie(i)
    sleep(2)
    driver.find_element_by_xpath("""//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/span/span""").click()
    sleep(2)
    driver.find_element_by_xpath("""//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span/span""").click()
    delta = datetime.timedelta(hours=1)
    now = datetime.datetime.now()
    next_hour = (now + delta).replace(microsecond=0, second=0, minute=2)
    class_time = (next_hour - now).seconds - end_class_before_how_many_seconds_of_next_class
    if class_time<0:
        class_time=1  
    sleep(class_time)
    driver.find_element_by_xpath("""//*[@id="ow3"]/div[1]/div/div[5]/div[3]/div[9]/div[2]/div[2]/div""").click()
    sleep(2)
    driver.close()

args = parser.parse_args()

if args.links:
    print("\n\n")
    list_of_links=[] 
    for i in dictionary_of_links:
        list_of_links.append([i,dictionary_of_links[i]])
    print(tabulate(list_of_links,["Subject","Link"],"fancy_grid"))

if args.saveCookie:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://accounts.google.com/login")
    input("Sign in and press enter")
    pickle.dump( driver.get_cookies() , open(cookie_file1,"wb"))
    driver.get(dictionary_of_links[subject_list[0]])
    sleep(2)
    try:
        driver.find_element_by_xpath("""//*[@id="yDmH0d"]/div[3]/div/div[2]/div[3]/div/span/span""").click()
        input("Disable Camera and Microphone.")
    except:
        pass
    pickle.dump( driver.get_cookies() , open(cookie_file2,"wb"))
    print("Cookie file saved.")
    driver.close()

if args.start:
    try:
        class_link=dictionary_of_links[subject_list[int(args.start)]]
        attend_class(class_link)
    except:
        print("Choose right index.")

if args.timetable:
    ttlist = []
    for i in range(5):
        temp=[week_days[i]]
        for j in range(4):
            temp.append(subject_list[tt[i][j]])
        ttlist.append(temp)
    print(tabulate(ttlist,[" ","9 - 10","10 - 11","11 - 12","12 - 1"],"fancy_grid"))

        
