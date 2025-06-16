import requests
from bs4 import BeautifulSoup
import os

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html#missionRewards"

print("🔄 Baixando página oficial...")
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Verifica se conseguiu acessar a página
if response.status_code != 200:
    print(f"❌ Erro ao acessar a página. Código {response.status_code}")
    exit(1)

# Define o que é uma relíquia
def is_relic(text):
    return any(text.startswith(prefix) for prefix in ["Lith ", "Meso ", "Neo ", "Axi "])

# Tenta encontrar a seção "Mission Rewards"
print("🔍 Procurando seção 'Mission Rewards'...")
mission_rewards_section = None
for h in soup.find_all(["h2", "h3"]):
    if "Mission Rewards" in h.get_text(strip=True):
        mission_rewards_section = h
        break

if not mission_rewards_section:
    print("❌ Seção 'Mission Rewards' não encontrada.")
    exit(1)

# Tenta encontrar a tabela logo após o título
print("🔍 Procurando tabela de recompensas...")
table = mission_rewards_section.find_next("table")
if not table:
    print("❌ Tabela não encontrada.")
    exit(1)

# Extrair relíquias da tabela
print("📦 Extraindo relíquias...")
relics = set()
for td in table.find_all("td"):
    text = td.get_text(strip=True)
    if is_relic(text):
        relics.add(text)

if not relics:
    print("⚠️ Nenhuma relíquia encontrada.")
    exit(1)

# Organiza por tipo
organized = {"Lith": [], "Meso": [], "Neo": [], "Axi": []}
for relic in sorted(relics):
    for prefix in organized:
        if relic.startswith(prefix):
            organized[prefix].append(relic)

# Gera HTML simples
print("📝 Gerando HTML...")
html_content = "<html><head><meta charset='utf-8'><title>Relíquias Atuais</title></head><body>"
html_content += "<h2>Relíquias Atuais Disponíveis em Missões</h2>"

for category in ["Lith", "Meso", "Neo", "Axi"]:
    html_content += f"<h3>{category}</h3><ul>"
    for relic in organized[category]:
        html_content += f"<li>{relic}</li>"
    html_content += "</ul>"

html_content += "</body></html>"

os.makedirs("output", exist_ok=True)

output_path = "output/relics.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ HTML gerado com sucesso: {output_path}")
