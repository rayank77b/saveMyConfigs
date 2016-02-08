import paramiko
import os
import sys

debug=True

def log(ok=True, msg='', exit=False):
    '''simple log if the debug is true. '''
    if debug:
        if ok:
            print "[+] %s"%msg
        else:
            print "[-] %s"%msg
    if exit:
        sys.exit(-1)

def _test_path(repo, path):
    '''test if the remote file/directory is existing, 
        if not, create'''
    p=path.split('/')
    if len(p)>1 :
        if not os.path.isdir(repo+"/"+p[0]) :
            log(ok=True, msg="%s does not exists, create it ..."%p[0])
            os.mkdir(repo+"/"+p[0])

def open(hostip, name, passwd):
    ''' open the ssh connection'''
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostip , username=name, password=passwd)
    return client

def cmd(client, cmd):
    '''execute a command on remote ssh server'''
    stdin, stdout, stderr = client.exec_command(cmd)
    errs = stderr.readlines()
    outs = stdout.readlines()
    if len(errs)>0 :
        return True, errs
    else:
        return False, outs

def remove(client, fname):
    '''remove a file, only in /tmp'''
    tokens = fname.split('/')
    if tokens[1] == 'tmp' :
        err, lines = cmd(client, "/bin/rm -f %s"%fname)
        return err, lines
    else:
        return True, ["the file is not in /tmp, we delete only in /tmp! file: %s"%fname]

def tar_c(client, name, directory):
    ''' enter the direcotory and tar a directory to /tmp/name.tgz'''
#    print "tar_c ( client: %s, name: %s, directory: %s)"%(client, name, directory)
    err, lines = cmd(client, "cd %s && /bin/tar zcf /tmp/%s.tgz %s"%(directory, name, name))
#    print err
#    print lines
    return err, lines

def scp_file(ftp, remote, local):
    ''' copy a file '''
    ftp.get(remote, local)
    
def scp(client, paths, repo):
    '''copy files in paths'''
    ftp = client.open_sftp()
    for x in paths:
        remotepath=x['remotepath']
        localpath =x['localpath']
        _test_path(repo, localpath)
        scp_file(ftp, remotepath, repo+"/"+localpath)
