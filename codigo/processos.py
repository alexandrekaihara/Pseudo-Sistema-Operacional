# Brief: Define the structure and data of the processes
# Author: Alexandre Kaihara and Pedro


from typing import Tuple
from variaveisglobais import *
from arquivo import ArchiveManager

'''
Módulo de Processos – classes e estruturas de dados relativas ao processo. Basicamente,
mantém informações específicas do processo.
'''


class Process():
    # Brief: 
    #   Initiate all process values
    # Param:
    #   processID: The id that represents the process
    #   priority: Priority of the process
    #   processor_time: Processor time required to execute the whole process
    #   mem_allocated: Total amouunt of memory needed to store all program
    #   printer: If there is a requisition on the printer
    #   scanner: If there is a requisition on the scanner
    #   modem = If there is a requisition on the modem
    #   driver: If there is a requisition on the driver
    # Return: 
    #   None
    def __init__(self, processID: int, priority: int, processor_time: int, mem_allocated: int, printer: bool, scanner: bool, modem: bool, driver: bool) -> None:
        self.processID = processID
        self.priority = priority
        self.processor_time = processor_time
        self.offset = 0
        self.mem_allocated = mem_allocated
        self.printer = printer
        self.scanner = scanner
        self.modem = modem
        self.driver = driver
        self.print_creation()

    # Brief: 
    #   Must execute the process, create files, delete, acess resources, etc... for "time" seconds, then return execution 
    #   OBS: If the process needs a resource (printer, scanner, etc) it returns either 
    #   NO_RESOURCE_REQUEST, SCANNER_RESOURCE_REQUESTED, PRINTER_RESOURCE_REQUESTED, MODEM_RESOURCE_REQUESTED, SATA_RESOURCE_REQUESTED
    # Param:
    #   time = number of seconds to be executed
    #   ArchiveM: Instance of the Archive Manager to access directly the archives
    #   end: Contains one element which has a code that indicates if the process has finished (PROCESS_FINISHED) or not
    # Return: 
    #   Return the code if it requested a resource () or not
    def run(self, time: int, ArchiveM: ArchiveManager, end: list) -> int:
        print("process ", self.processID, " =>")
        print("P", self.processID, " STARTED")

        '''Implementar'''
        
        return NO_RESOURCE_REQUEST       
        print("P", self.processID, " return SIGINT")

    # Brief: 
    #   Must print the characteristics of the process on creation
    # Param:
    # Return: 
    #   None
    def print_creation(self) -> None:
        print("dispatcher =>")
        print("    PID:     \t", self.processID)
        print("    offset:  \t", self.offset)
        print("    blocks:  \t", self.mem_allocated)
        print("    priority:\t", self.offset)
        print("    time:    \t", self.processor_time)
        print("    printers:\t", self.printer)
        print("    canners: \t", self.scanner)
        print("    modems:  \t", self.modem)
        print("    drives:  \t", self.driver, "\n")


class ProcessManager():
    # Brief: 
    #   Defines the structure of the processes
    # Param:
    # Return: 
    #   None
    def __init__(self) -> None:
        # Dictionary using its processID as the key
        self.__processes = {}
        self.last_given_id = -1

    # Brief: 
    #   Create a process
    # Param:
    #   priority: Priority of the process
    #   processor_time: Processor time required to execute the whole process
    #   mem_allocated: Total amouunt of memory needed to store all program
    #   printer: If there is a requisition on the printer
    #   scanner: If there is a requisition on the scanner
    #   driver: If there is a requisition on the driver
    # Return: 
    #   return id of the new process
    def create(self, priority: int, processor_time: int, offset: int, mem_allocated: int, printer: bool, scanner: bool, driver: bool) -> int:
        new_id = self.last_given_id + 1
        self.__processes[new_id] = Process(new_id, priority, processor_time, offset, mem_allocated, printer, scanner, driver)
        self.last_given_id = new_id
        return new_id

    # Brief: 
    #   Deletes a process from list
    # Param:
    #   processID: Id of the process to be deleted
    # Return: 
    #   None
    def delete(self, processID: int) -> None:
        self.__processes.pop(processID)

    # Brief: 
    #   Get a existing process
    # Param:
    #   processID: Id of the process to be returned
    # Return: 
    #   Return a instance of a existing process
    def get_process(self, processID: int) -> Process:
        return self.__processes[processID]

    # Brief: 
    #   Returns the next process id
    # Param:
    # Return: 
    #   Return the next id to be given
    def get_next_process_id(self) -> int:
        return self.last_given_id + 1
    

