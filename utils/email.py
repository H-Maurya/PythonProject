import smtplib  # python email library
# setting gmail servers
server = smtplib.SMTP('smtp.gmail.com', 587)
# establishing connection to mail servers
server.starttls()


def getEmailInfo():
    return {"email": "testingpythonemails17@gmail.com",  "password": "PythonC++"}


def sendMail(mail, message):
    # getting senders info
    info = getEmailInfo()
    # login with credentials
    server.login(info['email'], info['password'])
    # sending final mail
    server.sendmail(info['email'], mail, message)
