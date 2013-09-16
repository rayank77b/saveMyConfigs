#!/usr/bin/python
#
# TODO: read configuration(user,pass,what to save)
# TODO: log in ssh
# TODO: get the configs
# TODO: store it on git( clone if not exists, commit, push)

import git
import sys
import paramiko
import ConfigParser

#
ENV={}

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

def store2git(host):
    repopath=ENV['git']['repopath']
    # try open the repo, if none, then clone
    try:
        repo=git.Repo(repopath)
        print "[+] get the repo %s"%repopath
    except git.exc.NoSuchPathError:
        print "error you must clone the repo first,"
        print "execute following commands:\n"
        t=repopath.split('/')
        print "cd %s"%('/'.join(t[:-1]))
        print "git clone %s"%(ENV['git']['remote'])
        print
        sys.exit(-1) 
    origin = repo.remotes.origin
    # pull
    origin.pull()
    print "[+] pulled"
    # commit the file if modified or new
    untracked=repo.untracked_files
    if len(untracked)>0 :
        print "[+] untracked files:"
        for u in untracked:
            print "[+]  %s"%u
        index = repo.index
        index.add(untracked) 
        print "[+] added"
        index.commit("my commit message")
        print "[+] commited"
        # push
        origin.push()
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
