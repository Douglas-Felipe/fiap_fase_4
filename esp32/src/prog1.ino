#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <DHT.h>

#define botaoFosforo 22  // Pino GPIO conectado ao push button que simula o sensor de presença de fosforo
#define botaoPotassio 23 // Pino GPIO conectado ao push button que simula o sensor de presença de potassio
#define ledPin 17      // Pino GPIO conectado ao LED 
#define ldrPin 34      // Pino GPIO conectado ao LDR 
#define DHTPIN 13      // Pino GPIO conectado ao sensor DHT
#define DHTTYPE DHT22 // Tipo do sensor DHT (DHT11, DHT22, etc.)
#define RELAYPin 12 // Pino GPIO conectado ao relé 

const char* ssid = "Wokwi-GUEST";  // Substitua pelo seu SSID da sua rede Wi-Fi (quando rodar em dispositivo fisico)
const char* password = "";  // Substitua pela sua senha da rede Wi-Fi (quando rodar em dispositivo fisico)

const char* urlApi = "https://merely-blue-young-submit.trycloudflare.com/"; // URL do servidor rodando via clloudflare 

const int sensorFosforo = 1; // codigo do sensor de fosforo (P) na base de dados segundo script de carga inicial
const int sensorPotassio = 2; // codigo do sensor de Potassio (K) na base de dados segundo script de carga inicial
const int sensorPH = 3; // codigo do sensor de pH na base de dados segundo script de carga inicial
const int sensorUmidade = 4; // codigo do sensor de Umidade na base de dados segundo script de carga inicial
const int codigoLocal = 1; // codigo do local na base de dados segundo script de carga inicial
const int codigoProdutoIrrigacao = 1; // codigo do produto de irrigacao na base de dados segundo script de carga inicial

DHT dht(DHTPIN, DHTTYPE);


// Este métod é usado para emitir alertas atraves do Led, fazendo ele piscar
// quantas vezes forem necessárias e com velocidade variada
void geraSinal(int qt, int velocidade) 
  {
    //pisca o led X vezes 
    for (int i = 0; i <qt; i++) {
        digitalWrite(ledPin, HIGH);   // Liga o LED
        delay(velocidade);                   // Aguarda meio segundo
        digitalWrite(ledPin, LOW);    // Desliga o LED
        delay(velocidade);                   // Aguarda meio segundo
    }
  } 


// metodo que faz a inicialização de todos os camponentes configurando suas portas e fazendo
// a conexão inicial com o wifi
void setup() {
    pinMode(botaoFosforo, INPUT_PULLUP);  // Configura o pino do botão como entrada com pull-up interno
    pinMode(botaoPotassio, INPUT_PULLUP);  // Configura o pino do botão como entrada com pull-up interno
    pinMode(ledPin, OUTPUT);           // Configura o pino do LED como saída
    pinMode(RELAYPin, OUTPUT); // Configura o pino do relé como saída  

    Serial.begin(115200);                // Inicia a comunicação serial
    analogReadResolution(12);  // Define a resolução do ADC para 12 bits (0-4095)
    dht.begin();  // Inicia o sensor DHT
    WiFi.begin(ssid, password); 
    

    Serial.println("Conectando ao WiFi...");
    while (WiFi.status() != WL_CONNECTED) {  // Aguarda conexão com a rede Wi-Fi
        delay(2000);
        Serial.print(".");
    }

    geraSinal(3, 500);  // Pisca o LED 3 vezes para indicar que está ligado
    

    Serial.println("Conectado ao WiFi!");
}

// Eata rotina vai ficar em loop rodando a cada 15 segundos coletando os dados dos sensores
// e enviando para o servidor
void loop() {
    
    geraSinal(2, 400);  // Pisca o LED 2 vezes para indicar que está coletando dados
    
    //verifica se o botão de fosforo está pressionado
    int estadoBotaoFosforo = digitalRead(botaoFosforo);  // Lê o estado do botão de fosforo
    
    // verifica se o botao de potassio está pressionado
    int estadoBotaoPotassio = digitalRead(botaoPotassio);  // Lê o estado do botão de potassio


    // Realiza a leitura dos sensores
    int umidade = dht.readHumidity();  // Lê a umidade do sensor DHT
    int pH = analogRead(ldrPin);     // Lê o valor do LDR 
    int fosforo = 0;
    if (estadoBotaoFosforo == LOW) {  // Se o botão de fosforo for pressionado
        fosforo = 1;                  // Simula a presença de fosforo
    }
    int potassio = 0;
    if (estadoBotaoPotassio == LOW) {  // Se o botão de potassio for pressionado
        potassio = 1;                  // Simula a presença de potassio
    }   

    Serial.println("Vai enviar os dados para o servidor");
    // Envia os dados para o servidor  
    registraColeta(umidade, pH, fosforo, potassio);  // Chama a função para registrar a coleta via API Python

    if (umidade < 30) {  // Se a umidade estiver abaixo de 30%
        Serial.println("Umidade baixa!");  // Imprime mensagem de umidade baixa
        geraSinal(4, 200);  // Pisca o LED 3 vezes para indicar que a umidade está baixa
        digitalWrite(RELAYPin, HIGH);  // Liga o relé para irrigação
        invocaAPIAplicacao(codigoLocal, codigoProdutoIrrigacao, 100);  // Chama a função para registrar a aplicação de produtos no solo
    } 
    else {
        Serial.println("Umidade ok!");  // Imprime mensagem de umidade ok
        digitalWrite(RELAYPin, LOW);  // Desliga o relé para irrigação
    }

    delay(15000);  // aguarda 15 segundos antes de coletar novamente
}


// metodo responsavel por invocar a API Python para registrar indivisualmente os dados
// coletados de cada um dos 4 sensores
void registraColeta(int umidade, int pH, int fosforo, int potassio)
{
    Serial.println("");
    Serial.println("umidade: " + String(umidade));
    Serial.println("pH: " + String(pH));
    Serial.println("fosforo: " + String(fosforo));  
    Serial.println("potassio: " + String(potassio));
    
    invocaAPIColeta(pH, sensorPH, "pH");
    invocaAPIColeta(umidade, sensorUmidade, "Percentual");
    invocaAPIColeta(fosforo, sensorFosforo, "booleano");
    invocaAPIColeta(potassio, sensorPotassio, "booleano");    

}


// metodo responsavel por registrar que um determinado produto foi 
// aplicado ao local de cultivbo em resposta a algum indicador coletado pelos
// senshores, neste caso de uso em especial estamos registrando o inicio do processo
// de irrigação
void invocaAPIAplicacao(int local, int produto, int quantidade)
{
    Serial.println("Registrando dados da aplicação de produtos no solo...");
    WiFiClientSecure client;
    client.setInsecure();  // <== fundamental
    HTTPClient http;
    String url = String(urlApi) + "aplicacao";
    http.begin(client, url);  // Inicia a conexão com o servidor
    http.addHeader("Content-Type", "application/json");  // Define o cabeçalho da requisição como JSON
    String json = "{\"codigo_local\":" + String(local) + ",\"codigo_produto\":" + String(produto) + ",\"quantidade\":" + quantidade + "}";
    int httpCode = http.POST(json);
    if (httpCode > 0) 
    {
        Serial.println("Código HTTP: " + String(httpCode));
        Serial.println("Resposta: " + http.getString());
    } 
    else 
    {
        Serial.println(json);
        Serial.println("Erro: " + http.errorToString(httpCode));
    }
    http.end();  // Finaliza a conexão
}

// metodo responsavel por chamar a API Python para registrar em banco de dados
// os dados coletados dos sensores, estes dados ficaram disponiveis para 
// futura analise da correlação destas diferentes métricas com o resultado da colheita 
void invocaAPIColeta(int valorColetado, int codigoSensor, String tipoIndicador)
{
    WiFiClientSecure client;
    client.setInsecure();  // <== fundamental
    HTTPClient http;
    String url = String(urlApi) + "coleta";
    http.begin(client, url);  // Inicia a conexão com o servidor
    http.addHeader("Content-Type", "application/json");  // Define o cabeçalho da requisição como JSON
    String json = "{\"codigo_sensor\":" + String(codigoSensor) + ",\"valor_coletado\":" + String(valorColetado) + ",\"tipo_indicador\":\"" + tipoIndicador + "\"}";
    int httpCode = http.POST(json);
    if (httpCode > 0) 
    {
        Serial.println("Código HTTP: " + String(httpCode));
        Serial.println("Resposta: " + http.getString());
        if (httpCode == 400)
        {
            Serial.println(json);
        }
    } 
    else 
    {
        Serial.println(json);
        Serial.println("Erro: " + http.errorToString(httpCode));
    }
    http.end();  // Finaliza a conexão
}

