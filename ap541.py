#!/usr/bin/python
#
# Author  = Andrej Frank, IT-Designers GmbH, STZ Softwaretechnik
# Version = 0.0.1 Alpha
#
# connect to the AP641 WebUI Access Point and get the config.xml, 
#
# 1) post /admin.cgi?action=logon and get the cookieValue from data
# 2) post /config-dump.cgi and get the config.xml from data (attachment as response)
#

import httplib
import urllib
import time
import sys
import readConfig

class AP541:
    def __init__(self, host, hostenv):
        self.host = host
        self.login_url ='/admin.cgi?action=logon'
        self.get_url='/config-dump.cgi'
        self.username = hostenv['username']
        self.password = hostenv['password']
        self.remotepath = hostenv['ap541'][0]['remotepath'] 
        self.session = ''
        self.headersLogin = {'Connection':'keep-alive', 
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Origin':'https://'+self.host,
            'DNT': '1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36', 
            'Referer':'https://'+self.host+self.login_url, 
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Cache-Control': 'max-age=0'
        }
        self.paramsLogin = urllib.urlencode({'i_username':self.username, 'i_password':self.password, 'login':'Log In'})
        self.headersCMD = {'Connection':'keep-alive', 
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Origin':'https://'+self.host,
            'DNT': '1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36', 
            'Referer':'https://'+self.host+'/admin.cgi?action=config_man', 
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Cache-Control': 'max-age=0',
            'Cookie':''
        }
        self.paramsCMD = 'configBackup=&downloadServerip='
    
    def login(self):
        """ log in and set the cookie sessionSSL
            return:  status, message"""
        conn = httplib.HTTPSConnection(self.host)
        conn.request("POST", self.login_url, self.paramsLogin, self.headersLogin)
        response = conn.getresponse()
        time.sleep(1)  # wait 1 second
        if response.status == 200:
            #print "[+] status: ",response.status,"  reason: ", response.reason
            data = response.read()
            #print data
            for line in data.split('\n'):
                ## the line is similar to
                ## ' var cookieValue = "asdfASDFasdfASDFasdfASDFasdfASDF";'  32 byte
                if 'cookieValue' in line:
                    self.session = 'sessionSSL='+line.split('"')[1]
                    #print data
                    #print "session: "+self.session
                    if self.session == '':
                        return -1, "no sessionSSL, connection ok, to much connections?"
                    return response.status, response.reason
        return response.status, response.reason

    def get_config(self):
        self.headersCMD['Cookie']=self.session
        conn = httplib.HTTPSConnection(self.host)
        conn.request("POST", self.get_url, self.paramsCMD, self.headersCMD)
        time.sleep(1)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            with  open(self.remotepath, 'w') as f:
                f.write(data)
            return True
        return False

    # TODO: implement logout, ap541 handle to few connection 
    def logout(self):
        pass
        
    def __str__(self):
        return 'AP541 : host: '+self.host +"\n"+ \
          "username: "+self.username+ "\n"+ \
          "remotepath: " + self.remotepath + "\n"

if __name__ == '__main__':
    # this should be moved to test file
    ENV  = readConfig.read(configpath='smc.conf.example')
    #readConfig.printOut(ENV)
    host = 'ap541.mycompany.com'
    
    if host in ENV.keys():
        hostenv=ENV[host]
    else:
        print "ERROR, no host config found"
        sys.exit(-1)
    print hostenv
    cl = AP541(host, hostenv)
    print cl
    r, msg = cl.login()
    print r, msg
    if r==200:
        r=cl.get_config()
        if r:
            print "ok"
        else:
            print "error"
    else:
        print "error: ", r, msg
