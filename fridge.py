
import RPi.GPIO as GPIO
import time
import smtplib
from datetime import datetime
GPIO.setmode(GPIO.BOARD)
MAIL_TO_SEND = 'tanyafain7@gmail.com'#HERE THE MAIL
# TRIG = 16 # 1: trig: 16, echo: 11. 2: trig: 18, echo: 19. 3: trig: 22, echo: 23.
# ECHO = 11
shelf_dictionnary = {}

def empty(TRIG, ECHO, is_empty):
    i=0
    GPIO.setup(TRIG,GPIO.OUT) # to define trig as output
    GPIO.setup(ECHO,GPIO.IN) # to define ecgo as input


    GPIO.output(TRIG,False)
    print("Calibrating...")
    time.sleep(2)

    print("place the object....")

    try:
        while i<1:
            GPIO.output(TRIG,True)
            time.sleep(0.00001)
            GPIO.output(TRIG,False)

            while GPIO.input(ECHO)==0:
                pulse_start = time.time()

            while GPIO.input(ECHO)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance+1.15, 2)

            if distance <=20  and distance >=5:
                print("Distance:" , distance, "cm", TRIG)

            if distance > 20 :
                is_empty = "Not"
                print("Place the object...")
            i+=1
            time.sleep(2)

        if is_empty == "Not":
            return False
        return True

    except KeyboardInterrupt:
        GPIO.cleanup()




def send_mail_to_restaurant():
    gmail_user = 'fridgeofpeople@gmail.com'
    gmail_password = 'aharai123'

    sent_from = gmail_user
    to = [MAIL_TO_SEND]
    subject = 'Empty Fridge'
    body = 'Dear Restaurant the Fridge of people  is empty please come put some food '

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:

        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)

def send_mail_to_volonteer(shelf_num):
    gmail_user = 'fridgeofpeople@gmail.com'
    gmail_password = 'aharai123'

    sent_from = gmail_user
    to = [MAIL_TO_SEND]
    subject = 'Bad food in shelf ' + str(shelf_num)
    body = 'Dear Volonteer, on the shelf ' + str(
        shelf_num) + " The food gone wrong please come take the food "

    email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
        """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)


def add(shelf, date):
    shelf_dictionnary[shelf] = date

def erase(shelf):
    shelf_dictionnary.pop(shelf)

def menu():
    question = "Menu: if you want to take food please press 1, if you to put food please press 2 otherwise" \
                        "press 3."
    answer = int(input(question))
    while answer not in list(range(1, 4)):
        answer = int(question)
    if answer == 2:
        shelf = (input("Which shelf ?"))
        date = input("Peremption date ?")  # day.month
        add(shelf, date)

    elif answer == 1:
        shelf = int(input("Which shelf?"))
        erase(shelf)
        print("bon appetit!!")
    elif question == 3:
            print("thank you anyway!!")

def update():

    today = datetime.now()
    today_day_date = int(str(today.date())[8:10])
    today_month_date = int(str(today.date())[5:7])
    for key in shelf_dictionnary.keys():

        day = int(shelf_dictionnary[key][:2])
        month = int(shelf_dictionnary[key][3:])
        if day - today_day_date <= 0 and today_month_date - month <= 0:
            send_mail_to_volonteer(key)



if __name__ == '__main__':

    while True:
        is_empty = "yes"

        if ( not empty(16,11,is_empty) ) and (  not empty(18,19,is_empty) ):
                send_mail_to_restaurant()
        menu()
        update()

