#!/usr/bin/python
#
# Author  = Andrej Frank, IT-Designers GmbH, STZ Softwaretechnik
# Version = 0.0.1 Alpha
#
# connect to the pc6248 WebUI switch and get the running-config, 
# with upload to server
#
# 1) login
# 2) get /File_Upload_to_Server.html
#      there are 4 method: tftp, scp, sftp, http 
#      we use scp, you must run a ssh-server
# 3) send request
#      need: server ip, dest. file name, dest. path, username, password, which file
#      at moment we save only running-config
#
# why all this? why not direct per ssh+enable+show running-config?
# have problems with paramiko, broken channel, maybe in future direct.
#

import httplib
import urllib
import time
import sys
import readConfig

class PC6248:
    def __init__(self, host, hostenv, sshenv):
        self.host = host
        self.login_url ='/newlogin.html'
        self.get_url='/File_Upload_to_Server.html'
        self.origin = 'https://'+self.host
        self.switch_user = hostenv['username']
        self.switch_pass = hostenv['password']
        self.server_ip   = sshenv['ipaddress']
        f = hostenv['pc6428'][0]['remotepath']  # TODO: array: here can be different files
        self.server_file = f.split('/')[-1]
        self.server_path = f.split(self.server_file)[0]
        self.server_user = sshenv['username']
        self.server_pass = sshenv['password']
        self.sid = ''
        self.headersLogin = {'Connection':'keep-alive', 
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Origin':self.origin, 
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36', 
            'Referer':'https://'+self.host+self.login_url, 
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Cache-Control': 'max-age=0'
        }
        self.paramsLogin = urllib.urlencode({'uname':self.switch_user, 'pwd':self.switch_pass, 'err_flag':'0', 'err_msg':'', 'submit_flag':'1'})
        self.headersCMD = {'Connection':'keep-alive', 
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Origin':self.origin, 
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36', 
            'Referer':'https://'+self.host+self.get_url, 
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Cache-Control': 'max-age=0',
            'Cookie':''
        }
        self.paramsCMD = 'v_1_1_1=Config+script&v_1_1_1=Configuration&v_1_2_1=SCP' \
          + '&v_1_2_1=SCP&v_2_1_1='+self.server_ip+'&v_2_1_1='+self.server_ip \
          + '&v_2_2_1='+self.server_file+'&v_2_2_1='+self.server_file \
          + '&v_2_7_1='+self.server_path+'&v_2_7_1='+self.server_path \
          + '&v_2_4_1='+self.server_user+'&v_2_4_1='+self.server_user+'&v_2_5_1='+self.server_pass \
          + '&v_2_3_1=XIE_UI_ENUMVAL1&v_2_3_1=Running+Configuration&v_2_77_1=' \
          + '&v_3_1_2=IPv4&v_3_1_3=running-config&v_3_1_40=image1&v_3_1_20=' \
          + '&v_3_1_7=running-config&v_3_1_15=running-config&v_3_1_10=1' \
          + '&submit_flag=8&submit_target=upload_progress_dell.html' \
          + '&err_flag=0&err_msg=&clazz_information=File_Upload_to_Server.html' \
          + '&v_3_1_1=Apply+Changes'
    
    def login(self):
        """ log in and set the cookie sidssl
            return:  status, message"""
        conn = httplib.HTTPSConnection(self.host)
        conn.request("POST", self.login_url, self.paramsLogin, self.headersLogin)
        response = conn.getresponse()
        time.sleep(1)  # wait 1 second
        if response.status == 200:
            #print "[+] status: ",response.status,"  reason: ", response.reason
            headers = response.getheaders()
            cookie=''
            for h in headers:
                if 'set-cookie' in h[0]:
                    cookie=h[1]
            sidssl=''
            for x in cookie.split(';'):
                if 'SIDSSL' in x:
                    sidssl=x
            if sidssl=='':
                conn.close()
                return -1, "No SIDSSL found"
            self.sid=sidssl
            return response.status, response.reason
        return response.status, response.reason

    def get_config(self):
        self.headersCMD['Cookie']=self.sid
        conn = httplib.HTTPSConnection(self.host)
        conn.request("POST", self.get_url, self.paramsCMD, self.headersCMD)
        time.sleep(4)
        response = conn.getresponse()
        if response.status == 200:
            return True
        return False

    def __str__(self):
        return 'PC6428: host: '+self.host +"\n"+ \
          "username: "+self.switch_user + "\n"+ \
          "file: " + self.server_file + "\n"+ \
          "path: "+self.server_path

if __name__ == '__main__':
    # this should be moved to test file
    ENV=readConfig.read(configpath='smc.conf.example')
    host='swicht01.mycompany.com'
    
    if 'ssh-server' in ENV.keys():
        sshenv = ENV['ssh-server']
    else:
        print "ERROR, no ssh-server config found"
        sys.exit(-1)
    if host in ENV.keys():
        hostenv=ENV[host]
    else:
        print "ERROR, no host config found"
        sys.exit(-1)
    #print sshenv
    #print hostenv
    cl = PC6248(host, hostenv, sshenv)
    #print cl
    r, msg = cl.login()
    print r, msg
    if r==200:
        r=cl.get_config()
        if r:
            print "ok"
        else:
            print "error"

