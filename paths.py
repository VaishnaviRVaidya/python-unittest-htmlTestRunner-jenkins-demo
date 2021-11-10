import os
import glob
import subprocess
import re
from subprocess import Popen, PIPE, STDOUT


qspy = 'qspy -u -t'
Make_CMD = 'make'
Clean_CMD = 'make clean'

#Please provide path default python folder for Log

log_file = open(r"C:\Git_repo\app_bbm\Functions\Qu_Test_Log.txt",'a+')
log_file1 = open(r"C:\Git_repo\app_bbm\Functions\Qu_Test_Log2.txt",'w')
print(log_file)

path=r"C:\Git_repo\app_bbm\Functions"   #it takes the all folders in the git_repos
l=os.listdir(path)
#extracts the python files in all the folders of git_repos
g=glob.glob('**/*.py',recursive=True)
for f in g:
    paths=os.path.join(path,f)#joins the path of the folders with the extracted python file folder path
    MyString1 ="Qutest"
    MyString2 ="qutest"
    MyString3 ="quttest"
    if re.search( MyString1, paths ) or re.search( MyString2, paths ) or re.search( MyString3, paths ): #condition to check the only qutest folders which consits of .py files 
        dirname = os.path.dirname(paths)
        a=[dirname]
        print(a)
        for x in a:
            log_file.write(str(x))
            log_file.write("\r")
log_file.close()
lines_seen = set() # holds lines already seen
#checks the duplicate lines from the file and remove it
with open(r"C:\Git_repo\app_bbm\Functions\Qu_Test_Log.txt", "r+") as f:
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i not in lines_seen:
            f.write(i)
            lines_seen.add(i)
    f.truncate()
log_file.close()
with open(r'C:\Git_repo\app_bbm\Functions\Qu_Test_Log.txt') as f:
    Path1 = [line.rstrip('\n') for line in f]
    print(Path1)
##qtest_init = subprocess.Popen(qspy, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
qtest_init = subprocess.Popen('cmd.exe /k qspy -u -t')
print('Qu-Test Initialted')
for i in range(0,len(Path1)):
    os.chdir(Path1[i])
    run = subprocess.Popen(Make_CMD, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = run.stdout
    for x in output:
        print(x)
        log_file1.writelines(str(x))
        log_file1.write("\r")
    run.wait()
    run.terminate()
print('Qu-Test Completed ')
log_file1.close()

