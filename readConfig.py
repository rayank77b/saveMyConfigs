#!/usr/bin/python
#
# Author  = Andrej Frank, IT-Designers GmbH, STZ Softwaretechnik
# Version = 0.0.1 Alpha
# GNU GENERAL PUBLIC LICENSE
# 
# read and parse our config, to a python dictionary
# we use simple INI-File

import sys
import ConfigParser

C_GIT='git-configs'
C_SSH='ssh-server'

# simple ini file
def read(configpath='smc.conf'):
    r={}
    print "[+] load configs..."
    config = ConfigParser.RawConfigParser()
    config.read(configpath)
    for section in config.sections():
        if 'git-configs' == section :
            r[section]={}
            for x in config.options(section):
                r[section][x]=config.get(section, x)
        if 'ssh-server' == section :
            r[section]={}
            for x in config.options(section):
                r[section][x]=config.get(section, x)
        if 'host-' in section:
            host = config.get(section, 'host')
            if not host in r.keys():  
                r[host]={}
            for x in ('ipaddress','username', 'password'):
                r[host][x]=config.get(section, x)
        if 'file-' in section:
            host = config.get(section, 'host')
            if not host in r.keys():  
                r[host]={}
            f={}
            for x in ('remotepath','localpath'):
                f[x]=config.get(section, x)
            if not 'file' in r[host].keys():
                r[host]['file']=[]
            r[host]['file'].append(f)
        if 'pc6428-' in section:
            host = config.get(section, 'host')
            if not host in r.keys():  
                r[host]={}
            f={}
            for x in ('remotepath','localpath'):
                f[x]=config.get(section, x)
            if not 'pc6428' in r[host].keys():
                r[host]['pc6428']=[]
            r[host]['pc6428'].append(f)
        if 'ap541-' in section:
            host = config.get(section, 'host')
            if not host in r.keys():  
                r[host]={}
            f={}
            for x in ('remotepath','localpath'):
                f[x]=config.get(section, x)
            if not 'ap541' in r[host].keys():
                r[host]['ap541']=[]
            r[host]['ap541'].append(f)
    print "[+] verificate config"
    _verificate(r)
    return r

def _error(msg):
    sys.stderr.write('ERROR in verificate configuration\n')
    sys.stderr.write('  '+msg+'\n')
    sys.exit(-1)

def _verificate(e):
    if not C_GIT in e.keys():
        _error("No Git configuration found")
    if not C_SSH in e.keys():
        _error("No SSH configuration found")
    for host in e:
        if C_GIT in host:
            for x in ('username', 'repopath', 'password', 'remote'):
                if not x in e[host].keys():
                    _error("missing parameter in git config: %s"%x)
        elif C_SSH in host:
            for x in ('username','password','ipaddress'):
                if not x in e[host].keys():
                    _error("missing parameter in ssh config: %s"%x)
        else:
            for x in ('username','password','ipaddress'):
                if not x in e[host].keys():
                    _error("missing parameter in host %s config: %s"%(host,x))
            if len(e[host])<4:
                _error("there is no command in host or something wrong")

def printOut(env):
    print env
    print
    for k in env:
        print k
    print
    for k in env:
        for x in env[k]:
            print k.ljust(22), ": ", x.ljust(12), " : ", env[k][x]

if __name__ == '__main__':
    ENV=read(configpath='smc.conf.example')
    printOut(ENV)

