# Brief: Define the structure of the queue of processes and the logic that defines the next process to be executed
# Author: Alexandre Kaihara and Pedro

from variaveisglobais import *

'''
O programa deve ter duas filas de prioridades distintas: a fila de processos de tempo real e a fila de
processos de usuários. Processos de tempo real entram para a fila de maior prioridade, sendo gerenciados
pela política de escalonamento FIFO (First In First Out), sem preempção.
Processos de usuário devem utilizar múltiplas filas de prioridades com realimentação. Para isso,
devem ser mantidas três filas com prioridades distintas. Para evitar starvation, o sistema operacional deve
modificar a prioridade dos processos executados mais frequentemente e/ou utilizar uma técnica de
envelhecimento (aging). Quanto menor for o valor da prioridade atribuída a um processo, maior será a sua
prioridade no escalonamento. Dessa forma, os processos de tempo real, que são os mais prioritários, terão
prioridade definida como 0 (zero). Além disso, é importante destacar que processos de usuário podem ser
preemptados e o quantum deve ser definido de 1 segundo.
As filas devem suportar no máximo 1000 processos. Portanto, recomenda-se utilizar uma fila
“global”, que permita avaliar os recursos disponíveis antes da execução e que facilite classificar o tipo de
processo. A Figura 1 ilustra o esquema indicado.
'''

class QueueManager():
    # Brief: 
    #   Defines the queues. 1 queue for real-time processes and 3 queues for user processes
    #   OBS: !!!All methods which acess same shared variable, must have mutex!!!
    # Param:
    #   None
    # Return: 
    #   None
    def __init__(self):
        '''Implementation'''
        pass

    # Brief: 
    #   Insert new process on the queue according to the priority
    # Param:
    #   processID: The integer that defines the process
    #   priority: Integer that defines the priority
    # Return: 
    #   None
    def insert(self, processID: int, priority: int) -> None:
        print("Inserted process", processID, "with priority", priority, "\n")
        '''Implementation'''
        pass

    # Brief: 
    #   Remove a process from the queue by its ID
    # Param:
    #   processID: Identification of the process
    # Return: 
    def remove(self, processID: int) -> None:
        '''Implementation'''
        pass

    # Brief: 
    #   Remove a process from the queue and send it to be executed
    # Param:
    # Return: 
    #   Returns the integer that identify the next process to be executed, if there is no next process, return NO_NEXT_PROCESS
    def next_process(self) -> int:
        '''Implementation'''
        return NO_NEXT_PROCESS
