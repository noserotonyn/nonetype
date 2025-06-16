import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "relics.html")

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_page_content():
    print(f"🔄 Baixando dados em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text

def extract_relics(html):
    soup = BeautifulSoup(html, 'html.parser')
    relics = {
        'Lith': set(),
        'Meso': set(),
        'Neo': set(),
        'Axi': set()
    }

    # Encontra todas as tabelas de recompensas
    reward_tables = soup.find_all('table', class_='reward-table')
    
    if not reward_tables:
        raise Exception("Nenhuma tabela de recompensas encontrada")

    for table in reward_tables:
        rows = table.find_all('tr')[1:]  # Pula o cabeçalho
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                item_name = cols[0].get_text(strip=True)
                
                # Filtra apenas relíquias intactas
                if 'Relic' in item_name and 'Intact' in item_name:
                    for era in relics.keys():
                        if era in item_name:
                            clean_name = item_name.replace(' Intact', '').replace(' Relic', '')
                            relics[era].add(clean_name)
    
    return relics

def generate_html(relics):
    # Ordena as relíquias em cada era
    for era in relics:
        relics[era] = sorted(relics[era])

    max_rows = max(len(relics[era]) for era in relics)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Relíquias Warframe Atuais</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #FF6D00; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th {{ background-color: #f2f2f2; padding: 10px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        .timestamp {{ color: #666; font-size: 0.9em; margin-top: 20px; }}
        .era-header {{ color: #FF6D00; margin-top: 30px; }}
    </style>
</head>
<body>
    <h1>Relíquias Warframe Atuais</h1>
    <p>Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
"""

    # Tabela para cada era
    for era in relics:
        if relics[era]:
            html += f"""
    <div class="era-header">{era} ({len(relics[era])})</div>
    <table>
        <thead>
            <tr>
                <th>Nome</th>
                <th>Peças</th>
            </tr>
        </thead>
        <tbody>
"""
            for relic in relics[era]:
                parts = relic.split()
                relic_name = ' '.join(parts[:2])
                relic_parts = ', '.join(parts[2:]) if len(parts) > 2 else ''
                html += f"""
            <tr>
                <td>{relic_name}</td>
                <td>{relic_parts}</td>
            </tr>
"""
            html += """
        </tbody>
    </table>
"""

    html += """
</body>
</html>
"""
    return html

def main():
    try:
        ensure_output_dir()
        html_content = fetch_page_content()
        relics_data = extract_relics(html_content)
        html_output = generate_html(relics_data)
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"✅ Arquivo gerado com sucesso: {OUTPUT_FILE}")
        print("Resumo de relíquias encontradas:")
        for era, items in relics_data.items():
            print(f"- {era}: {len(items)} relíquias")
            
    except Exception as e:
        print(f"❌ Erro durante a execução: {str(e)}")
        raise

if __name__ == "__main__":
    main()
