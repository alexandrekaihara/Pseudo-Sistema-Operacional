# Brief: Mainscript which starts the pseudo SO 
# Author: Alexandre Kaihara and Pedro

import sys
import threading
from variaveisglobais import *
from arquivo import ArchiveManager
from memoria import MemoryManager
from processos import ProcessManager
from recurso import ResourceManager
from fila import QueueManager
from datetime import date, datetime
from time import sleep


class PseudoOS():
    # Brief: 
    #   Starts all modules
    # Param:
    # Return: 
    def __init__(self, process_path: str, memory_path: str) -> None:
        self.ArchiveMan = ArchiveManager(memory_path)
        self.MemoryMan = MemoryManager()
        self.ProcessMan = ProcessManager()
        self.QueueMan = QueueManager()
        self.ResourcesMan = ResourceManager()
        self.processes = []
        self.read_processes(process_path)
        self.current_time = datetime.now()
        self.enqueue_process = []
        self.quantum = 1
        print("** Initializing all resources")

    # Brief: 
    #   Thread for starting all processes on due time
    # Param:
    # Return: 
    def create_processes(self) -> None:
        print("** Starting Pseudo Operating System")
        for p in self.processes:
            # Define the sleep duration
            delta = datetime.now() - self.current_time
            wait = p[0] - delta.seconds + delta.microseconds/1000000
            sleep(wait)
            
            # Create process if possible
            id = self.ProcessMan.get_next_process_id()
            code = self.MemoryMan.load(id, p[3])
            if code != NOT_ENOUGH_RAM_MEMORY:
                id = self.ProcessMan.create(p[1], p[2], p[3], p[4], p[5], p[6], p[7])

            # Insert on queue to be executed
            self.QueueMan.insert(id, p[1])

    # Brief: 
    #   Thread for defining the next process to be executed
    # Param:
    # Return: 
    def scheduler(self) -> None:
        while True:
            # Reinsert blocked processess into the ready queue
            [self.QueueMan.insert(id, priority) for (id, priority) in self.ResourcesMan.get_buffer()]

            # Check which is the next process to be run
            id = self.QueueMan.next_process()
            # If there is next process
            if id != NO_NEXT_PROCESS:
                # As this process will be executed, must leave the ready queue
                self.QueueMan.remove(id)
                pr = self.ProcessMan.get_process(id)

                # Execute till the end if is a real time process, else, execute a quantum
                end = [0]
                if pr.priority == 0:
                    resourcecode = pr.run(pr.processor_time, self.ArchiveMan, end)
                else:
                    resourcecode = pr.run(self.quantum, self.ArchiveMan, end)
                
                # If the process has finished, so it has to free the memory occupied by the process
                if end[0] == PROCESS_FINISHED:
                    self.MemoryMan.remove(id, pr.mem_allocated)
                # If the running process not requested a resource, must get back to the ready queue, else, it must create a request
                elif resourcecode == NO_RESOURCE_REQUEST:
                    self.QueueMan.insert(id, pr.priority)
                else:
                    t = threading.Thread(target=self.resource_request, args=(resourcecode, id, pr.priority))
                    t.start()
            # If there is no more next processes and no more processes to be created, and no
            elif len(self.processes) == 0:
                break

    # Brief: 
    #   Thread for requesting a resource
    # Param:
    #   code: integer that identifies the resource to be requested
    #   processID: Process identification
    #   priority: Priority of the process
    # Return: 
    #   None
    def resource_request(self, code: int, processID: int, priority: int) -> None:
        if code == SCANNER_RESOURCE_REQUESTED:
            self.ResourcesMan.get_scanner(processID, priority)
        elif code == PRINTER_RESOURCE_REQUESTED:
            self.ResourcesMan.get_printer(processID, priority)
        elif code == MODEM_RESOURCE_REQUESTED:
            self.ResourcesMan.get_modem(processID, priority)
        elif code == SATA_RESOURCE_REQUESTED:
            self.ResourcesMan.get_sata(processID, priority)

    # Brief: 
    #   Read the processes file
    # Param:
    #   path: path to the file
    # Return: 
    #   None
    def read_processes(self, path: str) -> None:  
        # Separate by line
        with open(path, 'r') as file:
            [self.processes.append(line.split(', ')) for line in file]
        # Convert string to integer
        for i in range(len(self.processes)):
            self.processes[i] = [int(item.strip("\n")) for item in self.processes[i]]
        # Verify if every line on the file has 8 elements
        if sum([1 for line in self.processes if len(line) != 8]) != 0:
            raise Exception("Wrong file or incorrect file content")



def main():
    try:
        sys.argv[1]
        sys.argv[2]
    except:
        print("To start the operational system, type the path to the processes file (PFILE) and the memory file (MFILE) as follows:\npython main.py [PFILE] [MFILE]")
        return 0
    os = PseudoOS(sys.argv[1], sys.argv[2])
    
    threads = []
    threads.append(threading.Thread(target=os.create_processes))
    threads.append(threading.Thread(target=os.scheduler))

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


if __name__ == "__main__":
    main()