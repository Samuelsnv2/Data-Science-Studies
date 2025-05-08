# Remote Work Cities in Brazil (2025) Analysis

This project analyzes which Brazilian cities are most suitable for remote work based on a combination of factors such as cost of living, infrastructure, climate, safety, and quality of life. The analysis is conducted using a dataset containing various metrics related to 20 major cities in Brazil.

---

## 📊 Overview

The goal of this project is to rank cities for their suitability for remote work by calculating a **Remote Work Score** derived from several key indicators. This score incorporates weighted categories like:
- **Cost of Living**
- **Internet Speed**
- **Climate**
- **Safety**
- **Quality of Life**

Each city is normalized and scored using a Min-Max Scaler, and negative metrics are inverted appropriately to ensure higher scores indicate better conditions for remote work.

---

### Sources

- **Internet data**: [https://www.minhaconexao.com.br/ranking ](https://www.minhaconexao.com.br/ranking )
  - Contains information about internet quality and coverage for cities.

- **Climate data**: [https://bdmep.inmet.gov.br/ ](https://bdmep.inmet.gov.br/ )
  - Used to gather climate-related data. Some issues with names were encountered, so manual corrections were made.

- **Coworking data**: Collected via Google search web scraping.
  - Includes prices for coworking spaces in Brazilian Real (BRL).

- **Safety data**: [https://publicacoes.forumseguranca.org.br/items/f62c4196-561d-452d-a2a8-9d33d1163af0 ](https://publicacoes.forumseguranca.org.br/items/f62c4196-561d-452d-a2a8-9d33d1163af0 )
  - Provides data on safety indices and related statistics.

- **IPS (Índice de Progresso Social) data**: [https://ipsbrasil.org.br/pt/explore/dados?sort_order=asc&sort_by=id&page=1&per_page=10 ](https://ipsbrasil.org.br/pt/explore/dados?sort_order=asc&sort_by=id&page=1&per_page=10 )
  - Offers social progress index scores for municipalities.

- **Cost of life data**: Numbeo earlier 2025 dataset.
  - Gives cost of living details for cities in Brazil as of early 2025.

---

## 🧠 Key Metrics Used

| Metric | Description |
|--------|-------------|
| `1BR Apartment (Center)` | Cost of a one-bedroom apartment in the city center |
| `1BR Apartment (Outside)` | Cost of a one-bedroom apartment outside the city center |
| `Utilities (Monthly)` | Monthly utility costs (electricity, water, etc.) |
| `Internet (Monthly)` | Monthly internet costs |
| `Groceries (Monthly)` | Average monthly grocery expenses |
| `Public Transport (Monthly)` | Monthly public transport costs |
| `Índice de Progresso Social` | Social progress index |
| `Moradia` | Housing conditions |
| `Saúde e Bem-estar` | Health and well-being |
| `Água e Saneamento` | Water and sanitation |
| `speed_mbps` | Internet speed in Mbps |
| `Segurança Pessoal` | Personal safety index |
| `Taxa_2023` | Mortality rate in 2023 |
| `Climate Score` | Climate condition score |

---

## 🔧 Methodology

### 1. Data Preparation
- Cleaned and merged datasets containing city-specific information.
- Standardized city names across all datasets.
- Removed rows with excessive missing values.

### 2. Normalization
- All numerical features were normalized using the **Min-Max Scaler** to bring them into a common scale between 0 and 1.

### 3. Weight Assignment
- Categories were assigned weights based on their importance to remote work suitability:
  - Cost of Living: 20%
  - Infrastructure: 15%
  - Safety: 15%
  - Quality of Life: 35%
  - Climate: 15%

### 4. Score Calculation
- A **Remote Work Score** was calculated for each city by summing up the weighted contributions of the individual metrics.

---
### 📊 Justification for Weight Selection

Each category was assigned a weight based on its overall importance to the quality of life and feasibility of working remotely in a city. The final Remote Work Score is calculated as a weighted sum of the following categories:

- **Quality of Life (35%)**:  
  This category includes essential factors for physical and mental well-being, such as healthcare, adequate housing, clean water, and sanitation. These are foundational to any long-term living situation.

- **Cost of Living (20%)**:  
  Daily expenses like rent, utilities, groceries, and transportation directly impact the financial sustainability of a remote worker. While important, it’s secondary to basic quality of life needs.

- **Infrastructure (15%)**:  
  Access to reliable internet and efficient public transport is crucial for remote workers but not as fundamental as health or safety.

- **Safety (15%)**:  
  Personal safety and low crime rates are vital for peace of mind and longevity. A safe environment is necessary for remote professionals to thrive.

- **Climate (10%)**:  
  Favorable weather conditions improve quality of life, though this factor may be less critical for individuals with different lifestyle preferences.

- **Death Rate (5%)**:  
  Serves as an indirect indicator of public health. However, since some aspects of public health are already covered under "Quality of Life," this metric is given a smaller weight.

---

### ✅ Final Score Calculation Formula

The final Remote Work Score is computed using the formula below:

---

## 🏆 Top 10 Cities for Remote Work in Brazil (2025)

| Rank | City         | Remote Work Score |
|------|--------------|-------------------|
| 1    | Goiânia      | 0.7818            |
| 2    | Cuiabá       | 0.7558            |
| 3    | Florianópolis | 0.7452           |
| 4    | Brasília     | 0.7160            |
| 5    | Belo Horizonte | 0.6990          |
| 6    | Palmas       | 0.6588            |
| 7    | Curitiba     | 0.6546            |
| 8    | Campo Grande | 0.6323            |
| 9    | São Paulo    | 0.6144            |
| 10   | Porto Alegre | 0.5970            |

---

## 📈 Comparison of Top 5 Cities

The top five cities were further analyzed for their performance in the following categories:

| Category              | Goiânia | Cuiabá | Florianópolis | Brasília | Belo Horizonte |
|-----------------------|---------|--------|------------------|----------|----------------|
| Cost of Living        | 0.67    | 0.63   | 0.60             | 0.62     | 0.65           |
| Internet Speed        | 0.80    | 0.77   | 0.73             | 0.72     | 0.71           |
| Climate               | 0.75    | 0.73   | 0.70             | 0.68     | 0.69           |
| Safety                | 0.85    | 0.83   | 0.82             | 0.81     | 0.79           |
| Quality of Life       | 0.78    | 0.76   | 0.74             | 0.75     | 0.77           |

---

## 🛠️ Requirements

To run the analysis, ensure you have the following Python libraries installed:

```bash
pip install requirements.txt
```

## 📌 Contributions

Contributions are welcome! If you find any errors or want to suggest improvements, please open an issue or submit a pull request.