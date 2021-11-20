# Brief: Contains all implementation and rules related to creating and deleting files
# Author: Davi Dupin

from variaveisglobais import *


class ArchiveManager():
    # Brief: 
    #   Must read the file and load it on memory
    # Param:
    #   path: String containing the path to the file   
    # Return: 
    #   None
    def __init__(self, memoryload: list, memory_size: int) -> None:
        self.filemanagerlog = []
        self.existing_files = {}
        self.archive = [{}] * memory_size
        self.load_memory(memoryload)

    # Brief: 
    #   Verify using first-fit a contiguous available memmory free and create file.
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    #   filesize: Integer containing the number of blocks to be allocated
    # Return: 
    #   Returns integer which is a code if the file succeded of failed. If succeed on creating, return CREATE_FILE_SUCESS
    def createfile(self, processID: int, filename: str, filesize: int, priority: int) -> int:
        filesize = int(filesize)
        print("** Process", processID, " creating a file named", filename, "\n")
        # Check if the file name and user already exists
        keys = self.existing_files.keys()
        if (processID, filename) in keys or (-1, filename) in keys:
            return self.register_operation(processID, filename, CREATE_FILE_NAME_IN_USE, offset= (-1), filesize=filesize)
        
        # Iterate over all memory to check the first contiguous space to store a new file
        i: int = 0
        count = 0  
        while(i < len(self.archive)):
            if (self.archive[i] != {}):
                if(count >= filesize):
                    self.__alocate(filename, filesize, processID, (i-count), priority)
                    self.existing_files[(processID, filename)] = (i-count, filesize)
                    return self.register_operation(processID, filename, CREATE_FILE_SUCESS, offset= (i-count), filesize=filesize)
                count = 0
            else:
                count+=1
            i+=1
        if(count >= filesize):
            self.__alocate(filename, filesize, processID, (i-count), priority)
            self.existing_files[(processID, filename)] = (i-count, filesize)
            return self.register_operation(processID, filename, CREATE_FILE_SUCESS, offset= (i-count), filesize=filesize)
        return self.register_operation(processID, filename, CREATE_FILE_NOT_ENOUGTH_MEM)
    
    def __alocate(self, filename: str, size: int, processId: int, offset: int, priority: int) -> None:
        while(size>0):
            self.archive[offset + size - 1] = {"process_id": processId, "filename": filename, "priority": priority}
            size -= 1
    
    # Brief: 
    #   Verify if given file exists on memory, if so, then delete it.
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def deletefile(self, processID: int, filename: str, isRealTime) -> int:
        print("** Process", processID, " deleting a file named", filename, "\n")
        offset =-1
        size =0
        for i in range(len(self.archive)):
            file = self.archive[i]
            if( file != {}):
                if(file["filename"] == filename):
                    offset = i if offset == -1 else offset
                    # if is a real-time process it can delete any file
                    if isRealTime:
                        size +=1
                        self.archive[i] = {}
                    # If is not real-time, if the file was not created by a realtime or has no owner
                    elif(file["priority"] > 0 or file["process_id"] == -1):
                        size +=1
                        self.archive[i] = {}
                    else:
                        return self.register_operation(processID, filename, DELETE_FILE_NOT_PERMITTED)
        if(size == 0):                
            return self.register_operation(processID, filename, FILE_NOT_FOUND)
        else:
            return self.register_operation(processID, filename, DELETE_FILE_SUCESS, offset=offset, filesize=size)
    
    # Brief: 
    #   Register log of a file operation
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    #   operationID: Integer correspondig to the status of the operation (eg. CREATE_FILE_SUCESS, CREATE_FILE_NOT_ENOUGTH_MEM)
    # Return: 
    #   Returns a integer
    def register_operation(self, processID: int, filename: str, operationID: int, offset: int = 0, filesize: int = 0) -> int:
        self.filemanagerlog.append({"process_id": processID, "operation": operationID, "filename": filename, "offset": offset, "filesize": filesize});
        return operationID    
    
    # Brief: 
    #   Print the log of the file operations
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def parseOperation(self, operationID: int):
        if(operationID == CREATE_FILE_SUCESS):
            return {"status": True, "operation": 0,"reason": ""}
        elif(operationID == CREATE_FILE_NOT_ENOUGTH_MEM):
            return {"status": False, "operation": 0, "reason": "Memória insuficiente"}
        elif(operationID == CREATE_FILE_NAME_IN_USE):   
            return {"status": False, "operation": 0, "reason": "Arquivo já existe"}     
        elif(operationID == DELETE_FILE_SUCESS):
            return {"status": True, "operation": 1, "reason": ""}
        elif(operationID == DELETE_FILE_NOT_PERMITTED):
            return {"status": False, "operation": 1, "reason": "Acesso negado"}        
        elif(operationID == FILE_NOT_FOUND):   
            return {"status": False, "operation": 1, "reason": "Arquivo nao encontrado"} 
        elif(operationID == INVALID_PROCESS_ID):   
            return {"status": False, "operation": 1, "reason": "O processo não existe"} 
    
    def print_file_log(self) -> None:
        print("Sistema de arquivos =>")
        for i in range(len(self.filemanagerlog)):
            log = self.filemanagerlog[i]
            parsed_operation = self.parseOperation(log["operation"])
            operation = parsed_operation["operation"]
            status = parsed_operation["status"]
            print("Operação {index} => {status}"
                .format(
                    index = i+1, 
                    status = ( "Sucesso" if status else "Falha")
                )
            )
            print("O processo {process}{status_identifier} o arquivo {file}. {reason}"
                .format(
                    process = log["process_id"], 
                    status_identifier = " {op}".format(op="criou" if operation == 0 else "deletou") if status else " não pode {op}".format(op="criar" if operation == 0 else "deletar"),
                    file = log["filename"],
                    reason = parsed_operation["reason"] if parsed_operation["reason"] != "" else "Blocos: {start} .. {end}".format(start=log["offset"], end=log["offset"]+log["filesize"]-1 )
                )
            )
            print("")
    
    # Brief: 
    #   Print the allocation of memory on disk
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def print_memory_occupation(self) -> None:
        for file in self.archive:
            if(file != {}):
                print("{filename} |".format(filename = file["filename"]),end = ' ')
            else:
                print("0 |",end = ' ')
        print("")
    
    # Brief: 
    #   Load the files.txt files on memory
    # Param:
    #    load: List of the files on memory
    # Return: 
    #   None
    def load_memory(self, load: list) -> None:
        for line in load:
            try: # Process operations, ex: 0, 0, A, 5
                int(line[0])
                raise Exception("Something went wrong in file sistem initialization")
            except ValueError: # File ocupation, ex: X, 0, 2
                filename = line[0]
                offset = line[1]
                filesize = line[2]
                for i in range(filesize):
                    self.archive[offset + i] = {"process_id": -1, "filename": filename, 'priority': -1}
                self.existing_files[(-1, filename)] = (offset, filesize)
                
         