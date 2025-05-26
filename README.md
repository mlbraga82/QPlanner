# QPlanner

QPlanner é um script Python para o QGIS que permite criar pontos ao longo de uma camada de linha com intervalos fixos definidos pelo usuário, incluindo atributos de distância e horário de passagem. Inspirado no plugin QChainage, o QPlanner adiciona funcionalidades avançadas, como o cálculo de horários de passagem com base em um horário de partida e velocidade média, com conversão automática para o sistema de coordenadas EPSG:3857 (Web Mercator) para cálculos precisos em metros. O script também força a criação do ponto final da linha e configura rótulos no formato HH:MM para visualização clara dos horários.

## Funcionalidades
- **Criação de pontos ao longo de linhas**: Gera pontos em intervalos fixos (em metros) ao longo de uma camada de linha, incluindo o ponto final, mesmo que fora do intervalo fixo.
- **Atributos de distância e horário**: Cada ponto recebe atributos de:
  - **Distancia**: Distância acumulada ao longo da linha (em metros).
  - **Horario**: Horário previsto de passagem (formato HH:MM:SS), calculado com base no horário de partida e na velocidade média (em km/h).
- **Conversão para EPSG:3857**: Converte automaticamente as geometrias para EPSG:3857 para cálculos precisos em metros, mantendo o CRS original na camada de saída.
- **Rótulos personalizados**: Exibe rótulos no formato HH:MM para os horários de passagem, facilitando a visualização de itinerários.
- **Validação de entradas**: Verifica se a camada selecionada é válida (tipo linha) e se o horário de partida está no formato correto (HH:MM).
- **Interface amigável**: Solicita entradas do usuário (distância de intervalo, horário de partida e velocidade média) por meio de caixas de diálogo interativas.

## Requisitos
- **QGIS**: Versão 3.x ou superior.
- **Python**: Incluído com o QGIS (PyQt5 e bibliotecas padrão do QGIS).
- **Dependências**: Nenhuma dependência externa além das bibliotecas padrão do QGIS (`qgis.core`, `PyQt5`, `datetime`).

## Instalação
1. Baixe o arquivo `QPlanner.py` deste repositório.
2. Abra o QGIS e acesse o Console Python (`Plugins > Python Console` ou `Ctrl+Alt+P`).
3. Copie e cole o conteúdo do `QPlanner.py` no console ou carregue-o como um script.

Alternativamente, você pode salvar o arquivo `QPlanner.py` na pasta de scripts do QGIS para uso recorrente:
- Localização padrão da pasta de scripts:
  - Windows: `C:\Users\[SeuUsuário]\AppData\Roaming\QGIS\QGIS3\profiles\default\python`
  - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python`
  - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python`

## Como Usar
1. **Prepare sua camada**:
   - Certifique-se de que uma camada de linha (simples ou multiparte) está selecionada no painel de camadas do QGIS.
2. **Execute o script**:
   - Abra o Console Python no QGIS.
   - Cole o código do `QPlanner.py` ou carregue-o como um script.
   - Pressione Enter para executar.
3. **Insira os parâmetros**:
   - **Distância de intervalo**: Digite a distância fixa entre os pontos (em metros, ex.: 100).
   - **Horário de partida**: Insira o horário inicial no formato HH:MM (ex.: 08:00).
   - **Velocidade média**: Informe a velocidade em km/h (ex.: 60.0).
4. **Visualize o resultado**:
   - Uma nova camada de pontos chamada "Pontos_ao_Longo_da_Linha" será criada no projeto.
   - Os pontos incluirão atributos de distância (em metros) e horário de passagem (HH:MM:SS).
   - Rótulos no formato HH:MM serão exibidos automaticamente para cada ponto.

## Exemplo de Saída
Para uma linha de 250 metros, com:
- Distância de intervalo: 100 metros
- Horário de partida: 08:00
- Velocidade média: 60 km/h

A camada gerada terá pontos com atributos como:
| Distancia | Horario   | Rótulo (exibido) |
|-----------|-----------|------------------|
| 0.0       | 08:00:00  | 08:00            |
| 100.0     | 08:00:06  | 08:00            |
| 200.0     | 08:00:12  | 08:00            |
| 250.0     | 08:00:15  | 08:00            |

## Integração com Outros Plugins
O QPlanner pode ser combinado com plugins como:
- **OSM Route** ou **ORS Tools**: Para gerar rotas entre cidades como camada de linha inicial.
- **QGIS2Google**: Para exportar os pontos gerados para o Google My Maps, criando itinerários visuais e compartilháveis.

## Limitações
- **CRS**: O script assume que o CRS da camada de entrada é compatível com transformações para EPSG:3857. Para CRSs não projetados (como WGS84 em graus), os cálculos podem não ser precisos sem ajustes adicionais.
- **Velocidade**: A velocidade é interpretada como constante (média em km/h). Variações reais no terreno ou tráfego não são consideradas.
- **Performance**: Para camadas com muitas linhas longas, a transformação de coordenadas pode adicionar um pequeno custo computacional.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para:
- Adicionar novos atributos aos pontos (ex.: elevação, nome de locais).
- Implementar exportação automática para formatos como GeoJSON ou KML.
- Melhorar a interface do usuário com um painel de entrada personalizado.

## Licença
Este projeto é licenciado sob a [MIT License](LICENSE).

## Contato
Para sugestões ou dúvidas, abra uma issue no repositório ou entre em contato pelo GitHub.

---

**QPlanner**: Planeje itinerários precisos no QGIS com pontos, distâncias e horários personalizados!
