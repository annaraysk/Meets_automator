# Meets_automator
Automator in work

Automates the class attending process. Presently the script can attend classes you specify.

It will use New profile for each webdriver instance, So permissions for Webcam and Microphone are not permitted, Might well add Profiles in future commits, which will allow these permissions and modify script to disable microphone and webcam.

For now, you do that work.

## Features
* help : provides you with help in using script.
* list : lists the class links.
* saveCookie : Saves the cookie file locally in your Documents, these cookies are used to login next time in class, make sure you use this option to save cookies so that starting class doesnt end up in cookie file missing error.
* start : Starts class, check Usage part, start is provided with index of class, index is 0 based and starts the class whose index you provide.

## Usage 
python3 script.py [-h] [-s START] [-l] [--saveCookie]

Use that h flag to open help and follow instructions.

## Installation
1. Clone the repository
2. Python3 installed and environments set.
3. Chrome installed.
4. Install all requirements
   `python3 -m pip install -r requirements.txt`
5. Start with help bitches!!

## Feedbacks
Mail me bugs or improvements at annaraykalashetty1999@gmail.com 

Will be updating script to attend all 4 classes based on day, WAIT

Use your python knowledge to add your subject to list and update link for that subject (Do atleast that).
