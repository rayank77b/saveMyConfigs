#!/usr/bin/python
#
# TODO: read configuration(user,pass,what to save)
# TODO: log in ssh
# TODO: get the configs
# TODO: store it on git( clone if not exists, commit, push)

#import git
import subprocess
import sys
import paramiko
import ConfigParser

#
ENV={}

#example of smc.conf
#[git]
#repo=https://rayank77b:xxxxx@github.com/rayank77b/testGitEclipse.git
#repopath=/home/ray/tmp/testGitEclipse
#
#[host]
#cmd=copy
#ipaddress=xxxxxx
#username=ray
#password=xxxxx
#remotepath=/etc/hosts
#localpath=test/hosts


# simple ini file
def loadENV(configpath='smc.conf'):
    config = ConfigParser.RawConfigParser()
    config.read(configpath)
    sections = config.sections()
    for section in sections:
        ENV[section]={}
        for x in config.options(section):
            ENV[section][x]=config.get(section, x)

def get_copy(host):
    hostip     = ENV[host]['ipaddress']
    name       = ENV[host]['username']
    passwd     = ENV[host]['password']
    remotepath = ENV[host]['remotepath']
    localpath  = ENV[host]['localpath']
    repo       = ENV['git']['repopath']
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostip , username=name, password=passwd)

    ftp = client.open_sftp()
    ftp.get(remotepath, repo+"/"+localpath)

    client.close()   

def gitAdd(fileName, repoDir):
    cmd = ['git', 'add', fileName]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()

def gitPull(repoDir):
    cmd = ['git', 'pull']
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()

def gitCommit(message, repoDir):
    cmd = ['git', 'commit', '-a', '-m', message]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()

def gitPush(repoDir):
    cmd = ['git', 'push']
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()
    
# in smc.conf must be stored the username+password
def store2git(host):
    repopath=ENV['git']['repopath']
    # try open the repo, if none, then clone
    try:
        # pull
        gitPull(repopath)
        print "[+] get the repo %s"%repopath
        print "[+] pulled"
    except:
        print "error you must clone the repo first,"
        print "execute following commands:\n"
        t=repopath.split('/')
        print "cd %s"%('/'.join(t[:-1]))
        print "git clone %s"%(ENV['git']['remote'])
        print
        sys.exit(-1) 
    
    # commit the file if modified or new
    
    gitCommit("time test commit", repopath)
    print "[+] commited"
    # push
    gitPush(repopath)
    print "[+] pushed"

if __name__ == '__main__':
    loadENV()
    host=ENV.keys()[0]
    print "[+] work on host: %s"%host
    if(ENV[host]['cmd'] == "copy"):
        print "[+] copy"
        get_copy(host)
        print "[+] push on git"
        store2git(host)
    print "[+] all done"
