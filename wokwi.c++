#include <Wire.h>               // Inclui a biblioteca para comunicação I2C (necessária para o LCD)
#include <LiquidCrystal_I2C.h>  // Inclui a biblioteca para controlar o display LCD via I2C
#include <WiFi.h>               // Inclui a biblioteca para gerenciar a conexão WiFi do ESP32
#include <HTTPClient.h>         // Inclui a biblioteca para fazer requisições HTTP (GET, POST, PATCH, etc.)

// Cria um objeto para o LCD com endereço 0x27, 16 colunas e 2 linhas
LiquidCrystal_I2C lcd(0x27, 16, 2); 

// --- CONFIG WIFI ---
const char* ssid = "Wokwi-GUEST"; // Define o nome da rede WiFi (SSID)
const char* password = "";        // Define a senha da rede WiFi (vazia para Wokwi-GUEST)

// --- CONFIG FIWARE ORION ---
// Define o endereço do servidor FIWARE Orion e o endpoint para atualizar atributos da entidade 'TesteESP32'
String orion_ip = "http://130.131.19.158:1026/v2/entities/TesteESP32/attrs";

void setup() {
  Serial.begin(115200); // Inicializa a comunicação serial com velocidade de 115200 bits por segundo

  // Inicializa LCD
  lcd.init();           // Inicializa o hardware do display LCD
  lcd.backlight();      // Liga a luz de fundo do LCD para que o texto seja visível
  lcd.setCursor(0, 0);  // Posiciona o cursor na coluna 0, linha 0 (primeira linha)
  lcd.print("Iniciando..."); // Escreve "Iniciando..." no display

  // WiFi
  WiFi.begin(ssid, password); // Inicia a tentativa de conexão com a rede WiFi configurada
  lcd.setCursor(0, 1);        // Move o cursor para a coluna 0, linha 1 (segunda linha)
  lcd.print("WiFi...");       // Escreve "WiFi..." indicando que está tentando conectar

  // Loop que mantém o processador ocupado enquanto o status do WiFi não for "Conectado"
  while (WiFi.status() != WL_CONNECTED) {
    delay(300); // Aguarda 300 milissegundos antes de verificar novamente
  }

  lcd.clear();          // Limpa todo o conteúdo do display LCD
  lcd.print("WiFi OK"); // Escreve "WiFi OK" para confirmar a conexão
  delay(1000);          // Aguarda 1 segundo para o usuário ler a mensagem
  lcd.clear();          // Limpa o display novamente para deixá-lo pronto para uso

  Serial.println("Digite um ID: "); // Envia uma mensagem para o Monitor Serial pedindo um input do usuário
}

void loop() {
  // Verifica se há dados disponíveis chegando pela porta Serial (digitação do usuário)
  if (Serial.available()) {
    String id = Serial.readStringUntil('\n'); // Lê a string enviada até encontrar uma quebra de linha (Enter)
    id.trim(); // Remove espaços em branco ou quebras de linha no início e fim da string capturada

    if (id.length() == 0) return; // Se a string estiver vazia (apenas Enter foi pressionado), sai da função e não faz nada

    // Mostra no LCD
    lcd.clear();            // Limpa o display antes de mostrar a nova informação
    lcd.setCursor(0, 0);    // Posiciona o cursor na primeira linha
    lcd.print("Enviando ID:"); // Escreve o rótulo "Enviando ID:"
    lcd.setCursor(0, 1);    // Posiciona o cursor na segunda linha
    lcd.print(id);          // Escreve o ID que foi digitado pelo usuário

    // Envia para FIWARE
    enviarParaFiware(id);   // Chama a função personalizada para enviar o dado via HTTP

    Serial.println("Digite outro ID: "); // Solicita um novo ID no Monitor Serial
  }
}

// Função auxiliar para encapsular a lógica de envio HTTP
void enviarParaFiware(String id) {
  // Verifica se o WiFi ainda está conectado antes de tentar enviar
  if (WiFi.status() == WL_CONNECTED) { 
    HTTPClient http; // Cria uma instância do cliente HTTP

    http.begin(orion_ip); // Inicializa a conexão com a URL do Orion definida no início
    http.addHeader("Content-Type", "application/json"); // Define o cabeçalho indicando que o corpo da mensagem é JSON

    // Monta o JSON manualmente. As barras invertidas (\") servem para colocar aspas dentro da string.
    // Estrutura: {"idRecebido": {"type": "Text", "value": "VALOR_DO_ID"}}
    String json = "{\"idRecebido\": {\"type\": \"Text\", \"value\": \"" + id + "\"}}";

    // Envia a requisição do tipo PATCH com o JSON criado. 
    // PATCH é usado no FIWARE para atualizar apenas atributos específicos de uma entidade existente.
    int status = http.sendRequest("PATCH", json);

    Serial.print("Status Orion: "); // Imprime texto de depuração
    Serial.println(status);         // Imprime o código de resposta HTTP (ex: 204 é sucesso, 404 erro)

    // Se o status for maior que 0, significa que houve resposta do servidor
    if (status > 0) {
      Serial.println(http.getString()); // Imprime o corpo da resposta do servidor (se houver)
    } else {
      Serial.println("Erro ao enviar ao FIWARE"); // Imprime mensagem de erro caso o status seja negativo (erro de conexão)
    }

    http.end(); // Finaliza a conexão HTTP para liberar recursos
  }
}