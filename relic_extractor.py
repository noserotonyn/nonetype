import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"

print("🔄 Baixando página oficial...")
response = requests.get(URL)
response.raise_for_status()
html = response.text

soup = BeautifulSoup(html, "html.parser")

print("🔍 Procurando JSON com dados...")

# Procurar no <script> que contenha window.__data = {...}
script = None
for s in soup.find_all("script"):
    if s.string and "window.__data" in s.string:
        script = s.string
        break

if not script:
    raise Exception("❌ Script com 'window.__data' não encontrado.")

# Extrair JSON da variável window.__data
match = re.search(r"window\.__data\s*=\s*({.*?});\s*$", script, re.DOTALL | re.MULTILINE)
if not match:
    raise Exception("❌ JSON da variável window.__data não encontrado.")

json_text = match.group(1)

print("📦 Carregando JSON...")
data = json.loads(json_text)

# Agora, navegue dentro do objeto para encontrar as missões e suas recompensas
# Pela inspeção, essa estrutura pode variar. Por exemplo:

try:
    missions = data["props"]["pageProps"]["missions"]
except KeyError:
    raise Exception("❌ Estrutura JSON mudou, não encontrou 'missions'.")

print(f"✅ Encontradas {len(missions)} missões.")

# Extração das reliquias (Lith, Meso, Neo, Axi) das recompensas de missão:

eras = {
    "Lith": set(),
    "Meso": set(),
    "Neo": set(),
    "Axi": set(),
}

for mission in missions:
    rewards = mission.get("rewards", [])
    for reward in rewards:
        name = reward.get("name", "")
        for era in eras.keys():
            if name.startswith(era) and "Radiant" not in name:
                eras[era].add(name)

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
