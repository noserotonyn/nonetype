import requests
from bs4 import BeautifulSoup
import os

# URL da página oficial de recompensas do Warframe
URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html#missionRewards"

# Faz o download da página
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# Função para verificar se um texto é uma relíquia
def is_relic(text):
    return any(text.startswith(prefix) for prefix in ["Lith ", "Meso ", "Neo ", "Axi "])

# Encontrar a seção de recompensas de missões
mission_rewards_section = soup.find("h3", string="Mission Rewards")

if not mission_rewards_section:
    print("⚠️ Seção 'Mission Rewards' não encontrada.")
    exit()

# Encontrar a próxima <table> após o título
table = mission_rewards_section.find_next("table")
if not table:
    print("⚠️ Tabela não encontrada após 'Mission Rewards'.")
    exit()

# Extrair todas as relíquias únicas da tabela
relics = set()
for td in table.find_all("td"):
    text = td.get_text(strip=True)
    if is_relic(text):
        relics.add(text)

# Organizar por tipo
organized = {"Lith": [], "Meso": [], "Neo": [], "Axi": []}
for relic in sorted(relics):
    for prefix in organized:
        if relic.startswith(prefix):
            organized[prefix].append(relic)

# Gera HTML simples
html_content = "<html><head><meta charset='utf-8'><title>Relíquias Atuais</title></head><body>"
html_content += "<h2>Relíquias Atuais Disponíveis em Missões</h2>"

for category in ["Lith", "Meso", "Neo", "Axi"]:
    html_content += f"<h3>{category}</h3><ul>"
    for relic in organized[category]:
        html_content += f"<li>{relic}</li>"
    html_content += "</ul>"

html_content += "</body></html>"

# Cria pasta de saída se não existir
os.makedirs("output", exist_ok=True)

# Salva o HTML
with open("output/relics.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ HTML gerado com sucesso em output/relics.html")
