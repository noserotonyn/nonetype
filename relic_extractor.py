import requests
from bs4 import BeautifulSoup

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"

print("🔄 Baixando página oficial...")
response = requests.get(URL)
response.raise_for_status()
html = response.text

soup = BeautifulSoup(html, "html.parser")

print("🔍 Procurando a seção 'Mission Rewards' pelo texto...")

# Buscar pela tag que contenha texto 'Mission Rewards'
mission_rewards_header = None
for header in soup.find_all(['h2', 'h3', 'h4', 'h5']):
    if "Mission Rewards" in header.text:
        mission_rewards_header = header
        break

if not mission_rewards_header:
    raise Exception("❌ Seção 'Mission Rewards' não encontrada.")

# A seção desejada deve estar logo após esse header
section = mission_rewards_header.find_next_sibling()
if not section:
    raise Exception("❌ Conteúdo após 'Mission Rewards' não encontrado.")

print("🧹 Extraindo reliquias da seção...")

eras = {
    "Lith": set(),
    "Meso": set(),
    "Neo": set(),
    "Axi": set(),
}

# Vamos buscar dentro da section todos os textos que começam com Lith, Meso, Neo, Axi e ignorar radiant
for el in section.find_all(text=True):
    text = el.strip()
    for era in eras.keys():
        if text.startswith(era) and "Radiant" not in text:
            eras[era].add(text)
            break

print("🔧 Montando tabela HTML...")

html_table = """
<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; text-align: left;">
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

max_rows = max(len(eras["Lith"]), len(eras["Meso"]), len(eras["Neo"]), len(eras["Axi"]))

list_lith = sorted(eras["Lith"])
list_meso = sorted(eras["Meso"])
list_neo = sorted(eras["Neo"])
list_axi = sorted(eras["Axi"])

for i in range(max_rows):
    html_table += "<tr>"
    html_table += f"<td>{list_lith[i] if i < len(list_lith) else ''}</td>"
    html_table += f"<td>{list_meso[i] if i < len(list_meso) else ''}</td>"
    html_table += f"<td>{list_neo[i] if i < len(list_neo) else ''}</td>"
    html_table += f"<td>{list_axi[i] if i < len(list_axi) else ''}</td>"
    html_table += "</tr>"

html_table += """
  </tbody>
</table>
"""

with open("output/relics.html", "w", encoding="utf-8") as f:
    f.write(html_table)

print("✅ Arquivo 'output/relics.html' gerado com sucesso.")
