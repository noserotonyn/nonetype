import requests
from bs4 import BeautifulSoup
import os

print("🔄 Baixando página oficial...")

URL = "https://warframe-webassets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

print("🔍 Procurando por recompensas de missões com relíquias...")

# Encontrar todas as tabelas com recompensas
tables = soup.find_all("table")
relics = {"Lith": set(), "Meso": set(), "Neo": set(), "Axi": set()}

for table in tables:
    rows = table.find_all("tr")[1:]  # Ignora o cabeçalho
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        reward = cols[1].get_text(strip=True)
        for era in relics:
            if reward.startswith(era):
                relics[era].add(reward.split(" (")[0])  # remove "(Radiant)", etc.

# Garante que a pasta output existe
os.makedirs("output", exist_ok=True)

print("✅ Gerando tabela HTML...")

# Gera HTML organizado
html = "<html><head><meta charset='utf-8'><style>table{width:100%;border-collapse:collapse}td,th{border:1px solid #ccc;padding:8px;text-align:left}th{background:#eee}</style></head><body>"
html += "<h1>Relíquias Disponíveis em Missões</h1>"
html += "<table><tr><th>Lith</th><th>Meso</th><th>Neo</th><th>Axi</th></tr>"

# Preenche linha por linha
max_rows = max(len(relics["Lith"]), len(relics["Meso"]), len(relics["Neo"]), len(relics["Axi"]))
for i in range(max_rows):
    html += "<tr>"
    for era in ["Lith", "Meso", "Neo", "Axi"]:
        items = sorted(relics[era])
        html += f"<td>{items[i] if i < len(items) else ''}</td>"
    html += "</tr>"

html += "</table></body></html>"

with open("output/relics.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Arquivo 'output/relics.html' gerado com sucesso!")
