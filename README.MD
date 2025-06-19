# FIAP - Faculdade de Informática e Administração Paulista 

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" width=40% height=40%></a>
</p>

<br>

# Agricultura Inteligente

## Grupo DRELL

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/douglas-souza-felipe-b815281a2/">Douglas</a>
- <a href="https://www.linkedin.com/in/richard-marques-26b3a14/">Richard</a>
- <a href="https://www.linkedin.com/in/lucasmedeirosleite">Lucas Medeiros</a> 
- <a href="https://www.linkedin.com/in/evelyn-z-342a07365/">Evelyn Z</a> 
- <a href="https://www.linkedin.com/in/luis-fernando-dos-santos-costa-b69894365/">Luis</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://github.com/leoruiz197">Leo Ruiz</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">Andre Godoi</a>


## 📜 Descrição

Este projeto tem por objetivo demonstrar as capacidades aprendidadas pelo grupo na fase 3 do curso de Inteligencia Artificial da FIAP. Neste exercicio criamos uma API Python que permite interagir com a b ase de dados modelada na fase 2. 

Aqui tem o link da documentação para você ter acesso ao código fonte e colocar para rodar a API para que possa ser usada pelo simulador:
[Documentacao API Python](api-python/README.MD)

![Modelagem da base de dados](assets/modelo_agro.png)


A partir desta API usamos um simulador ESP32 para servir de IoT para o nosso projeto, simulando a coleta de vários dados do cultivo permitindo acionar quando necessário a irrigação dos campos. 

Aqui tem o link da documentação e o código fonte do projeto ESP32 para você executar o simulador.
[Documentacao ES32](esp32/README.MD)

![Diagrama do projeto ESP32](esp32/ìmagens/monitor-lcd.png)


## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>api-python</b>: aqui estão todos os documentos do projeto da API  Pythin bem como o código fonte

- <b>esp32</b>: Aqui estão toda a documentação e código fonte do projeto IoT baseado em ESP32 e as instruçòes para executá-lo

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

Precisa ser feita em duas etapas, siga a documentação da API Python primeiro, uma vez que ela esteja rodando e com a URL exposta na Internet, você segue a documentação do Esp32, reconfigura ele com a sua URL, compila e executa o simulador. 

Todas as instruçòes estào bem documentadas, mas havendo qualquer dificultade abra um Issue para te ajduarmos.

## Demonstração da solução funcionando

[Entrega 0.1.0](https://www.youtube.com/watch?v=It2_9pf46x4)

[Entrega 0.2.0](https://youtu.be/syZCVDUYr8E)



## 🗃 Histórico de lançamentos

* 0.1.0 - 20/05/2025
    * Entrega do escopo incial do projeto, com diagrama, e principais funcionalidades:
        * API que armazena e permite a consulta de todos os dados para futura analise
        * simulador que conecta a esta API para enviar dados coletados
        * simulador ainda preve uma automação via relé para simular a ativação de sistema de irrigação

* 0.2.0 - 20/06/2025
    * Atualização do projeto com novas implementações
        * ESP32:
            * Adicionado Monitor LCD -> umidade e pH
            * Exibindo umidade e pH no serialPlotter
            * Otimização na coleta de pH -> Convertendo o valor do sensor para um valor entre 0 a 14
        * Python
            * DB
                * Novo scripts para popular banco de dados com informações ficticias no período de 1 ano
            * Streamlit
                * Implementação do streamlit para visualizar as coletas de forma gráfica
            * Modelo de ML
                * Implementação de um Modelo de Floresta aleatória para prever qual produto utilizar com base na coleta atual
            


## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

