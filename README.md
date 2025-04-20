# README - Dashboard Interativo da Adidas 📊👟

## Sobre o Projeto 🚀

Este projeto consiste em um dashboard interativo desenvolvido em Python para análise de dados da Adidas, utilizando diversas bibliotecas modernas para visualização e manipulação de dados. O objetivo é apresentar informações relevantes de forma visual e intuitiva, facilitando a tomada de decisões estratégicas.

## Tecnologias Utilizadas 🛠️

- **Python**: Linguagem principal para desenvolvimento do dashboard.
- **Streamlit**: Framework para criação rápida de aplicações web interativas.
- **Pandas**: Manipulação e análise de dados em formato tabular.
- **Plotly Express e Graph Objects**: Geração de gráficos interativos e visualmente atrativos.
- **Pillow (PIL)**: Manipulação de imagens para exibição no dashboard.
- **Locale**: Configuração regional para formatação de datas em português do Brasil.
- **Folium**: Visualização de mapas interativos.
- **Geopy**: Geocodificação para localização geográfica.
- **Streamlit Folium**: Integração do Folium com Streamlit para exibição de mapas.

## Funcionalidades Principais 🔍

- Upload e leitura de arquivos Excel com dados da Adidas.
- Exibição do logo da Adidas para identidade visual.
- Visualizações gráficas interativas que facilitam a análise de vendas, localização e outras métricas.
- Mapa interativo para análise geográfica dos dados.
- Interface responsiva e amigável, ajustada para diferentes tamanhos de tela.

## Como Executar Localmente 💻

Siga os passos abaixo para rodar o dashboard em sua máquina:

1. **Clone este repositório:**

```bash
git clone 
cd 
```

2. **Instale as dependências necessárias:**

```bash
pip install streamlit pandas plotly pillow folium geopy streamlit-folium
```

3. **Certifique-se de ter o arquivo `Adidas.xlsx` dentro da pasta `dataset/` e a imagem `adidas-logo.jpg` na raiz do projeto.**

4. **Execute o aplicativo Streamlit:**

```bash
streamlit run dashboard.py
```

5. **Abra o navegador no endereço que o Streamlit indicar (geralmente http://localhost:8501).**

## Análise do Código 📈

O script `dashboard.py` inicia configurando a localidade para português do Brasil, garantindo que as datas e textos estejam no formato correto para o público-alvo. Em seguida, carrega os dados do Excel e a imagem do logo Adidas para exibição.

A interface é montada com colunas para organizar o layout, e utiliza gráficos Plotly para apresentar dados de forma interativa, permitindo ao usuário explorar diferentes aspectos do dataset. A integração com Folium e Geopy possibilita a visualização de dados geográficos, enriquecendo a análise com mapas dinâmicos.

O uso do Streamlit torna a aplicação leve e fácil de usar, ideal para compartilhar insights rapidamente sem a necessidade de configurações complexas.

---

Este projeto é uma excelente demonstração de como combinar análise de dados, visualização e geolocalização em uma aplicação web simples e eficiente. Aproveite para explorar e expandir conforme suas necessidades! 🎉

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/58011902/783a9c60-dcb8-4d62-9a98-a435ff3ff58f/dashboard.py

---
Resposta do Perplexity: pplx.ai/share
