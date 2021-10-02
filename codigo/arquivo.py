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
    def __init__(self, memoryload: list) -> None:
        self.filemanagerlog = []
        self.load_memory(memoryload)
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
    def createfile(self, processID: int, filename: str, filesize: int):
        '''IMPLEMENT
        operationID: Integer correspondig to the status of the operation (eg. CREATE_FILE_SUCESS, CREATE_FILE_NOT_ENOUGTH_MEM)
        '''
        
        self.__register_operation(processID, filename, CREATE_FILE_SUCESS)

    # Brief: 
    #   Verify if given file exists on memory, if so, then delete it.
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def deletefile(self, processID: int, filename: str) -> int:
        '''IMPLEMENT
        operationID: Integer correspondig to the status of the operation (eg. DELETE_FILE_SUCESS, DELETE_FILE_NOT_PERMITTED, FILE_NOT_FOUND)
        '''
        self.__register_operation(processID, filename, DELETE_FILE_SUCESS)

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
    def print_file_log(self) -> None:
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

    # Brief: 
    #   Print the allocation of memory on disk
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
    def print_memory_occupation(self) -> None:
        '''IMPLEMENT'''
        '''
        Example 
        D D D Y 0 Z Z Z 0 0 
        '''
        pass

    # Brief: 
    #   Load the files.txt files on memory
    # Param:
    #    load: List of the files on memory
    # Return: 
    #   None
    def load_memory(self, load: list) -> None:
        pass