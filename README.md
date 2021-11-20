# Pseudo Sistema Operacional - PseudoOS
O objetivo desse trabalho é aplicar os conhecimentos adquiridos na disciplina de Sistemas Operacionais através da implementação de um Pseudo Sistema Operacional, simulando as várias funções desempenhada pelo sistema operacional. Adicionalmente, iremos trabalhar conceitos aprendidos de Egenharia de Software para a modularização e boas práticas de programação.

# Ferramentas e Linguagens utilizadas
A linguagem utilizada para esse trabalho foi Python. No trabalho foram utilizadas as bibliotecas “Threading” para a sincronização e garantir a exclusão mútua. A biblioteca “Queue” para implementar as filas de prioridade. A biblioteca “datetime” para obter os  timestamps do programa. A biblioteca “Random” e “time” para poder simular um omportamento aleatório do sistema. E por fim a biblioteca “sys” para poder receber do terminal os caminhos para os arquivos de entrada para o programa. 

# Arquitetura
sistema foi subdividido em seis grandes módulos, sendo: Módulos de fila, processos, arquivos, memória e recurso, implementados de modo independente e  integrados pelo último módulo chamado de PseudoOS, responsável por implementar toda a lógica de controle e interação entre todos os módulos. Os módulos ao máximo, realizam apenas as funções de sua responsabilidade sem depender de outro módulo, ficando a cargo do módeulo de PseudoOS saber como proceder quando um módulo necessita conversar com o outro. Assim, casa módulo pode desenvolver suas próprias implementações de modo independente e os protocolos de interação entre módulos pode ser fácilmente alterado em um único local, dominuindo a complexidade e aumentando a modularidade do sistema. 

## 1. Módulo de arquivos
O módulo de arquivos é responsável por representar o Sistema de Arquivos do nosso pseudo-SO. Aqui realizamos todo o gerenciamento de arquivos no que tange à criação e à exclusão destes. A estratégia utilizada para realizar essas operações segue todos os princípios pré-estabelecidos pela especificação do trabalho, isto é: há persistência dos dados em disco; a alocação é contígua; o algoritmo de alocação do disco é o first-fit; processos de tempo real podem criar e deletar qualquer arquivo; e processos comuns possuem a limitação de deletar apenas arquivos criados por eles. 

## 2. Módulo de filas
O módulo de filas tem a responsabilidade de gerenciar as filas do escalonamento de processos. São 4 filas de prioridades tal a fila de menor número possui a maior prioridade. Além disso, também é utilizado uma estratégia de aging que visa aumentar a prioridade de um processo caso ele fique muito tempo na mesma fila.

## 3. Módulo de processos
O módulo de processos de forma geral mantém informações específicas do processo, além de possuir capacidade de agrupar os processos em quatro níveis de prioridades definidas no módulo de filas. Toda a gerência de processos é feita por meio de chamadas do sistema realizando operações como criação, e suspensão. 

## 4. Módulo de memória
O módulo de Memória tem basicamente 2 responsabilidades. Receber um processo e busca um espaço na memória para que seja alocado um espaço para tal processo na memória utilizando o algoritmo best-fit e receber um processo e um endereço na memória e liberar esse espaço desalocando esse processo.

## 5. Módulo de recurso
O módulo de recurso, na aplicação, representa o gerenciamento de E/S com um pequeno subgrupo de recursos, que são 1 scanner, 2 impressoras, 1 modem e 2 dispositivos SATA. Por se tratar de um Pseudo-SO, todas as operações envolvendo esses recursos são simuladas, com seu tempo de uso representado por um sleep randômico (entre 1 e 5 segundos).

## 6. Módulo PseudoOS
E o último módulo é o PseudoOs que é responsável por saber todas os procedimentos que envolvem na utilização de todos os demais módulos e como estes interagem de acordo com o uso dos recursos do sistema.

# Requisitos
A linguagem utilizada para esse trabalho foi Python. Todas as dependências e bibliotecas utilizadas nesse trabalho foram apenas aquelas que já vêm baixadas nativamente no Python não tendo a necessidade de se instalar nenhuma biblioteca de terceiros.
A versão Python utilizada para esse trabalho foi python 3.8.2.

# Execução
Primeiramente acesse a pasta onde estão localizados os códigos:
> cd codigo
Para executar esse programa, basta passar como dois argumentos o path para os arquivos .txt dos processos e .txt dos files como segue abaixo:
> python main.py processes.txt files.txt    
