import paramiko

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
        return False, errs
    else:
        return True, outs

def remove(client, fname):
    '''remove a file, only in /tmp'''
    tokens = fname.split('/')
    if tokens[1] == 'tmp' :
        err, lines = _ssh_cmd(client, "/bin/rm -f %s"%fname)
        return err, lines
    else:
        return False, ["the file is not in /tmp, we delete only in /tmp! file: %s"%fname]

def tar_c(client, name, directory):
    ''' enter the direcotory and tar a directory to /tmp/name.tgz'''
    err, lines = _ssh_cmd(client, "cd %s && /bin/tar zcf /tmp/%s.tgz %s"%(directory, name, name))
    return err, lines

def scp(client, paths, repo):
    '''copy files in paths'''
    ftp = client.open_sftp()
    for x in paths:
        remotepath=x['remotepath']
        localpath =x['localpath']
        test_path(repo, localpath)
        log(ok=True, msg="copy %s  to %s"%(remotepath, repo+"/"+localpath))
        ftp.get(remotepath, repo+"/"+localpath)
