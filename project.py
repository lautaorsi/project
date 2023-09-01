from email.message import EmailMessage
import os
import time
import ssl
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from shirtificate import shirtificate
import inflect
from pyfiglet import Figlet


values = ['ID','FIRST NAME','LAST NAME','SCORE','EMAIL']
positions = [0,1,2,3,4]



def main():
    values = ['ID','FIRST NAME','LAST NAME','SCORE','EMAIL']

    #Ask for credentials

    os.system('cls')
    cancel()
    username = input("User:")
    check(username)
    password = input('Password:')
    check(password)
    os.system('cls')
    cancel()

    validate()




    #Validate credentials
    log(username, password)
    time.sleep(1)
    os.system('cls')
    

    cancel()
    file_loc = input('Insert the excel path: ')
    check(file_loc)

    #check for right path
    try:
        ex = pd.read_excel(file_loc)
    except FileNotFoundError:
        sys.exit('Path not found')



    #Check for excel pattern    
    headers = excel()
    pass_mark = int(input('Please insert the overall passing score: '))
    check(pass_mark)



    #create list of dictionaries
    students = []
    #iterate by row
    for j in range((ex.shape[0])):
        c = 0
        dictionary = {'ID': [],'FIRST NAME': [],'LAST NAME': [],'SCORE': [],'EMAIL': []}
        #iterate by column
        for i in headers:
            #create dictionary for each student (ex.iloc gets a cell by calling [column,row])
            dictionary[values[int(i)]].extend([ex.iloc[j,c]])
            c += 1
        students.append(dictionary)
    

    

    
    #creating email for the automatizer
    em = MIMEMultipart('alternative')
    em['From'] = username
    em['subject'] = input('Email subject: ')
    check(em['subject'])
    for student in students:
        em['To'] = (student['EMAIL'])[0]
        if grade(student['SCORE']) >= pass_mark:
            cookies = cookify(grade(student['SCORE']))
            pass_text = f'Congratulations dear {name(student)} on passing the CS50 course! You got an astonishing {grade(student["SCORE"])}, here are {cookies} cookies for your amazing work ' + cookies
            body = MIMEText(pass_text)
            em.attach(body)
            em.attach(shirtificate(f'{name(student)} '))
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(username, password)
                smtp.sendmail(username, (student['EMAIL'])[0], em.as_string())
        else:
            fail_text = f'Sorry {name(student)}, your grade is not enough to pass CS50, but dont give up! {name(student)}, here is a cookie for all your effort, keep going! 🍪 ' 
            body = MIMEText(fail_text)
            em.attach(body)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(username, password)
                smtp.sendmail(username, (student['EMAIL'])[0], em)


    




            

        

def grade(list):
    total = 0
    for i in list:
        total += float(i) 
    return(int(total/len(list)))


def log(user, pas):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, pas)
            print('Login successful!')
    except (smtplib.SMTPAuthenticationError):
        sys.exit('Incorrect username or password, please try again')
    
    
def cookify(n):
    text = ''
    for i in range(int(n)):
        text += '🍪'
    return text
   


def validate():
    for i in range(2):
        print('Validating.')
        time.sleep(0.5)
        os.system('cls')
        cancel()
        print('Validating..')
        time.sleep(0.5)
        os.system('cls')
        cancel()
        print('Validating...')
        os.system('cls')
        cancel()


def excel():
        p = inflect.engine()
        os.system('cls')
        cancel()
        global values
        while True:
            out = ''
            c = 1
            print('\n')
            print('                                                                                 ------------------        Please select the excel headers order')
            print('                                                                                 |HEADERS:        |        ')
            print('                                                                                 | 0- ID          |        Score may be selected more than once')
            print('                                                                                 | 1- FIRST NAME  |        ') 
            print('                                                                                 | 2- LAST NAME   |        The excel must contain both email and score columns')
            print('                                                                                 | 3- SCORE       |        ')  
            print('                                                                                 | 4- EMAIL       |              Example: 0-1-2-3-3-3-4')  
            print('                                                                                 ------------------')
            
            #get desired order and transform into list which will be used on the code
            order = input('Order:')
            check(order)
            order = order.split('-')
            os.system('cls')
            cancel()
            #Verify email and score are included
            if not ('3' in order) and not ('4' in order):
                sys.exit('Please include score and email columns')
            if not ('3' in order):
                sys.exit('Please include a score column')
            if not ('4' in order):
                sys.exit('Please include an email column')

            #create a user-friendly output to validate the input
            for i in order:
                if i == '':
                    continue
                i = int(i)
                if i == 3:
                    w = (p.ordinal(c)).upper()
                    out += f'{w} SCORE | '
                    c += 1
                else:
                    out += f'{values[i]} | '
            #validate the user's input
            print(f'                                                                                         Is this the desired order? \n \n                                                                      | {out} \n \n')
            conf = input('(yes/no):').lower()
            check(conf)
            if conf == 'yes':
                break
            else:
                os.system('cls')
                continue
        #return the list
        return(order)

def location(head):
    global positions
    if int(head) in positions:
        return(positions.index(int(head)))
    else:
        sys.exit(f'{values[int(head)]} could not be found in the spreadsheet')

def name(student):
    name = ''
    if len(student['FIRST NAME']) == 1:
        name += f'{(student["FIRST NAME"])[0]}'
    if len(student['LAST NAME']) == 1:
        name += f'{(student["LAST NAME"])[0]}'
    if name == '':
        name = 'student'


def word(n):
     p = inflect.engine()
     words = p.number_to_words(n)
     return(words)

def cancel():
    print('                                                                                 To stop the program simply write "stop" \n')

def check(x):
    f = Figlet('doom')
    if x.lower() == 'stop':
        os.system('cls')
        out = f.renderText('Program stopped')
        sys.exit(out)



if __name__ == "__main__":
    main()