"""
Coletor de Dados de Capitais Brasileiras - Versão Melhorada

Este script coleta dados sobre as capitais brasileiras incluindo:
- Custo de vida
- Segurança
- Qualidade de vida
- Índices de transporte

Com métodos aprimorados para extração de dados.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
import json
from urllib.parse import quote


class BrazilCapitalsCollector:
    def __init__(self):
        # Dicionário das capitais brasileiras (Estado: Capital)
        self.capitals = {
            "Acre": "Rio Branco",
            "Alagoas": "Maceió",
            "Amapá": "Macapá",
            "Amazonas": "Manaus",
            "Bahia": "Salvador",
            "Ceará": "Fortaleza",
            "Distrito Federal": "Brasília",
            "Espírito Santo": "Vitória",
            "Goiás": "Goiânia",
            "Maranhão": "São Luís",
            "Mato Grosso": "Cuiabá",
            "Mato Grosso do Sul": "Campo Grande",
            "Minas Gerais": "Belo Horizonte",
            "Pará": "Belém",
            "Paraíba": "João Pessoa",
            "Paraná": "Curitiba",
            "Pernambuco": "Recife",
            "Piauí": "Teresina",
            "Rio de Janeiro": "Rio de Janeiro",
            "Rio Grande do Norte": "Natal",
            "Rio Grande do Sul": "Porto Alegre",
            "Rondônia": "Porto Velho",
            "Roraima": "Boa Vista",
            "Santa Catarina": "Florianópolis",
            "São Paulo": "São Paulo",
            "Sergipe": "Aracaju",
            "Tocantins": "Palmas"
        }
        
        # Lista para armazenar todos os dados
        self.all_data = []
        
        # Cabeçalhos para simular um navegador real (mais detalhados)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        }
        
        # Sessão para manter cookies entre requisições
        self.session = requests.Session()
    
    def format_city_for_url(self, city_name):
        """Formata o nome da cidade para uso em URLs."""
        formatted = city_name.replace(" ", "-")\
                       .replace("ã", "a")\
                       .replace("é", "e")\
                       .replace("í", "i")\
                       .replace("ó", "o")\
                       .replace("ç", "c")\
                       .replace("á", "a")\
                       .replace("ê", "e")\
                       .replace("ú", "u")
        return formatted
    
    def extract_float_from_text(self, text):
        """Extrai um valor float de um texto."""
        if not text:
            return None
        # Remove caracteres não numéricos, exceto ponto decimal
        cleaned_text = re.sub(r'[^\d.]', '', text.strip())
        try:
            if cleaned_text:
                return float(cleaned_text)
            return None
        except ValueError:
            return None
    
    def get_cost_of_living_data(self, city_name):
        """Coleta dados de custo de vida para uma cidade."""
        city_url = self.format_city_for_url(city_name)
        url = f'https://www.numbeo.com/cost-of-living/in/{city_url}-Brazil'
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"Erro ao acessar {url}: Status code {response.status_code}")
                return None, None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Método 1: Buscar pelo índice na tabela
            cost_index = None
            rent_index = None
            
            # Procurar todas as tabelas
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    row_text = row.text.strip()
                    if "Cost of Living Index" in row_text:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            cost_index = self.extract_float_from_text(cells[1].text)
                    elif "Rent Index" in row_text:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            rent_index = self.extract_float_from_text(cells[1].text)
            
            # Método 2: Se o método 1 falhar, buscar por texto
            if cost_index is None:
                cost_pattern = re.compile(r'Cost of Living Index.*?(\d+\.\d+)')
                cost_match = cost_pattern.search(response.text)
                if cost_match:
                    cost_index = float(cost_match.group(1))
            
            if rent_index is None:
                rent_pattern = re.compile(r'Rent Index.*?(\d+\.\d+)')
                rent_match = rent_pattern.search(response.text)
                if rent_match:
                    rent_index = float(rent_match.group(1))
            
            return cost_index, rent_index
            
        except Exception as e:
            print(f"Erro ao coletar dados de custo de vida para {city_name}: {e}")
            return None, None
    
    def get_safety_data(self, city_name):
        """Coleta dados de segurança para uma cidade."""
        city_url = self.format_city_for_url(city_name)
        url = f'https://www.numbeo.com/crime/in/{city_url}-Brazil'
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"Erro ao acessar {url}: Status code {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Método 1: Buscar pelo índice na tabela
            safety_index = None
            
            # Procurar todas as tabelas
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    row_text = row.text.strip()
                    if "Safety Index" in row_text:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            safety_index = self.extract_float_from_text(cells[1].text)
            
            # Método 2: Se o método 1 falhar, buscar por texto
            if safety_index is None:
                safety_pattern = re.compile(r'Safety Index.*?(\d+\.\d+)')
                safety_match = safety_pattern.search(response.text)
                if safety_match:
                    safety_index = float(safety_match.group(1))
            
            return safety_index
            
        except Exception as e:
            print(f"Erro ao coletar dados de segurança para {city_name}: {e}")
            return None
    
    def get_quality_of_life_data(self, city_name):
        """Coleta dados de qualidade de vida para uma cidade."""
        city_url = self.format_city_for_url(city_name)
        url = f'https://www.numbeo.com/quality-of-life/in/{city_url}-Brazil'
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"Erro ao acessar {url}: Status code {response.status_code}")
                return None, None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Método 1: Buscar pelos índices na tabela
            qol_index = None
            transport_index = None
            
            # Procurar todas as tabelas
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    row_text = row.text.strip()
                    if "Quality of Life Index" in row_text:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            qol_index = self.extract_float_from_text(cells[1].text)
                    elif "Traffic Commute Time Index" in row_text:
                        cells = row.find_all('td')
                        if len(cells) >= 2:
                            transport_index = self.extract_float_from_text(cells[1].text)
            
            # Método 2: Se o método 1 falhar, buscar por texto
            if qol_index is None:
                qol_pattern = re.compile(r'Quality of Life Index.*?(\d+\.\d+)')
                qol_match = qol_pattern.search(response.text)
                if qol_match:
                    qol_index = float(qol_match.group(1))
            
            if transport_index is None:
                transport_pattern = re.compile(r'Traffic Commute Time Index.*?(\d+\.\d+)')
                transport_match = transport_pattern.search(response.text)
                if transport_match:
                    transport_index = float(transport_match.group(1))
            
            return qol_index, transport_index
            
        except Exception as e:
            print(f"Erro ao coletar dados de qualidade de vida para {city_name}: {e}")
            return None, None

    def get_coworking_data(self, city_name):
        """Tenta coletar dados aproximados de espaços de coworking via Google Places API."""
        # Nota: Este método é apenas demonstrativo e requer uma chave API válida do Google
        # Para uma implementação real, você precisaria de uma chave API do Google
        
        # Valores simulados baseados em estimativas
        coworking_spaces = {
            "São Paulo": {"count": 120, "avg_price": 800},
            "Rio de Janeiro": {"count": 80, "avg_price": 750},
            "Belo Horizonte": {"count": 45, "avg_price": 600},
            "Brasília": {"count": 40, "avg_price": 700},
            "Curitiba": {"count": 35, "avg_price": 550},
            "Porto Alegre": {"count": 30, "avg_price": 580},
            "Recife": {"count": 25, "avg_price": 500},
            "Salvador": {"count": 22, "avg_price": 490},
            "Fortaleza": {"count": 20, "avg_price": 450},
            "Goiânia": {"count": 18, "avg_price": 420},
            "Florianópolis": {"count": 15, "avg_price": 600},
            "Vitória": {"count": 12, "avg_price": 480},
            "Belém": {"count": 10, "avg_price": 400},
            "Manaus": {"count": 10, "avg_price": 410},
            "Natal": {"count": 8, "avg_price": 420},
            "João Pessoa": {"count": 8, "avg_price": 380},
            "Campo Grande": {"count": 7, "avg_price": 350},
            "Maceió": {"count": 7, "avg_price": 370},
            "Cuiabá": {"count": 6, "avg_price": 360},
            "São Luís": {"count": 6, "avg_price": 340},
            "Teresina": {"count": 5, "avg_price": 320},
            "Aracaju": {"count": 5, "avg_price": 330},
            "Porto Velho": {"count": 4, "avg_price": 300},
            "Boa Vista": {"count": 3, "avg_price": 280},
            "Macapá": {"count": 3, "avg_price": 270},
            "Rio Branco": {"count": 3, "avg_price": 260},
            "Palmas": {"count": 4, "avg_price": 290}
        }
        
        # Retorna dados simulados para a cidade especificada ou dados padrão
        if city_name in coworking_spaces:
            return coworking_spaces[city_name]["count"], coworking_spaces[city_name]["avg_price"]
        else:
            # Valores padrão para cidades não listadas
            return 5, 350
    
    def collect_data(self):
        """Coleta dados para todas as capitais."""
        for state, capital in self.capitals.items():
            print(f"Coletando dados para {capital}, {state}...")
            
            # Criar um dicionário para armazenar os dados desta cidade
            city_data = {
                'estado': state,
                'capital': capital,
                'indice_custo_de_vida': None,
                'indice_aluguel': None,
                'indice_seguranca': None,
                'indice_qualidade_de_vida': None,
                'indice_transporte': None,
                'espacos_coworking': None,
                'preco_medio_coworking': None
            }
            
            # Coletar dados de custo de vida
            cost_index, rent_index = self.get_cost_of_living_data(capital)
            city_data['indice_custo_de_vida'] = cost_index
            city_data['indice_aluguel'] = rent_index
            
            # Adicionar um atraso para evitar bloqueios
            time.sleep(random.uniform(3, 5))
            
            # Coletar dados de segurança
            safety_index = self.get_safety_data(capital)
            city_data['indice_seguranca'] = safety_index
            
            # Adicionar um atraso para evitar bloqueios
            time.sleep(random.uniform(3, 5))
            
            # Coletar dados de qualidade de vida
            qol_index, transport_index = self.get_quality_of_life_data(capital)
            city_data['indice_qualidade_de_vida'] = qol_index
            city_data['indice_transporte'] = transport_index
            
            # Adicionar um atraso para evitar bloqueios
            time.sleep(random.uniform(3, 5))
            
            # Coletar dados simulados de coworking (baseados em estimativas)
            spaces_count, avg_price = self.get_coworking_data(capital)
            city_data['espacos_coworking'] = spaces_count
            city_data['preco_medio_coworking'] = avg_price
            
            # Adicionar os dados desta cidade à nossa coleção
            self.all_data.append(city_data)
            
            print(f"Dados coletados para {capital}:")
            print(f"  Custo de Vida: {cost_index}")
            print(f"  Aluguel: {rent_index}")
            print(f"  Segurança: {safety_index}")
            print(f"  Qualidade de Vida: {qol_index}")
            print(f"  Transporte: {transport_index}")
            print(f"  Espaços Coworking: {spaces_count}")
            print(f"  Preço Médio Coworking: R${avg_price}")
    
    def save_to_csv(self, filename='dados_capitais_brasileiras.csv'):
        """Salva os dados coletados em um arquivo CSV."""
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Dados salvos em {filename} - {len(self.all_data)} registros.")
        else:
            print("Nenhum dado para salvar.")

    def load_existing_data(self, filename='dados_capitais_brasileiras.csv'):
        """Carrega dados de um CSV existente para complementar."""
        try:
            df = pd.read_csv(filename, encoding='utf-8-sig')
            self.all_data = df.to_dict('records')
            print(f"Carregados {len(self.all_data)} registros do arquivo {filename}.")
            return True
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return False


# Executar o coletor se o script for executado diretamente
if __name__ == "__main__":
    collector = BrazilCapitalsCollector()
    
    # Se quiser complementar dados existentes, descomente a linha abaixo
    # collector.load_existing_data()
    
    collector.collect_data()
    collector.save_to_csv()