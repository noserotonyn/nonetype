import requests
from bs4 import BeautifulSoup
import os

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"

print("🔄 Baixando página oficial...")
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

if response.status_code != 200:
    print(f"❌ Erro ao acessar a página. Código {response.status_code}")
    exit(1)

# Define o que é uma relíquia
def is_relic(text):
    return any(text.startswith(prefix) for prefix in ["Lith ", "Meso ", "Neo ", "Axi "])

# Encontrar a primeira tabela (a de Missões)
print("🔍 Procurando primeira tabela com relíquias...")
tables = soup.find_all("table")
if not tables:
    print("❌ Nenhuma tabela encontrada.")
    exit(1)

# Extrair da primeira tabela
table = tables[0]

relics = set()
for td in table.find_all("td"):
    text = td.get_text(strip=True)
    if is_relic(text):
        relics.add(text)

if not relics:
    print("⚠️ Nenhuma relíquia encontrada na primeira tabela.")
    exit(1)

# Organizar relíquias
organized = {"Lith": [], "Meso": [], "Neo": [], "Axi": []}
for relic in sorted(relics):
    for prefix in organized:
        if relic.startswith(prefix):
            organized[prefix].append(relic)

# Gerar HTML
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

with open("output/relics.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ HTML gerado com sucesso: output/relics.html")
