# Brief: Contains all implementation and rules related to creating and deleting files
# Author: Alexandre Kaihara and Pedro


from variaveisglobais import *


'''
1.2 Estrutura de Memória
A alocação de memória deve ser implementada como um conjunto de blocos contíguos, onde cada
bloco equivale uma palavra da memória real.
Cada processo deve alocar um segmento contíguo de memória, o qual permanecerá alocado durante
toda a execução do processo. Deve-se notar que não é necessário a implementação de memória virtual,
swap, nem sistema de paginação. Portanto, não é necessário gerenciar a memória, apenas verificar a
disponibilidade de recursos antes de iniciar um processo.
Deve ser utilizado um tamanho fixo de memória de 1024 blocos. Dessa quantidade, 64 blocos devem
ser reservados para processos de tempo-real e os 960 blocos restantes devem ser compartilhados entre os
processos de usuário. A Figura 2 ilustra o caso onde cada bloco de memória possui 1 MB.

OBS:
- A memória tem 1024 blocos;
- Desses 1024, 64 blocos é reservado ao processo de tempo-real;
- O método de alocação de processos na memória RAM pode ser feita através de qlqr algoritmo
'''


class MemoryManager():
    # Brief: 
    #   Starts all variables and strutures of the memory
    #   OBS: All methods that share variables, must use locks
    # Param:
    #   processID: Integer representing the process ID
    #   filename: String containing the filename
    # Return: 
    #   Returns a integer
   
    def __init__(self) -> None:
        self.memory = [False] * 1024 # False means that the block is free and true means it is ocupied

    # Brief: 
    #   Load on RAM memory the process
    # Param:
    #   processID: Integer representing the process ID
    #   size: Process size to the accupied
    #   offset: At the end of execution, should set this variable with the offset given to the allocated process
    # Return: 
    #   If there is no free memory available, return NOT_ENOUGH_RAM_MEMORY, else, MEMORY_ALLOCATION_SUCESS
    #   Else return 0
    def load(self, processID: int, size: int, offset: list) -> int:
        i: int = 0
        count = 0
        unsorted_free = {}
        # Percorre memória de forma a conferir sequencias de falses de forma a identificar espaços vazios
        while(i < len(self.memory)):
            if (self.memory[i] == True):
                if(count > 0):
                    unsorted_free[i - count] = count # é sahvo em um hash em que {endereço: tamanho}
                count = 0
            else:
                count+=1 
            i+=1

        if(count > 0):
            unsorted_free[i - count] = count
                
        free = sorted(unsorted_free.items(), key = lambda kv:(kv[1], kv[0])) # Ordena lista de espaços vazios em ordem crescente de tamanho

        for key,val in free:
            if(val >= size ): # Seleciona o menor tamanho livre possível que caiba o processo
                offset[0] = key
                self.__alocate(size,offset[0]) 
                return MEMORY_ALLOCATION_SUCESS

        return NOT_ENOUGH_RAM_MEMORY

    def __alocate(self, size: int, offset: int) -> None:
        while(size>=0):
            self.memory[offset + size - 1] = True
            size -= 1
        
    # Brief: 
    #   Remove from memory
    # Param:
    #   processID: Integer representing the process ID
    # Return: 
    #   None
    def remove(self, processID: int, size: int, offset: list) -> None:
        while(size>=0):
            self.memory[offset + size - 1] = False
            size -= 1
        

