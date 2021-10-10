# Brief: Pseudo-SO program 
# Author: Alexandre Kaihara and Pedro

from variaveisglobais import *
from arquivo import ArchiveManager
from memoria import MemoryManager
from processos import ProcessManager
from recurso import ResourceManager
from fila import QueueManager

from threading import Thread
from datetime import datetime
from time import sleep


class PseudoOS():
    # Brief: 
    #   Starts all modules
    # Param:
    # Return: 
    def __init__(self, process_path: str, memory_path: str) -> None:
        # Read all input files
        self.done = 0           # flag that indicates that there is no more processes to be created
        self.processes = []
        self.archive_op = {}
        self.memory_load = []
        self.memory_size = 0
        self.read_processes(process_path)
        self.read_archive(memory_path)

        # System variables
        print("** Initializing all resources")
        self.current_time = datetime.now()
        self.enqueue_process = []
        self.quantum = 1
        self.ArchiveMan = ArchiveManager(self.memory_load)
        self.MemoryMan  = MemoryManager()
        self.ProcessMan = ProcessManager()
        self.QueueMan   = QueueManager()
        self.ResourcesMan = ResourceManager()

    # Brief: 
    #   Thread for defining the next process to be executed
    # Param:
    # Return: 
    def scheduler(self) -> None:
        while self.ProcessMan.num_active_processes() > 0 or self.done != PROCESS_CREATION_FINISHED:
            # Reinsert blocked processess into the ready queue
            [self.QueueMan.insert(id, priority) for (id, priority) in self.ResourcesMan.get_buffer()]

            # Check which is the next process to be run, if there is a process it is removed from queue
            id = self.QueueMan.next_process()
            # If there is next process
            if id != NO_NEXT_PROCESS:
                # Get instance of Process
                pr = self.ProcessMan.get_process(id)

                # Execute till the end if is a real time process, else, execute a quantum
                if pr.priority == 0:
                    duration = pr.processor_time
                else:
                    duration = self.quantum
                code = pr.run(duration, self.ArchiveMan)
                
                # If the process has finished, so it has to free the memory occupied by the process
                if code == PROCESS_FINISHED:
                    self.MemoryMan.remove(id, pr.mem_allocated, pr.offset)
                    self.ProcessMan.delete(id)
                # If the running process not requested a resource, must get back to the ready queue
                elif code == NO_RESOURCE_REQUEST:
                    self.QueueMan.insert(id, pr.priority)
                # Else, a source was requested, then the system creates a thread to handle it
                else:
                    t = Thread(target=self.resource_request, args=(code, id, pr.priority))
                    t.start()

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
            offset = [0]
            id = self.ProcessMan.get_next_process_id()
            code = self.MemoryMan.load(id, p[3], offset)
            if code != NOT_ENOUGH_RAM_MEMORY:
                id = self.ProcessMan.create(p[1], p[2], p[3], p[4], p[5], p[6], p[7], offset[0], self.archive_op[id])

            # Insert on queue to be executed
            self.QueueMan.insert(id, p[1])
        self.done = PROCESS_CREATION_FINISHED

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

    # Brief: 
    #   Read the archive file
    # Param:
    #   path: path to the file
    # Return: 
    #   None
    def read_archive(self, path: str) -> None:
        lines = tuple(open(path, 'r'))
        lines = [line.strip('\n') for line in lines]
        self.memory_size = int(lines.pop(0))
        numberoffiles = int(lines.pop(0))
        # Convert char integers to integer
        for i in range(len(lines)):
            lines[i] = lines[i].split(', ')
            lines[i] = [int(item) if item.isnumeric() else item for item in lines[i]] 
        [self.memory_load.append(lines.pop(0)) for _ in range(numberoffiles)]
        operations = [lines.pop(0) for _ in range(len(lines))]
        for op in operations:
            self.archive_op[op[0]] = []
        for op in operations:
            self.archive_op[op[0]].append(op)
        
    
            
