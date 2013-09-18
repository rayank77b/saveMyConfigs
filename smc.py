#!/usr/bin/python
#
# TODO: read configuration(user,pass,what to save)
# TODO: log in ssh
# TODO: get the configs
# TODO: store it on git( clone if not exists, commit, push)

import git
import subprocess
import sys, os
import paramiko
import ConfigParser

#
ENV={}

# simple ini file
def loadENV(configpath='smc.conf'):
    print "[+] load configs..."
    config = ConfigParser.RawConfigParser()
    config.read(configpath)
    sections = config.sections()
    for section in sections:
        ENV[section]={}
        for x in config.options(section):
            ENV[section][x]=config.get(section, x)
    print "[+] load configs done"

def test_path(repo, path):
    """test if the remote file/directory is existing, 
        if not, create"""
    p=path.split('/')
    if len(p)>1 :
        if not os.path.isdir(repo+"/"+p[0]) :
            os.mkdir(repo+"/"+p[0])

def get_copy(host):
    print "[+] start to copy..."
    hostip     = ENV[host]['ipaddress']
    name       = ENV[host]['username']
    passwd     = ENV[host]['password']
    remotepath = ENV[host]['remotepath']
    localpath  = ENV[host]['localpath']
    repo       = ENV['git']['repopath']
     
    test_path(repo, localpath)
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostip , username=name, password=passwd)

    ftp = client.open_sftp()
    ftp.get(remotepath, repo+"/"+localpath)

    client.close()
    print "[+] copieng ended"

def open_repo():
    """ open the repo if exists and pull it"""
    print "[+] open repo..."
    repopath=ENV['git']['repopath']
    # try open the repo, if none, then clone
    try:
        repo=git.Repo(repopath)
        print "[+] get the repo %s"%repopath
        origin = repo.remotes.origin
        # pull
        origin.pull()
        print "[+] pulled"
        return repo
    except git.exc.NoSuchPathError:
        print "error you must clone the repo first,"
        print "execute following commands:\n"
        t=repopath.split('/')
        print "cd %s"%('/'.join(t[:-1]))
        print "git clone %s"%(ENV['git']['remote'])
        print
        sys.exit(-1)

def add2git(repo, msg):
    print "[+] start to add..."
    repopath=ENV['git']['repopath']
    # commit the file if modified or new
    gitCommit(msg, repopath)
    print "[+] commited (%s)"%msg

def push2git(repo):
    print "[+] start to push..."
    origin = repo.remotes.origin
    origin.push()
    print "[+] pushed"     

def gitCommit(message, repoDir):
    cmd = ['git', 'add', '.']
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()
    cmd = ['git', 'commit', '-a', '-m', message]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()

if __name__ == '__main__':
    loadENV()
    
    repo=open_repo()
    
    for host in ENV.keys():
        if host != 'git':
            print "[+] work on host: %s"%host
            if(ENV[host]['cmd'] == "file"):
                get_copy(host)
                add2git(repo, "added config host %s"%host)
    
    push2git(repo)
    print "[+] all done"



