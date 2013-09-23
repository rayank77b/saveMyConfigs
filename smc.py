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

debug=True

def log(ok=True, msg='', exit=False)
    if debug:
        if ok:
            print "[+] %s"%msg
        else:
            print "[-] %s"%msg
    if exit:
        sys.exit(-1)

def test_path(repo, path):
    """test if the remote file/directory is existing, 
        if not, create"""
    p=path.split('/')
    if len(p)>1 :
        if not os.path.isdir(repo+"/"+p[0]) :
            log(ok=True, msg="%s does not exists, create it ..."%p[0])
            os.mkdir(repo+"/"+p[0])

def get_copy(host):
    log(ok=True, msg="start to copy...")
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
        log(ok=True, msg="copy %s  to %s"%(remotepath, repo+"/"+localpath))
        ftp.get(remotepath, repo+"/"+localpath)

    client.close()
    log(ok=True, msg="copy ok")

def get_copy_remote(host):
    log(ok=True, msg="start to copy...")
    hostip     = ENV[C_SSH]['ipaddress']
    name       = ENV[C_SSH]['username']
    passwd     = ENV[C_SSH]['password']
    paths      = ENV[host]['pc6428']
    repo       = ENV[C_GIT]['repopath']
    
    # it is better if we have temporaer local files
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    log(ok=True, msg="connect to %s  user %s"%(hostip, name))
    client.connect(hostip , username=name, password=passwd)
    ftp = client.open_sftp()
    
    for x in paths:
        remotepath=x['remotepath']
        localpath =x['localpath']
        test_path(repo, localpath)
        log(ok=True, msg="copy %s@%s  to %s"%(hostip, remotepath, repo+"/"+localpath))
        ftp.get(remotepath, repo+"/"+localpath)

    # we must delete the files 
    client.close()
    log(ok=True, msg="copy ok")

def open_repo():
    """ open the repo if exists and pull it"""
    log(ok=True, msg="open repo...")
    repopath=ENV[C_GIT]['repopath']
    # try open the repo, if none, then clone
    try:
        repo=git.Repo(repopath)
        log(ok=True, msg="get the repo %s"%repopath)
        origin = repo.remotes.origin
        # pull
        origin.pull()
        log(ok=True, msg="pulled")
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
    log(ok=True, msg="start to add...")
    repopath=ENV[C_GIT]['repopath']
    # commit the file if modified or new
    gitCommit(msg, repopath)
    log(ok=True, msg="commited (%s)"%msg)

def push2git(repo):
    log(ok=True, msg="start to push...")
    origin = repo.remotes.origin
    origin.push()
    log(ok=True, msg="pushed")

def gitCommit(message, repoDir):
    cmd = ['git', 'add', '.']
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()
    cmd = ['git', 'commit', '-a', '-m', message]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()

def getPC6248(host):
    log(ok=True, msg="start to get from Switch pc6248  %s..."%host)
    if 'ssh-server' in ENV.keys():
        sshenv = ENV['ssh-server']
    else:
        log(ok=False, msg="ERROR, no ssh-server config found", exit=True)
    hostenv=ENV[host]
    cl = pc6248.PC6248(host, hostenv, sshenv)
    r, msg = cl.login()
    log(ok=True, msg="Login ok: ",r, msg)
    if r==200:
        r=cl.get_config()
        if r:
            log(ok=True, msg="OK, get the files")
        else:
            log(ok=False, msg="Error on getting files from pc6428 %s"%host)
    else:
        log(ok=False,  msg="Error on getting files from pc6428 %s"%host)

def getAP541(host):
    log(ok=True, msg="start to get from Access Point ap541  %s..."%host)
    hostenv=ENV[host]
    cl = ap541.AP541(host, hostenv)
    r, msg = cl.login()
    log(ok=True, msg="Login ok: %d %s"%(r, msg))
    if r==200:
        r=cl.get_config()
        if r:
            log(ok=True, msg="OK, get the files")
        else:
            log(ok=False,  msg="Error on getting files from ap541 %s"%host
    else:
        log(ok=False,  msg="Error on getting files from ap541 %s"%host

def move_local(host, how, nr):
    log(ok=True, msg="move local file...")
    repo     = ENV[C_GIT]['repopath']
    fromfile = ENV[host][how][nr]['remotepath']
    tofile   = repo+"/"+ENV[host][how][nr]['localpath']
    log(ok=True, msg="move local file from %s to %s ..."%(fromfile, tofile))
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
    if !options.verbose:
        debug=True
    
    log(ok=True, msg="read configuration...")
    ENV = readConfig.read(configpath=configfile)
    #readConfig.printOut(ENV)
    
    repo=open_repo()
    
    for host in ENV.keys():
        if host != C_GIT:
            log(ok=True, msg="work on host: %s"%host)
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
    log(ok=True, msg="all done")



