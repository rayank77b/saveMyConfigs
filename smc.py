#!/usr/bin/python
#
# Author  = Andrej Frank, IT-Designers GmbH, STZ Softwaretechnik
# Version = 0.0.1 Alpha
# GNU GENERAL PUBLIC LICENSE
# 
# what we do:
# - read configuration(user,pass,what to save, where to save)
# - get the config from switchs
# - log in ssh, get the configs
# - store it on git( clone if not exists, commit, push)
#
# at moment is it alpha and the error handling is very bad (like my english ;)

import git
import subprocess
import sys, os
import shutil
import paramiko
from optparse import OptionParser

import readConfig
import pc6248
import ap541

ENV={}
C_GIT='git-configs'
C_SSH='ssh-server'

def test_path(repo, path):
    """test if the remote file/directory is existing, 
        if not, create"""
    p=path.split('/')
    if len(p)>1 :
        if not os.path.isdir(repo+"/"+p[0]) :
            print "[+] %s does not exists, create it ..."%p[0]
            os.mkdir(repo+"/"+p[0])

def get_copy(host):
    print "[+] start to copy..."
    hostip     = ENV[host]['ipaddress']
    name       = ENV[host]['username']
    passwd     = ENV[host]['password']
    paths      = ENV[host]['file']
    repo       = ENV[C_GIT]['repopath']
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostip , username=name, password=passwd)
    ftp = client.open_sftp()
    
    for x in paths:
        remotepath=x['remotepath']
        localpath =x['localpath']
        test_path(repo, localpath)
        print "[+] copy %s  to %s"%(remotepath, repo+"/"+localpath)
        ftp.get(remotepath, repo+"/"+localpath)

    client.close()
    print "[+] copy ok"

def get_copy_remote(host):
    print "[+] start to copy..."
    hostip     = ENV[C_SSH]['ipaddress']
    name       = ENV[C_SSH]['username']
    passwd     = ENV[C_SSH]['password']
    paths      = ENV[host]['pc6428']
    repo       = ENV[C_GIT]['repopath']
    
    # it is better if we have temporaer local files
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "[+] connect to %s  user %s"%(hostip, name)
    client.connect(hostip , username=name, password=passwd)
    ftp = client.open_sftp()
    
    for x in paths:
        remotepath=x['remotepath']
        localpath =x['localpath']
        test_path(repo, localpath)
        print "[+] copy %s@%s  to %s"%(hostip, remotepath, repo+"/"+localpath)
        ftp.get(remotepath, repo+"/"+localpath)

    # we must delete the files 
    client.close()
    print "[+] copy ok"

def open_repo():
    """ open the repo if exists and pull it"""
    print "[+] open repo..."
    repopath=ENV[C_GIT]['repopath']
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
        print "  cd %s"%('/'.join(t[:-1]))
        print "  git clone %s"%(ENV[C_GIT]['remote'])
        print
        print "and you must set the username:password in .git/config url"
        print "we dont handle username:password yet\n"
        sys.exit(-1)

def add2git(repo, msg):
    print "[+] start to add..."
    repopath=ENV[C_GIT]['repopath']
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

def getPC6248(host):
    print "[+] start to get from Switch pc6248  %s..."%host
    if 'ssh-server' in ENV.keys():
        sshenv = ENV['ssh-server']
    else:
        print "ERROR, no ssh-server config found"
        sys.exit(-1)
    hostenv=ENV[host]
    cl = pc6248.PC6248(host, hostenv, sshenv)
    #print cl
    r, msg = cl.login()
    print "[+] Login ok: ",r, msg
    if r==200:
        r=cl.get_config()
        if r:
            print "[+] OK, get the files"
        else:
            print "[-] Error on getting files from pc6428 %s"%host
    else:
        print "[-] Error on getting files from pc6428 %s"%host

def getAP541(host):
    print "[+] start to get from Access Point ap541  %s..."%host
    hostenv=ENV[host]
    cl = ap541.AP541(host, hostenv)
    #print cl
    r, msg = cl.login()
    print "[+] Login ok: ",r, msg
    if r==200:
        r=cl.get_config()
        if r:
            print "[+] OK, get the files"
        else:
            print "[-] Error on getting files from ap541 %s"%host
    else:
        print "[-] Error on getting files from ap541 %s"%host

def move_local(host, how, nr):
    print "[+] move local file..."
    repo     = ENV[C_GIT]['repopath']
    fromfile = ENV[host][how][nr]['remotepath']
    tofile   = repo+"/"+ENV[host][how][nr]['localpath']
    print "[+] move local file from %s to %s ..."%(fromfile, tofile)
    shutil.move(fromfile, tofile)
    

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-c", "--config", dest="config",
                  help="get the config file", metavar="FILE")
    parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    configfile=''
    if options.config==None:
        sys.stderr.write('ERROR:   please give a configuration file (see -h)\n')
        sys.exit(-1)
    else:
        configfile=options.config
        if not os.path.isfile(configfile):
            sys.stderr.write('ERROR:   can\'t open the file\n')
            sys.exit(-1)

    print "[+] read configuration..."
    ENV=readConfig.read(configpath=configfile)
    readConfig.printOut(ENV)
    sys.exit(0)
    repo=open_repo()
    
    for host in ENV.keys():
        if host != C_GIT:
            print "[+] work on host: %s"%host
            if 'file' in ENV[host].keys():
                get_copy(host)
                add2git(repo, "added config host %s"%host)
            if 'pc6428' in ENV[host].keys():
                getPC6248(host)
                get_copy_remote(host)
                add2git(repo, "added pc6248 config from host %s"%host)
            if 'ap541' in ENV[host].keys():
                getAP541(host)
                move_local(host, 'ap541', 0)
                add2git(repo, "added AP541 config.xml from host %s"%host)
    push2git(repo)
    print "[+] all done"



