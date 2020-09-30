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
from selenium.webdriver.common.keys import Keys

#my important variables
class_time = 55*60
end_class_before_how_many_seconds_of_next_class = 0
seconds_late_to_class = 900
cookie_file1 = "cookie1.data"
profile_path_file = "pf.txt" 
week_days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

parser = argparse.ArgumentParser(description="Meets automator Script\n"+str(subject_list)+"\nMake sure you use right index to start class.", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-s", "--start", help="Start the specified class.",action="store",type=str)
parser.add_argument("-l","--links", help="Show Links.", action="store_true")
parser.add_argument("--saveCookie", help="saves cookie to local file, make sure you have a cookie file to prevent login issues for class.",action="store_true")
parser.add_argument("-a","--auto",help="Automates all 4 classes, based on day and timetable.",action="store_true")
parser.add_argument("-t","--timetable", help="Shows timetable", action="store_true")
parser.add_argument("-w","--wait",help="wait for classes to begin, instead of Ending script.",action="store_true")
parser.add_argument("-v","--verbose",help="Show extensive log",action="store_true")

def wait1(hr,minu):
    now = datetime.datetime.now()
    wait_minute=0
    if now.hour!=hr:
        wait_minute += (60-now.minute)
    wait_minute+=minu
    for i in range(wait_minute,0,-1):
        print("[+] waiting for",i,"minute",end='\r')
        sleep(60)

def attend_class(class_link,hr,minu):
    pfile = open(profile_path_file,"r")
    profile = pfile.read()
    args.verbose and print("[+] Profile load success") 
    opti = webdriver.ChromeOptions() 
    opti.add_argument("user-data-dir="+profile)
    args.verbose and print("[+] ChromeOptions initialised success")
    driver = webdriver.Chrome(options=opti)
    driver.get("https://accounts.google.com/login")
    cookies = pickle.load(open(cookie_file1,"rb"))
    for i in cookies:
        if 'expiry' in i:
            i['expiry'] = int(i['expiry'])
        driver.add_cookie(i)
    args.verbose and print("[+] Log in success")
    driver.get(class_link)
    sleep(2)
    args.verbose and print("[+] Load class link success")
    driver.find_element_by_xpath("//body").send_keys(Keys.CONTROL,'d')
    args.verbose and print("[+] Disable Microphone success")
    sleep(1)
    driver.find_element_by_xpath("//body").send_keys(Keys.CONTROL,'e')
    args.verbose and print("[+] Disable Camera success")
    sleep(5)
    driver.find_element_by_xpath("""//*[@id="yDmH0d"]/c-wiz/div/div/div[5]/div[3]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span/span""").click()
    args.verbose and print("[+] Start class successs")
    wait1(hr,minu)
    try:
        driver.find_element_by_xpath("""//*[@id="ow3"]/div[1]/div/div[5]/div[3]/div[9]/div[2]/div[2]/div""").click()
        args.verbose and print("[+] Click on end call")
    except:
        print("[-] Failed to end class")
    sleep(2)
    driver.close()
    args.verbose and print("[+] Force close success")


args = parser.parse_args()

if args.links:
    print("\n\n")
    list_of_links=[] 
    for i in dictionary_of_links:
        list_of_links.append([i,dictionary_of_links[i]])
    print(tabulate(list_of_links,["Subject","Link"],"fancy_grid"))

if args.saveCookie:
    driver = webdriver.Chrome()
    driver.get("https://accounts.google.com/login")
    input("[?] Sign in and press enter")
    pickle.dump( driver.get_cookies() , open(cookie_file1,"wb"))
    print("[+] Cookie file saved.")
    driver.close()
    print("\n[+] We need a chrome profile \n(that has permissions)\n i cannot get it on my own\nFollow my instructions and provide me that\n\nGo to Chrome\ntype 'chrome://version' in search without quotes")
    print("[+] Search for Profile path and copy that path and paste here")
    pf = str(input("Path:> ")).replace('Default','')
    pfile = open(profile_path_file,"w")
    pfile.write(pf)
    pfile.close()
    print("\n[+] This profile will be loaded while attending class.\n")

if args.start:
    if int(args.start)>6:
        print("[-] Choose right index.")
        quit()
    print("\n[+] Attending "+subject_list[int(args.start)]+" class.")    
    class_link=dictionary_of_links[subject_list[int(args.start)]]
    attend_class(class_link)

if args.timetable:
    ttlist = []
    for i in range(5):
        temp=[week_days[i]]
        for j in range(4):
            temp.append(subject_list[tt[i][j]])
        ttlist.append(temp)
    print(tabulate(ttlist,[" ","9 - 10","10 - 11","11 - 12","12 - 1"],"fancy_grid"))

if args.auto:
    present_time = datetime.datetime.now()
    present_day = present_time.weekday()
    while True:
        if present_day not in [0,1,2,3,4]:
            print("\n\n[-] Not a good day to attend classes.\n")
            break
        if args.wait :
            if (present_time.hour < 7):
                print("\n\n[-] Wait time is more than an hour, better come at 8")
            elif (present_time.hour ==8):
                delta = datetime.timedelta(hours=1)
                now = datetime.datetime.now()
                next_hour = (now + delta).replace(microsecond=0, second=0, minute=2)
                class_time = (next_hour - now).seconds 
                for i in range(class_time,-1,-1):
                    print("[+] Attending classes in",i,"sec",end="\r")
                    sleep(1)
        present_time = datetime.datetime.now()
        if (present_time.hour < 9 or (present_time.hour > 13 and present_time.minute > 30)) :
            print("\n\n[-] No classes to attend now.\n")
            break
        elif (present_time.hour ==9 ):
            index_of_tt = 0
            end_time = [10,0]
        elif (present_time.hour==10):
            if  present_time.minute>10:
                index_of_tt = 1
                end_time = [11,10]
            else:
                wait1(10,10)
                continue
        elif (present_time.hour==11 ):
            if present_time.minute>20:
                index_of_tt = 2
                end_time = [12,20]
            else:
                wait1(11,20)
                continue
        elif (present_time.hour == 12 ):
            if  present_time.minute>30:
                index_of_tt = 3
                end_time = [13,30]
            else:
                wait1(12,30)
                continue
        index_of_class = tt[present_day][index_of_tt]
        print("[+] Attending "+subject_list[index_of_class]+" class.")
        class_to_attend = dictionary_of_links[subject_list[index_of_class]]
        attend_class(class_to_attend,end_time[0],end_time[1])
        print("\n\n")
        
