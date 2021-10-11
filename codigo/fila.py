# Brief: Define the structure of the queue of processes and the logic that defines the next process to be executed
# Author: Alexandre Kaihara and Pedro

from variaveisglobais import *

from queue import Queue
from datetime import datetime
from threading import Semaphore

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
    def __init__(self, aging_time):
        self.aging_time = aging_time
        self.real_time_sem = Semaphore(1)
        self.user_1_sem = Semaphore(1)
        self.user_2_sem = Semaphore(1)
        self.user_3_sem = Semaphore(1)
        self.real_time  = Queue()
        self.user_1     = Queue()
        self.user_2     = Queue()
        self.user_3     = Queue()
        self.queues = [self.real_time, self.user_1, self.user_2, self.user_3]
        self.sems = [self.real_time_sem, self.user_1_sem, self.user_2_sem, self.user_3_sem]

    # Brief: 
    #   Insert new process on the queue according to the priority
    # Param:
    #   processID: The integer that defines the process
    #   priority: Integer that defines the priority
    # Return: 
    #   None
    def insert(self, processID: int, priority: int) -> None:
        if priority <= 3:
            print("** Inserted process", processID, " on queue with priority", priority, "\n")
            now = datetime.now()
            process = (processID, now)
            queue = self.queues[priority]
            sem = self.sems[priority]

            # Insert process on right queue
            sem.acquire()
            queue.put(process)
            sem.release()
        else:
            print("[ERROR] Requested priority not permitted")

    # Brief: 
    #   Remove a process from the queue by its ID
    # Param:
    #   processID: Identification of the process
    #   priority: priority of the process
    # Return: 
    def remove(self, processID: int, priority: int) -> None:
        queue = self.queues[priority]
        sem = self.sems[priority]
        # Find process and remove it from queue
        def removeitem(processID: int) -> None:
            aux, insertion_time = queue.get()
            if(aux != processID):
                queue.put((aux, insertion_time))
        # Remove item from queue
        sem.acquire()
        [removeitem(processID) for _ in range(len(queue.queue))]
        sem.release()
        
    # Brief: 
    #   Verify if all processes are over the aging time and put on a higher priority queue
    # Param:
    # Return
    def aging(self) -> None:
        now = datetime.now()
        # Get all processes to be aged
        for priority in range(2, 4):
            # Get list of all processID with aging time higher than self.aging_time
            processes = [id for id, insertion_time in list(self.queues[priority].queue) \
                if diff_time(now, insertion_time) > self.aging_time]
            # Remove them and insert on a higher priority file
            if len(processes) > 0:
                print("** Priority ", priority, " queue has to these processes to be aged", processes, "\n")
            [self.remove(id, priority) for id in processes]
            [self.insert(id, priority-1) for id in processes]
        
    # Brief: 
    #   Remove a process from the queue and send it to be executed
    # Param:
    # Return: 
    #   Returns the integer that identify the next process to be executed, if there is no next process, return NO_NEXT_PROCESS
    def next_process(self) -> int:
        for priority in range(4):
            if(not self.queues[priority].empty()):
                return self.__get_next(priority)[0]
        return NO_NEXT_PROCESS
    
    # Brief: 
    #   Remove the next process according to the priority
    # Param:
    #   priority: Priority of the process
    # Return: 
    #   Returns the integer that identify the next process to be executed
    def __get_next(self, priority: int) -> int:
        self.sems[priority].acquire() 
        aux = self.queues[priority].get()
        self.sems[priority].release()
        return aux 
