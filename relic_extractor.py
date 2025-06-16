import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import time

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"

# Tentativas para contornar falhas de rede
for attempt in range(3):
    try:
        print("🔄 Baixando página oficial...")
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        break
    except Exception as e:
        print(f"⚠️ Tentativa {attempt + 1} falhou: {e}")
        if attempt == 2:
            raise Exception("❌ Falha ao baixar a página após 3 tentativas")
        time.sleep(5)

html = response.text
soup = BeautifulSoup(html, 'html.parser')

print("🔍 Procurando tabela de missões...")
mission_tables = soup.find_all("table")
if not mission_tables:
    raise Exception("❌ Nenhuma tabela encontrada na página.")

relics_by_era = defaultdict(set)
eras = ["Lith", "Meso", "Neo", "Axi"]

for table in mission_tables:
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        for cell in cells:
            text = cell.get_text(strip=True)
            for era in eras:
                if text.startswith(era):
                    relics_by_era[era].add(text.split(" (" )[0])

# HTML formatado em tabela
print("📝 Gerando HTML...")
html_output = """
<html>
<head>
    <meta charset="UTF-8">
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Relíquias Disponíveis em Missões</h1>
    <table>
        <tr>
"""

# Cabeçalhos
for era in eras:
    html_output += f"            <th>{era}</th>\n"
html_output += "        </tr>\n        <tr>\n"

# Pegar o maior número de relíquias entre as eras para criar as linhas corretamente
max_len = max(len(relics_by_era[era]) for era in eras)

# Organizar como lista
era_lists = {era: sorted(relics_by_era[era]) for era in eras}

for i in range(max_len):
    html_output += "        <tr>\n"
    for era in eras:
        relic = era_lists[era][i] if i < len(era_lists[era]) else ""
        html_output += f"            <td>{relic}</td>\n"
    html_output += "        </tr>\n"

html_output += """
    </table>
</body>
</html>
"""

# Salvar arquivo
output_path = "output/relics.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"✅ Arquivo gerado com sucesso em {output_path}")
