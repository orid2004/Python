import os
import sys
import os.path
import whois
import shutil


def setup(project_name):
    if os.path.exists(project_name):
        resetup(project_name)
    else:
        os.makedirs(project_name)
        open(project_name + "/output.txt", "w").close()
        open(project_name + "/whois.txt", "w").close()


def who_input(domain, project_name):
    try:
        info = str(whois.whois(domain))
    except Exception as e:
        print(e)
        info = 'Failed'
    with open(project_name + "/whois.txt", "w") as f:
        f.write(info)


def resetup(project_name):
    ans = str(input(project_name + " exists! Overwrite? (Warning!!) y/n: ")).lower()
    if ans == 'y':
        shutil.rmtree(project_name)
        setup(project_name)
    else:
        sys.exit()
