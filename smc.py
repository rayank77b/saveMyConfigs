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
import readConfig
import pc6248

#
ENV={}
C_GIT='git-configs'

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
    hostip     = ENV['ssh-server']['ip']
    name       = ENV['ssh-server']['username']
    passwd     = ENV['ssh-server']['password']
    paths      = ENV[host]['pc6428']
    repo       = ENV[C_GIT]['repopath']
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "[+] connect to %s  user %s"%(hostip, name)
    client.connect(hostip , username=name, password=passwd)
    ftp = client.open_sftp()
    
    print paths
    for x in paths:
        remotepath=x['remotepath']
        localpath =x['localpath']
        test_path(repo, localpath)
        print "[+] copy %s@%s  to %s"%(hostip, remotepath, repo+"/"+localpath)
        ftp.get(remotepath, repo+"/"+localpath)

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
    print "[+] start to get from pc6248  %s..."%host
    if 'ssh-server' in ENV.keys():
        sshenv = ENV['ssh-server']
    else:
        print "ERROR, no ssh-server config found"
        sys.exit(-1)
    hostenv=ENV[host]
    cl = pc6248.PC6248(host, hostenv, sshenv)
    #print cl
    r, msg = cl.login()
    print "[+] ",r, msg
    if r==200:
        r=cl.get_config()
        if r:
            print "[+] OK, get the files"
        else:
            print "[-] Error on getting files from pc6428 %s"%host

if __name__ == '__main__':
    ENV=readConfig.read()
    
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
                add2git(repo, "added config host %s"%host)
    push2git(repo)
    print "[+] all done"



