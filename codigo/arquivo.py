# Brief: Contains all implementation and rules related to creating and deleting files
# Author: Alexandre Kaihara and Pedro

from variaveisglobais import *

'''
1.4 Estrutura do Sistema de Arquivos
O pseudo-SO deve permitir que cada processo possa criar e deletar arquivos. Na criação de um
arquivo, os dados devem ficar residentes no disco, mesmo após o encerramento do processo. O sistema de
arquivos fará a alocação por meio do método de alocação contígua. Contudo, o arquivo deve ser tratado
como uma unidade de manipulação. Além disso, para que possamos ter a mesma tomada de decisão, vamos
considerar que o algoritmo a ser usado no armazenamento do disco (embora não seja usual ser usado na
alocação do disco) seja o first-fit (sempre considerando a busca a partir do primeiro bloco do disco).
Além disso, o sistema de arquivos deve garantir que os processos de tempo real possam criar (se
tiver espaço) e deletar qualquer arquivo (mesmo que não tenha sido criado pelo processo). Por outro lado, os
processos comuns do usuário, só podem deletar arquivos que tenham sido criados por eles, e podem criar
quantos arquivos desejarem, no tamanho que for solicitado (se houver espaço suficiente).
O sistema de arquivos terá como entrada um arquivo com extensão .txt, que contém a quantidade
total de blocos no disco, a especificação dos segmentos ocupados por cada arquivo, as operações a serem
realizadas por cada processo.
Assim, após o pseudo-SO executar todos os processos, ele deve mostrar na tela do computador um
mapa com a atual ocupação do disco, descrevendo quais arquivos estão em cada bloco, e quais são os
blocos vazios (identificados por 0).


Observações:
- Quando for criar um bloco na memória, marcar cada bloco ocupado com o nome do arquivo que a ocupou;
- O sistema de arquivos fará a alocação por meio do método de alocação contígua;
- Algoritmo de armazenamento é first-fit (sempre considerando a busca a partir do primeiro bloco do disco);
- Arquivos só podem ser deletados pelo próprio usuário que a criou. Se o processo for do tipo "tempo real", pode deletar qualquer um;
'''


class ArchiveManager():
    # Brief: 
    #   Must read the file and load it on memory
    # Param:
    #   path: String containing the path to the file   
    # Return: 
    #   None
    def __init__(self, memoryload: list, memory_size: int) -> None:
        self.filemanagerlog = []
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
    def createfile(self, processID: int, filename: str, filesize: int) -> int:
        i: int = 0
        count = 0
        while(i < len(self.archive)):
            if (self.archive[i] != {}):
                if(count >= filesize):
                    self.__alocate(filename, filesize, processID, (i-count))
                    return self.__register_operation(processID, filename, CREATE_FILE_SUCESS, offset= (i-count), filesize=filesize)
                count = 0
            else:
                count+=1

            if(count >= filesize):
                self.__alocate(filename, filesize, processID, (i-count))
                return self.__register_operation(processID, filename, CREATE_FILE_SUCESS, offset= (i-count), filesize=filesize)
                
            i+=1

        return self.__register_operation(processID, filename, CREATE_FILE_NOT_ENOUGTH_MEM)

    def __alocate(self, filename: str, size: int, processId: int, offset: int) -> None:
        while(size>0):
            self.archive[offset + size] = {"process_id": processId, "filename": filename}
            size -= 1

    # Brief: 
    #   Verify if given file exists on memory, if so, then delete it.
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def deletefile(self, processID: int, filename: str, isRealTime) -> int:
        offset =0
        size =0
        for i in range(len(self.archive)):
            file = self.archive[i]
            if( file != {}):
                if(file["filename"] == filename):
                    offset = i if offset == 0 else offset
                    if(file["process_id"] == processID or file["process_id"] == -1 or isRealTime):
                        size +=1
                        self.archive[i] = {}
                    else:
                        return self.__register_operation(processID, filename, DELETE_FILE_NOT_PERMITTED)
        if(size == 0):                
            return self.__register_operation(processID, filename, FILE_NOT_FOUND)
        else:
            return self.__register_operation(processID, filename, DELETE_FILE_SUCESS, offset=offset, filesize=size)

    # Brief: 
    #   Register log of a file operation
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    #   operationID: Integer correspondig to the status of the operation (eg. CREATE_FILE_SUCESS, CREATE_FILE_NOT_ENOUGTH_MEM)
    # Return: 
    #   Returns a integer
    def __register_operation(self, processID: int, filename: str, operationID: int, offset: int = 0, filesize: int = 0) -> int:
        self.filemanagerlog.append({"process_id": processID, "operation": operationID, "filename": filename, "offset": offset, "filesize": filesize});
        return operationID
        
    
    # Brief: 
    #   Print the log of the file operations
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    '''
        Example:
        Sistema de arquivos =>
        Operação 1 => Falha
        O processo 0 não pode criar o arquivo A (falta de espaço).
        Operação 2 => Sucesso
        O processo 0 deletou o arquivo X.
        Operação 3 => Falha
        O processo 2 não existe.
        Operação 4 => Sucesso
        O processo 0 criou o arquivo D (blocos 0, 1 e 2).
        Operação 5 => Falha
        O processo 1 não pode deletar o arquivo E porque ele não existe.
    '''
    def parseOperation(self, operationID: int):
        if(operationID == CREATE_FILE_SUCESS):
            return {"status": True, "operation": 0,"reason": ""}
        if(operationID == CREATE_FILE_NOT_ENOUGTH_MEM):
            return {"status": False, "operation": 0, "reason": "Memória insuficiente"}
        if(operationID == CREATE_FILE_NAME_IN_USE):   
            return {"status": False, "operation": 0, "reason": "Arquivo já existe"}     
        if(operationID == DELETE_FILE_SUCESS):
            return {"status": True, "operation": 1, "reason": ""}
        if(operationID == DELETE_FILE_NOT_PERMITTED):
            return {"status": False, "operation": 1, "reason": "Acesso negado"}        
        if(operationID == FILE_NOT_FOUND):   
            return {"status": False, "operation": 1, "reason": "Arquivo nao encontrado"} 


    def print_file_log(self) -> None:
        print("Sistema de arquivos =>")
        for i in range(len(self.filemanagerlog)):
            log = self.filemanagerlog[i]
            parsed_operation = self.parseOperation(log["operation"])
            operation = parsed_operation["operation"]
            status = parsed_operation["status"];
            print("Operação {index} => {status}"
                .format(
                    index = i+1, 
                    status = ( "Sucesso" if status else "Falhou")
                )
            )
            print("O processo {process}{status_identifier}o arquivo {file} {reason}"
                .format(
                    process = log["process_id"], 
                    status_identifier = " {op}".format(op="criou" if operation == 0 else "deletou") if status else " não pode {op}".format(op="crear" if operation == 0 else "deletar"),
                    file = log["filename"],
                    reason = ", "+parsed_operation["reason"] if parsed_operation["reason"] != "" else "Blocos: {start} .. {end}".format(start=log["offset"], end=log["offset"]+log["filesize"] -1 )
                )
            )


    # Brief: 
    #   Print the allocation of memory on disk
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    '''
        Example 
        D D D Y 0 Z Z Z 0 0 
    '''
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
                    self.archive[offset + i] = {"process_id": -1, "filename": filename}
                
         