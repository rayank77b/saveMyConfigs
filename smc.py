#!/usr/bin/python
#
# TODO: read configuration(user,pass,what to save)
# TODO: log in ssh
# TODO: get the configs
# TODO: store it on git

import sys
import paramiko
import ConfigParser

#
ENV={}

# simple ini file
def loadENV():
    config = ConfigParser.RawConfigParser()
    config.read('smc.conf')
    sections = config.sections()
    for section in sections:
        ENV[section]={}
        for x in config.options(section):
            ENV[section][x]=config.get(section, x)

def get_copy(host):
    ip = ENV[host]['ipaddress']
    name = ENV[host]['username']
    passwd = ENV[host]['password']
    remotepath=ENV[host]['remotepath']
    localpath=ENV[host]['localpath']
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip , username=name, password=passwd)

    ftp = client.open_sftp()
    #stdin, stdout, stderr = client.exec_command(cmd)
    ftp.get(remotepath, localpath)
    #for line in stdout.readlines():
    #    print line
    client.close()   

if __name__ == '__main__':
    loadENV()
    host=ENV.keys()[0]
    print host
    get_copy(host)

