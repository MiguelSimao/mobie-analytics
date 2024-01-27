# Análise da Mobilidade Elétrica em Portugal

Este repositório contém uma análise abrangente da mobilidade elétrica em Portugal, utilizando Jupyter Notebooks e dados relevantes. A análise aborda diferentes aspetos, desde infraestrutura de carregamento até tarifas elétricas, proporcionando uma compreensão detalhada do cenário de mobilidade elétrica no país.

Resultados apresentados com o Github Pages e disponibilizados [neste link](https://miguelsimao.github.io/mobie-analytics).


## Estrutura de ficheiros

```
├── LICENSE.md
├── README.md
├── data                                        # dados extraídos
├── notebooks                                   # notebooks, toc e config para jupyter-book
│   ├── _config.yml
│   ├── _toc.yml
│   ├── europe_comparison
│   │   ├── rawdata
│   │   │   ├── estat_road_if_roadsc_en.csv
│   │   │   ├── evses_2022.csv
│   │   │   ├── fleet_per_country_2022.csv
│   │   │   └── roads_wikipedia.csv
│   │   └── roads.ipynb
│   ├── intro.md
│   ├── mobidata
│   │   ├── 20230821-plugs-per-user.ipynb
│   │   └── data
│   │       └── mobidata_utilizadores_tomadas.csv
│   ├── mobie
│   │   └── extract.py
│   └── static
├── requirements.txt
├── scripts                                     # scripts de extração de dados
│   ├── extract_chargers.py
│   ├── extract_gsheets.py
│   ├── extract_road_length_wikipedia.py
│   └── extract_tariffs.py
└── src                                         # source code partilhado entre notebooks
    ├── __init__.py
    └── data_collection
        ├── __init__.py
        ├── db.py
        └── tariffs.py
```


## Artigos / Notebooks

* Mobidata: Análise específica sobre a utilização de tomadas e utilizadores de veículos elétricos, com dados base nos dados da MobiE.

* [WIP] Europe Comparison: Análises comparativas entre Portugal e restantes países Europeus.

* [WIP] Comparação entre CEMEs a operar em Portugal


## Scripts

* extract_chargers.py: Extração de dados sobre pontos de carregamento.

* extract_gsheets.py: Extração de dados de folhas de cálculo do Google.

* extract_road_length_wikipedia.py: Extração de dados sobre o comprimento de estradas da Wikipedia.

* extract_tariffs.py: Extração de dados das tarifas CPO.


## Instruções para Reprodução

### Python 3.10 / Ubuntu


```bash
python3 -m venv venv

source venv/bin/activate

python -m pip install -r requirements.txt

jupyter-book build notebooks
```


## Contribuir


Sinta-se à vontade para contribuir para este projeto! Se encontrar problemas, tiver sugestões ou quiser adicionar novas funcionalidades, por favor, abra uma "issue" ou submeta um "pull request".


## Licença

Este projeto é licenciado sob a [licença MIT](https://github.com/MiguelSimao/mobie-analytics/blob/main/LICENSE.md).
