#!/usr/bin/python

import ConfigParser


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
    print "[+] load configs done"
    return r

if __name__ == '__main__':
    ENV={}
    ENV=read()
    print ENV
    print
    for k in ENV:
        print k
    print
    for k in ENV:
        for x in ENV[k]:
            print k.ljust(12), ": ", x.ljust(12), " : ", ENV[k][x]

