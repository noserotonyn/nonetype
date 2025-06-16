import requests
from bs4 import BeautifulSoup

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"

print("🔄 Baixando página oficial...")
response = requests.get(URL)
response.raise_for_status()
html = response.text

soup = BeautifulSoup(html, "html.parser")

print("🔍 Procurando seção 'missionRewards' pelo id...")

# Encontrar o header <h2 id="missionRewards">
header = soup.find("h2", id="missionRewards")
if not header:
    raise Exception("❌ Seção com id 'missionRewards' não encontrada.")

# A tabela está logo após o header, pode estar em next siblings
table = None
next_el = header.find_next_sibling()
while next_el and not table:
    if next_el.name == "table":
        table = next_el
    else:
        next_el = next_el.find_next_sibling()

if not table:
    raise Exception("❌ Tabela com as recompensas não encontrada após 'missionRewards'.")

print("🧹 Extraindo reliquias da tabela...")

# Agora vamos extrair as reliquias dessa tabela, ignorando as radiant, e separando por era
eras = {
    "Lith": set(),
    "Meso": set(),
    "Neo": set(),
    "Axi": set(),
}

# A tabela tem linhas <tr>, vamos iterar elas
for tr in table.find_all("tr")[1:]:  # pular header
    cols = tr.find_all("td")
    if len(cols) < 2:
        continue
    reward = cols[1].get_text(strip=True)  # segunda coluna é a recompensa
    # Verifica se é uma reliquia (começa com Lith, Meso, Neo, Axi) e não tem radiant
    for era in eras.keys():
        if reward.startswith(era) and "Radiant" not in reward:
            eras[era].add(reward)

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
