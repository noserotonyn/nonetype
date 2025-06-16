import requests
from bs4 import BeautifulSoup

def get_current_relics():
    # URL oficial das recompensas de missão
    URL = "https://warframe-webassets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"
    
    print("🔄 Obtendo dados da Warframe...")
    response = requests.get(URL)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontra todas as tabelas de recompensas
    reward_tables = soup.find_all('table', class_='reward-table')
    
    # Dicionário para armazenar as relíquias por era
    relics = {
        'Lith': set(),
        'Meso': set(),
        'Neo': set(),
        'Axi': set()
    }
    
    # Extrai relíquias de cada tabela
    for table in reward_tables:
        rows = table.find_all('tr')[1:]  # Ignora o cabeçalho
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:  # Pelo menos nome e chance
                relic_name = cols[0].get_text(strip=True)
                
                # Filtra apenas relíquias intactas
                if 'Relic' in relic_name and 'Intact' in relic_name:
                    for era in relics.keys():
                        if era in relic_name:
                            relics[era].add(relic_name.replace(' Intact', ''))
                            break
    
    return relics

def generate_html_table(relics):
    # Ordena as relíquias em cada era
    for era in relics:
        relics[era] = sorted(relics[era])
    
    # Determina o número máximo de linhas necessário
    max_rows = max(len(relics[era]) for era in relics)
    
    # Gera a tabela HTML
    html = """
    <table border="1" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr>
                <th style="padding: 8px; background: #f2f2f2;">Lith</th>
                <th style="padding: 8px; background: #f2f2f2;">Meso</th>
                <th style="padding: 8px; background: #f2f2f2;">Neo</th>
                <th style="padding: 8px; background: #f2f2f2;">Axi</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for i in range(max_rows):
        html += "<tr>"
        for era in ['Lith', 'Meso', 'Neo', 'Axi']:
            relic = relics[era][i] if i < len(relics[era]) else ''
            html += f'<td style="padding: 6px;">{relic}</td>'
        html += "</tr>"
    
    html += """
        </tbody>
    </table>
    """
    
    return html

# Execução principal
if __name__ == "__main__":
    try:
        relics = get_current_relics()
        html_table = generate_html_table(relics)
        
        # Salva em arquivo
        with open('current_relics.html', 'w', encoding='utf-8') as f:
            f.write(html_table)
        
        print("✅ Tabela HTML gerada com sucesso: current_relics.html")
        print(f"Relíquias encontradas: Lith({len(relics['Lith']}) | Meso({len(relics['Meso'])}) | Neo({len(relics['Neo'])}) | Axi({len(relics['Axi'])})")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
