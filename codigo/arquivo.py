# Brief: Contains all implementation and rules related to creating and deleting files
# Author: Alexandre Kaihara and Pedro



'''
Observações:
- A memória tem 1024 blocos;
- Desses 1024, 64 blocos é reservado ao processo de tempo-real;
- Quando for criar um bloco na memória, marcar cada bloco ocupado com o nome do arquivo que a ocupou;
- O sistema de arquivos fará a alocação por meio do método de alocação contígua;
- Algoritmo de armazenamento é first-fit (sempre considerando a busca a partir do primeiro bloco do disco);
- Arquivos só podem ser deletados pelo próprio usuário que a criou. Se o processo for do tipo "tempo real", pode deletar qualquer um;
- 
'''


class ArchiveManager():
    # Brief: 
    #   Must read the file and load it on memory
    # Param:
    #   path: String containing the path to the file
    # Return: 
    #   None
    def __init__(self, path: str) -> None:
        self.filemanagerlog = []
        '''IMPLEMENT'''
        pass

    # Brief: 
    #   Verify using first-fit a contiguous available memmory free and create file.
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    #   filesize: Integer containing the number of blocks to be allocated
    # Return: 
    #   Returns integer which is a code if the file succeded of failed. If succeed on creating, return CREATE_FILE_SUCESS
    def createfile(self, processID: int, filename: str, filesize: int) -> int:
        '''IMPLEMENT'''
        self.__register_operation(processID, filename, operationID)

    # Brief: 
    #   Verify if given file exists on memory, if so, then delete it.
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def deletefile(self, processID: int, filename: str) -> int:
        '''IMPLEMENT'''
        self.__register_operation(processID, filename, operationID)

    # Brief: 
    #   Register log of a file operation
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    #   operationID: Integer correspondig to the status of the operation (eg. CREATE_FILE_SUCESS, CREATE_FILE_NOT_ENOUGTH_MEM)
    # Return: 
    #   Returns a integer
    def __register_operation(self, processID: int, filename: str, operationID: int) -> None:
        '''IMPLEMENT'''
        pass
    
    # Brief: 
    #   Print the log of the file operations
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def print_file_log():
        '''IMPLEMENT'''
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
        pass


    def print_memory_occupation():
        '''IMPLEMENT'''
        '''
        Example 
        D D D Y 0 Z Z Z 0 0 
        '''
        pass

        