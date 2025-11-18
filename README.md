# 🚀 Insight Jobs: Sistema de Controle de Acesso Inteligente

O projeto **Insight Jobs** é um sistema de controle de acesso inteligente que integra hardware (simulado no Wokwi com ESP32 e LCD) e software (uma API em Flask e uma interface web) para monitorar e gerenciar tentativas de acesso em tempo real. A comunicação entre o hardware e o software é realizada através da plataforma **FIWARE Orion Context Broker**, seguindo os princípios da Internet das Coisas (IoT) e Cidades Inteligentes.

O objetivo principal é simular um sistema robusto onde um dispositivo de campo (ESP32) envia uma identificação (ID) para a nuvem (FIWARE), e um sistema de backend (API Flask) consome essa informação, processa a lógica de acesso (liberado ou negado) e, em seguida, atualiza o contexto no FIWARE, que pode ser lido de volta pelo dispositivo ou visualizado em uma interface de monitoramento.

## ⚙️ Arquitetura do Sistema

A solução é dividida em três componentes principais que interagem de forma assíncrona através do FIWARE Orion Context Broker:

| Componente | Tecnologia | Função Principal |
| :--- | :--- | :--- |
| **Dispositivo de Campo (Simulação)** | Arduino/C++ (ESP32) | Captura e envia o ID de acesso para o FIWARE. Exibe o status no LCD. |
| **Context Broker** | FIWARE Orion | Atua como o ponto central de coleta e distribuição de dados de contexto em tempo real. |
| **Backend e Frontend** | Python (Flask), HTML, CSS, JavaScript | Monitora o FIWARE, processa a lógica de acesso, armazena o histórico e exibe o painel de controle. |

### Fluxo de Dados

1.  O usuário insere um ID no monitor serial do **ESP32 (Wokwi)**.
2.  O código do ESP32 envia o ID para a entidade `TesteESP32` no **FIWARE Orion** via requisição HTTP `PATCH`.
3.  A **API Flask** monitora continuamente a entidade `TesteESP32` no FIWARE.
4.  Ao detectar um novo ID, a API Flask verifica se o ID está na lista de IDs autorizados.
5.  A API Flask atualiza a entidade no FIWARE com o resultado do acesso (`statusAcesso`, `nomeUsuario`, `departamento`).
6.  A **Interface Web** consome as APIs do Flask para exibir o status do último acesso, estatísticas e histórico em tempo real.

## 💻 Tecnologias Utilizadas

Este projeto utiliza um conjunto de tecnologias modernas para simular um ambiente de IoT completo:

| Categoria | Tecnologia | Descrição |
| :--- | :--- | :--- |
| **Hardware/Firmware** | **ESP32** | Microcontrolador utilizado para simular o dispositivo de campo. |
| | **Arduino/C++** | Linguagem de programação e ambiente de desenvolvimento para o ESP32. |
| | **LiquidCrystal_I2C** | Biblioteca para controle do display LCD 16x2. |
| | **WiFi.h, HTTPClient.h** | Bibliotecas para conectividade de rede e requisições HTTP. |
| **Plataforma IoT** | **FIWARE Orion Context Broker** | Componente essencial para gerenciar e compartilhar informações de contexto em tempo real. |
| **Backend** | **Python (Flask)** | Framework web leve para construir a API de controle de acesso e monitoramento do FIWARE. |
| | **`requests`** | Biblioteca Python para fazer requisições HTTP ao FIWARE. |
| **Frontend** | **HTML5, CSS3, JavaScript** | Tecnologias padrão para a construção da interface de monitoramento web. |
| | **CORS** | Configuração no Flask para permitir a comunicação entre o frontend e o backend. |

## 👥 Integrantes do Grupo

O projeto foi desenvolvido pelos seguintes membros do grupo:

| Nome | RM |
| :--- | :--- |
| Kelwin Silva | 566348 |
| Pedro Almeida | 564711 |
| João Paulo | 565383 |

## 🛠️ Passo a Passo para Teste

Para testar o sistema, você precisará simular o ambiente do ESP32 (Wokwi) e executar o backend (API Flask) localmente.

### 1. Configuração do Backend (API Flask)

O backend é responsável pela lógica de acesso e pela interface de monitoramento.

1.  **Pré-requisitos:** Certifique-se de ter o **Python 3** instalado.
2.  **Instalar Dependências:** Navegue até o diretório do projeto e instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Executar a API:** Inicie o servidor Flask. Ele começará a monitorar o FIWARE e servirá a interface web na porta `5000`.
    ```bash
    python app.py
    ```
    Você verá a saída no console indicando que o monitoramento do FIWARE foi iniciado e a interface web está disponível.

4.  **Acessar a Interface Web:** Abra seu navegador e acesse:
    ```
    http://localhost:5000
    ```
    A interface de monitoramento será carregada, exibindo o status atual, estatísticas e histórico.

### 2. Simulação do Dispositivo (Wokwi - ESP32)

O código do ESP32 simula o envio do ID de acesso.

1.  **Acessar o Wokwi:** O código fornecido é para o simulador Wokwi. Você pode criar um novo projeto ESP32 e colar o código `wokwi: #include <Wire.h> ...` no arquivo `main.ino`.
2.  **Verificar o Circuito:** O circuito deve incluir um **ESP32** e um **LCD I2C 16x2**, conforme a imagem de referência:

    ![Diagrama de Conexão do ESP32 com LCD I2C no Wokwi](https://private-us-east-1.manuscdn.com/sessionFile/8U7qjkfkejeOAnWSV3sIjT/sandbox/zh9M7CyNkmLoQACshmefcz-images_1763448042719_na1fn_L2hvbWUvdWJ1bnR1L3VwbG9hZC93b2t3aV9jaXJjdWl0bw.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvOFU3cWprZmtlamVPQW5XU1Yzc0lqVC9zYW5kYm94L3poOU03Q3lOa21Mb1FBQ3NobWVmY3otaW1hZ2VzXzE3NjM0NDgwNDI3MTlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzVndiRzloWkM5M2IydDNhVjlqYVhKamRXbDBidy5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=FGgrAYnX7B2WRi~qxkJ8vCYBXfh0VJmVSNqvmwzuUTz5hJ9LSEyJkBv1daKMQhh9PI9Jv7W6Oy3oJor3rcSKJIEOXswj45oxi1T8kmUyCKyaK1d4s-~xvMxIWSqU0EyjIU9eyNDajrJNBmcjUNTpKrGcY3EjYkZLpzUKxWrDirID-tIAd0jsW4DsQB8cz0EGyK4ZrCrcFb4VZCv5Gdi10dA75FleQ0h3FVSYbLAq4kbkn5Zo3d-Wq685e95aXmAUDi93yiw7ZfJEjtNYlLMJLmAZItxskr0LLiCDzB1yQ9fi1LlsgN4r2vKpKWEK-cZBW7g6z6XehMdgZkbTTTPllg__)

3.  **Iniciar a Simulação:** Clique no botão "Start Simulation". O ESP32 irá se conectar à rede `Wokwi-GUEST`.
4.  **Enviar IDs de Teste:** Use o **Monitor Serial** do Wokwi para enviar os IDs.

    *   **ID Autorizado (Acesso Liberado):** Digite `12345` e pressione Enter.
    *   **ID Não Autorizado (Acesso Negado):** Digite `00000` e pressione Enter.

    O LCD exibirá o ID enviado, e o Monitor Serial mostrará o status da requisição HTTP para o FIWARE (espera-se um `Status Orion: 204` para sucesso).

    ![Saída do Monitor Serial no Wokwi](https://private-us-east-1.manuscdn.com/sessionFile/8U7qjkfkejeOAnWSV3sIjT/sandbox/zh9M7CyNkmLoQACshmefcz-images_1763448042721_na1fn_L2hvbWUvdWJ1bnR1L3VwbG9hZC93b2t3aV9zZXJpYWxfb3V0cHV0.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvOFU3cWprZmtlamVPQW5XU1Yzc0lqVC9zYW5kYm94L3poOU03Q3lOa21Mb1FBQ3NobWVmY3otaW1hZ2VzXzE3NjM0NDgwNDI3MjFfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwzVndiRzloWkM5M2IydDNhVjl6WlhKcFlXeGZiM1YwY0hWMC5wbmciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=vTVbecsDGxE~5xs-guk3XVIww41sqcL-eNgiJk914sev8ZvqeUPBTL~vO60~MxXjr~akWdkKpFiafr-kEl5UTHHZWFKWQTFP7lyGZjQzsUT0ajo5yjn6dVGXCdJXGjqIEPM1mR3bv~lz0~6Ftp9Lqw7D~J29N9bTY0avDDxjSi1GpwH0qbMCXKRjReuRxC9y0HXul7MA-6IdLTyK3cf9rnkYlQgwBHEpX3ZU0DMW9yEZG-nT-2dJvHWZ2xZHZKLbZhSnXZqc4K4mwOmwCOk5qWwTGK5~wP9xnv~Smg3DNjW8uPuMlzoTqdVKDOglY0W1ePqOgBvzfqrlaWUpaS5hmQ__)

### 3. Verificação do Resultado

Ao enviar um ID pelo Wokwi, o resultado deve ser instantaneamente refletido em dois lugares:

1.  **Console da API Flask:** O console da API Flask (`python app.py`) deve exibir a mensagem de **ACESSO LIBERADO** ou **ACESSO NEGADO**, indicando que o backend recebeu e processou o ID do FIWARE.
2.  **Interface Web:** A página `http://localhost:5000` deve atualizar automaticamente:
    *   O **Status Card** mudará para verde (Liberado) ou vermelho (Negado), exibindo os detalhes do usuário.
    *   As **Estatísticas** (Total, Liberados, Negados) serão incrementadas.
    *   O **Histórico de Acessos** listará a nova tentativa.

## 🖼️ Imagens do Projeto

| Descrição | Imagem |
| :--- | :--- |
| **Logo do Projeto** | ![Logo Insight Jobs](public/assets/logo.png) |
| **Simulação do Circuito Wokwi** | ![Diagrama de Conexão do ESP32 com LCD I2C no Wokwi](public/assets/lcd.png) |
| **Saída do Monitor Serial (Wokwi)** | ![Saída do Monitor Serial no Wokwi](public/assets/terminal.png) |
| **Exemplo da Interface Web (Acesso Negado)** | ![Interface Web - Acesso Negado](public/assets/web.png) |
