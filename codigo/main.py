# Brief: Mainscript which starts the pseudo SO 
# Author: Alexandre Kaihara, Pedro, Higor Santos and Davi Dupin
# cd C:\Users\Kaihara\Desktop\FSO-PSEUDO-SO\codigo
# python main.py input/test/processes.txt input/test/files.txt
# python main.py input/aging/processes.txt input/aging/files.txt

from sys import argv
from threading import Thread
from pseudoOS import PseudoOS
from variaveisglobais import *


def main():
    try:
        argv[1]
        argv[2]
    except:
        print("To start the operational system, type the path to the processes file (PFILE)\
             and the memory file (MFILE) as follows:\npython main.py [PFILE] [MFILE]")
        return 0
    
    os = PseudoOS(argv[1], argv[2])
    
    threads = []
    threads.append(Thread(target=os.create_processes))
    threads.append(Thread(target=os.scheduler))

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]    
    
    os.ArchiveMan.print_file_log()
    os.ArchiveMan.print_memory_occupation()
    print("** Ending execution of Pseudo Operational System")

if __name__ == "__main__":
    main()