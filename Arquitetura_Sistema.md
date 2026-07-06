# Descrição da Arquitetura do Sistema — SoundWave

## 1. Justificativas Técnicas
O sistema foi projetado seguindo a arquitetura em camadas para separar a lógica de negócio da interface do usuário. Optamos pelo uso de **Python** devido à sua vasta gama de bibliotecas para manipulação de áudio e facilidade na implementação de estruturas de dados complexas.

## 2. Padrões de Projeto Utilizados
- **Singleton:** Aplicado na classe `MusicRepository`. Garante que apenas uma instância gerencie a biblioteca e as playlists, evitando inconsistências na persistência de dados.
- **Observer:** O `MusicPlayer` atua como o sujeito e a `SoundWaveCLI` como observadora. Isso permite que a interface seja notificada e atualizada automaticamente quando uma música começa ou termina, sem acoplamento forte.
- **Repository:** Isola a lógica de acesso a dados (JSON) do restante da aplicação, facilitando futuras trocas de banco de dados como o SQLite.

## 3. Estruturas de Dados
- **Pilha (Stack):** Utilizada para o **Histórico de Reprodução**. O comportamento LIFO (Last-In, First-Out) é ideal para navegar pelas músicas ouvidas recentemente.
- **Fila (Queue):** Utilizada para a **Fila de Reprodução**. Garante que as músicas sejam tocadas na ordem em que foram adicionadas (FIFO).
- **Lista Duplamente Encadeada:** Implementada para permitir a navegação flexível (Próxima/Anterior) em sequências de reprodução futuras.

## 4. Diagrama de Classes (Resumo)
- `Song`: Entidade com metadados e caminho do arquivo.
- `MusicRepository`: Gerencia a coleção de `Song` e dicionários de playlists.
- `MusicPlayer`: Controla o `pygame.mixer` e gerencia threads de monitoramento.
- `SoundWaveCLI`: Orquestra as entradas do usuário e exibe o estado do sistema.

## 5. Programação Concorrente
Foi utilizado o módulo `threading` para criar um monitor em background. Esse monitor verifica o estado do mixer de áudio a cada segundo. Se detectar que uma música terminou, ele dispara automaticamente o comando para tocar a próxima música da fila, garantindo uma experiência fluida.

## 6. Análise Crítica e Melhorias Futuras
O sistema cumpre todos os requisitos funcionais e técnicos. Como melhoria, a implementação de uma **Árvore AVL** para busca binária por título de música aumentaria a eficiência em bibliotecas com milhares de arquivos. Além disso, uma interface gráfica (GUI) com `Tkinter` ou `PyQt` tornaria o uso mais amigável.
