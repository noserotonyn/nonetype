import requests
from bs4 import BeautifulSoup

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"

print("🔄 Baixando página oficial...")
response = requests.get(URL)
response.raise_for_status()
html = response.text

soup = BeautifulSoup(html, "html.parser")

print("🔍 Procurando a tabela de missões...")

# Buscar a tabela que tem a class 'missionRewardsTable'
table = soup.find("table", class_="missionRewardsTable")
if not table:
    raise Exception("❌ Tabela de missões (class 'missionRewardsTable') não encontrada.")

print("🧹 Extraindo reliquias da tabela...")

eras = {
    "Lith": set(),
    "Meso": set(),
    "Neo": set(),
    "Axi": set(),
}

for tr in table.find_all("tr")[1:]:  # Pular cabeçalho
    cols = tr.find_all("td")
    if len(cols) < 2:
        continue
    reward = cols[1].get_text(strip=True)
    # Filtra por reliquias, ignorando radiant
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
