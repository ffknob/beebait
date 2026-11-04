1. Com base nos conceitos iniciais do Módulo 1, como você descreveria a relação fundamental entre a Internet das Coisas (IoT) e a Inteligência Artificial (IA)?

Os dispositivos IoT muitas vezes (ainda que essa não seja a única arquitetura possível) atuam como meros coletores de métricas de um determinado ambiente em que se encontram inseridos e têm a função de enviar essas métricas, cruas ou processadas localmente (edge), para uma central de processamento local (fog) ou remota (cloud), que por sua vez utilizará sua capacidade de processamento para produzir descobertas em cima das métricas coletadas. O processamento muitas vezes envolverá aprendizado de máquina, que, uma vez que métricas suficientes tenham sido rotuladas e repassadas ao modelo via treinamento, possibilitará a descoberta de outliers e a predição de eventos. 

2. Apresente pelo menos um exemplo prático e detalhado de uma aplicação onde essa sinergia cria um valor que nenhuma das tecnologias conseguiria isoladamente.

Depois de passar a vida inteira cultivando milho e soja na sua propriedade no norte do estado, meu sogro se aposentou e passou a arrendar as terras. No entanto, ao mesmo tempo ele passou a desenvolver a apicultura como hobby e combinou com o locatário das terras que poderia instalar iscas de colmeias (caixas próprias para isso, ou, de forma mais rudimentar com garrafas PET) ao longo da propriedade. Essas caixas ficam espalhadas ao longo de uma grande área, instaladas em árvores e têm como objetivo atrair um enxame. Iscas que tenham atraído um enxame são então levadas para um apiário para serem acompanhadas até que tenham produzido mel.

O problema óbvio que ele enfrenta é que para descobrir quais iscas capturaram um enxame ele precisa verificar cada uma. Outro problema é que, como a preparação de uma isca é muito simples e como a propriedade oferece diversos pontos interessantes de captura, ele às vezes espalha muitas delas e acaba esquecendo a localização.

Portanto, meu exemplo aplicação que demonstraria a sinergia entre IoT e IA seria o desenvolvimento de controladores de iscas de colmeias, que seriam acoplados a cada isca e se comunicariam com uma central instalada na sede da propriedade, de forma que meu sogro pudesse realizar visitas apenas à sede e então aos locais de iscas ocupadas.

Funcionalidades desejadas

1. Identificação: Cada isca passaria a ser identificada unicamente.

2. Localização: Cada isca teria sua localização registrada tanto através de geolocalização, quanto através de fotos do local (ao ser instalada), para facilitar a localização. 
2.1. (opcional) Caso o controlador identifique uma mudança no geolocalização (roubo, vento, ...), a central seria avisada. Mas isso demandaria ao controlador ter a capacidade de identificar sua geolocalização através de GPS.
2.2. (opcional) Quando estiver procurando pela isca, o apicultor poderia ter a possibilidade de acionar um aviso sonoro na isca para facilitar a sua localização.

3. Identificar a ocupação: Uma ideia seria o controlador possuir um microfone instalado dentro da isca e conseguisse indicar a sua ocupação meramente pela presença de algum ruído, mas idealmente através de algum modelo de inferência baseado em bioacústica computacional. Talvez seja possível inclusive contabilizar a população da colmeia, caso a entrada da isca fosse através de um túnel (cano de PVC) no qual conseguíssemos instalar dois pontos de medição a laser. 

4. Comunicar a ocupação: Visualmente, através de uma lâmpada LED piscante, mas principalmente remotamente, enviando a informação para a central.

5. Bioacústica: Utilizar o microfone interno para capturar o áudio da colmeia e executar um modelo de inferência treinado com fins de bioacústica computacional voltada para a apicultura para determinar características como saúde, presença de rainha, ... O modelo de inferência teria que ser executado na borda (controlador instalado na isca), uma vez que o tipo de rede que será utilizado não permitirá transmitir áudio, mas apenas poucos bytes por vez (ou seja, apenas uma conclusão como "isca 123: O .92", significando que a isca nº 123 estaria ocupada (O) com uma confiança de 92%).

Implementação

Percepção (sensores e emissores): Microfones (para processamento da bioacústica), sensores de passagem (laser), sensores de umidade  e temperatura (uma colônia com cria mantém o ninho em torno de 34–35 °C, então uma temperatura interna estável e acima da externa é um forte indício de ocupação), luzes LED para indicação da situação ocupacional, caixa de som para emissão de sinal sonoro para facilitar a localização.
Rede: LoRaWAN, devido à falta da cobertura 5G e à distância entre as iscas e a sede da propriedade.
Comunicação: MQTT
Middleware: Processa o sinal de áudio capturado pelos microfones e aplica um modelo de inferência lightweight localmente (TinyML) que consiga determinar a situação ocupacional da isca. Avalia também outros sensores, como o de umidade e temperatura. Utiliza todas as métricas para compor um grau de confiança quanto à ocupação da isca.
Aplicação: Mapa da propriedade e com as iscas localizadas em suas respectivas geolocalizações. Cada isca é apresentada no mapa como um ícone indicando de forma visual (cor) sua situação com relação à ocupação.
Energização: Em aberto.
Custo: Em aberto.

