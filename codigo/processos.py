# Brief: Define the structure and data of the processes
# Author: Alexandre Kaihara and Pedro


from typing import Tuple
from variaveisglobais import *
from arquivo import ArchiveManager
from datetime import datetime
from time import sleep

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
    #   offset: offset on RAM memory allocated for the process
    #   archive_op = a list of all archive operations to be executed
    # Return: 
    #   None
    def __init__(self, processID: int, priority: int, processor_time: int, mem_allocated: int, printer: bool, scanner: bool, modem: bool, driver: bool, offset: int, archive_op: list) -> None:
        self.processID = processID
        self.priority = priority
        self.processor_time = processor_time
        self.offset = offset
        self.mem_allocated = mem_allocated
        self.instruction_counter = 1
        self.to_do = []
        self.create_to_do_list(printer, scanner, modem, driver, archive_op)
        self.print_creation(printer, scanner, modem, driver)

    # Brief: 
    #   Creates the relation of all actions to do
    # Param:
    # Return: 
    def create_to_do_list(self, printer, scanner, modem, driver, archive_op) -> None:
        if printer != 0:    self.to_do.append([RESOURCE_ACTION, PRINTER_RESOURCE_REQUESTED])
        if scanner != 0:    self.to_do.append([RESOURCE_ACTION, SCANNER_RESOURCE_REQUESTED])
        if modem != 0:      self.to_do.append([RESOURCE_ACTION, MODEM_RESOURCE_REQUESTED])
        if driver != 0:     self.to_do.append([RESOURCE_ACTION, SATA_RESOURCE_REQUESTED])
        [self.to_do.append([ARCHIVE_ACTION, archive_op.pop(0)]) for _ in range(len(archive_op))]
            
    # Brief: 
    #   Must execute the process, create files, delete, acess resources, etc... for "time" seconds, then return execution 
    #   OBS: If the process needs a resource (printer, scanner, etc) it returns either 
    #   NO_RESOURCE_REQUEST, SCANNER_RESOURCE_REQUESTED, PRINTER_RESOURCE_REQUESTED, MODEM_RESOURCE_REQUESTED, SATA_RESOURCE_REQUESTED
    # Param:
    #   time = number of seconds to be executed
    #   ArchiveM: Instance of the Archive Manager to access directly the archives
    # Return: 
    #   Return the code if the process ended (PROCESS_FINISHED) or not requested a resource (NO_RESOURCE_REQUEST) or 
    #   if it needs a resouce, so it should return some of these codes SCANNER_RESOURCE_REQUESTED, PRINTER_RESOURCE_REQUESTED, MODEM_RESOURCE_REQUESTED, SATA_RESOURCE_REQUESTED
    def run(self, time: int, ArchiveM: ArchiveManager) -> int:
        print("process", self.processID , "=>")
        print("P" + str(self.processID), "STARTED")

        # Execute instructions
        for i in range(time):
            # Instruction with duration of 1 second
            remaining_time = 1
            start = datetime.now()
            while remaining_time > 0:
                
                if len(self.to_do) > 0:
                    task = self.to_do.pop(0)

                    # If needs some resource, let the system make the request, return the appropriate code
                    if task[0] == RESOURCE_ACTION:
                        return task[1]
                    # If needs some archive operation, let the archive module handle
                    elif task[0] == ARCHIVE_ACTION:
                        op = task[1]
                        if op[1] == CREATE_FILE_REQUEST:
                            ArchiveM.createfile(self.processID, op[2], op[3])
                        elif op[1] == DELETE_FILE_REQUEST:
                            ArchiveM.deletefile(self.processID, op[2], self.priority == 0)
                remaining_time = 1 - diff_time(datetime.now(), start)
            
            # End of an instruction
            print("P" + str(self.processID), "instruction", self.instruction_counter)
            if self.instruction_counter >= self.processor_time:
                print("P" + str(self.processID),  "return SIGINT", "\n")
                return PROCESS_FINISHED  
            self.instruction_counter += 1
        print("\n")
        return NO_RESOURCE_REQUEST     
                

    # Brief: 
    #   Must print the characteristics of the process on creation
    # Param:
    # Return: 
    #   None
    def print_creation(self, printer, scanner, modem, driver) -> None:
        print("dispatcher =>")
        print("    PID:     \t", self.processID)
        print("    offset:  \t", self.offset)
        print("    blocks:  \t", self.mem_allocated)
        print("    priority:\t", self.priority)
        print("    time:    \t", self.processor_time)
        print("    printers:\t", printer)
        print("    canners: \t", scanner)
        print("    modems:  \t", modem)
        print("    drives:  \t", driver, "\n")


class ProcessManager():
    # Brief: 
    #   Defines the structure of the processes
    #   OBS: All methods which share some variable, must use locks
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
    #   printer: Code of the requested printer
    #   scanner: If there is a requisition on the scanner
    #   driver: Code of the requested driver
    #   offet: offset of the RAM memory in which the process was allocated
    #   archive_op = a list of all archive operations to be executed
    # Return: 
    #   return id of the new process
    def create(self, priority: int, processor_time: int, mem_allocated: int, printer: int, scanner: bool, modem: bool, driver: int, offset: int, archive_op: list) -> int:
        new_id = self.last_given_id + 1
        print("** Created process", new_id, "\n")
        self.__processes[new_id] = Process(new_id, priority, processor_time, mem_allocated, printer, scanner, modem, driver, offset, archive_op)
        self.last_given_id = new_id
        return new_id

    # Brief: 
    #   Deletes a process from list
    # Param:
    #   processID: Id of the process to be deleted
    # Return: 
    #   None
    def delete(self, processID: int) -> None:
        print("** Deleted process with id", processID, "\n")
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
    
    # Brief: 
    #   Returns the number of active processes
    # Param:
    # Return: 
    #   Return the next id to be given
    def num_active_processes(self):
        return len(self.__processes)