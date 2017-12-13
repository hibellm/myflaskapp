# https://www.adampalmer.me/iodigitalsec/2014/11/23/ssh-sftp-paramiko-python/
# https://codereview.stackexchange.com/questions/127180/finding-all-non-empty-directories-and-their-files-on-an-sftp-server-with-paramik
import paramiko
import stat
from collections import defaultdict
import os
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('moveit.accenture.com', username='TCRomh01', password='3hEjc1T1')
except paramiko.SSHException:
    print ("Connection Error")
sftp = ssh.open_sftp()
#sftp.chdir("/SDTM Conversion Library/Converted Studies/")


def recursive_ftp(sftp, path='/SDTM Conversion Library/Converted Studies/', files=None):
    if files is None:
        files = defaultdict(list)
        #print('nothing')

    # loop over list of SFTPAttributes (files with modes)
    for attr in sftp.listdir_attr(path):

        if stat.S_ISDIR(attr.st_mode):
            # If the file is a directory, recurse it
            recursive_ftp(sftp, os.path.join(path,attr.filename), files) #WORKS


        else:
            #  if the file is a file, add it to our dict
            files[path].append(attr.filename)

    return files

files = recursive_ftp(sftp)
#print(files)
x=dict.items(files)
print(x)


#with open('myfile.txt', 'w') as f:
#    for key, value in x():
#        f.write('%s:%s\n' % (key, value))

ssh.close()
