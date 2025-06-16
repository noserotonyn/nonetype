import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os

URL = "https://warframe-webassets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "relics.html")

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_relic_data():
    print(f"🔄 Baixando dados em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    return response.text

def parse_relics(html):
    soup = BeautifulSoup(html, "html.parser")
    script = None
    
    for s in soup.find_all("script"):
        if s.string and "window.__data" in s.string:
            script = s.string
            break

    if not script:
        raise Exception("❌ Dados das relíquias não encontrados na página")

    match = re.search(r"window\.__data\s*=\s*({.*?});\s*$", script, re.DOTALL)
    if not match:
        raise Exception("❌ Formato dos dados inválido")

    data = json.loads(match.group(1))
    missions = data.get("props", {}).get("pageProps", {}).get("missions", [])
    
    if not missions:
        raise Exception("❌ Nenhuma missão encontrada nos dados")

    return extract_relics_from_missions(missions)

def extract_relics_from_missions(missions):
    eras = {"Lith": set(), "Meso": set(), "Neo": set(), "Axi": set()}
    
    for mission in missions:
        for reward in mission.get("rewards", []):
            name = reward.get("name", "")
            if "Relic" in name and "Intact" in name:
                for era in eras:
                    if era in name:
                        eras[era].add(name.replace(' Intact', ''))
    
    return eras

def generate_html(relics):
    for era in relics:
        relics[era] = sorted(relics[era])

    max_rows = max(len(relics[era]) for era in relics)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Relíquias Warframe Atuais</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th { background-color: #f2f2f2; text-align: left; padding: 10px; }
            td { padding: 8px; border-bottom: 1px solid #ddd; }
            .timestamp { color: #666; font-size: 0.9em; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>Relíquias Warframe Atuais</h1>
        <table>
            <thead>
                <tr>
                    <th>Lith</th>
                    <th>Meso</th>
                    <th>Neo</th>
                    <th>Axi</th>
                </tr>
            </thead>
            <tbody>
    """

    for i in range(max_rows):
        html += "<tr>"
        for era in ["Lith", "Meso", "Neo", "Axi"]:
            relic = relics[era][i] if i < len(relics[era]) else ""
            html += f"<td>{relic}</td>"
        html += "</tr>"
    
    html += f"""
            </tbody>
        </table>
        <div class="timestamp">Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </body>
    </html>
    """
    
    return html

def main():
    try:
        ensure_output_dir()
        html = fetch_relic_data()
        relics = parse_relics(html)
        output = generate_html(relics)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(output)
        
        print(f"✅ Arquivo gerado: {OUTPUT_FILE}")
        print(f"Resumo: Lith({len(relics['Lith'])}), Meso({len(relics['Meso'])}), Neo({len(relics['Neo'])}), Axi({len(relics['Axi'])})")
    
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        raise

if __name__ == "__main__":
    main()
