import requests
from bs4 import BeautifulSoup
import os

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Criar estrutura para armazenar as relíquias
relics = {"Lith": set(), "Meso": set(), "Neo": set(), "Axi": set()}

# Encontrar a seção "Mission Rewards"
mission_rewards_section = None
for h2 in soup.find_all("h2"):
    if "Mission Rewards" in h2.text:
        mission_rewards_section = h2.find_next_sibling()
        break

if mission_rewards_section:
    # Dentro da seção, procurar por todas as listas de itens
    for ul in mission_rewards_section.find_all("ul"):
        for li in ul.find_all("li"):
            text = li.get_text(strip=True)
            for tier in relics:
                if text.startswith(tier + " "):
                    relics[tier].add(text)

# Criar diretório de saída
os.makedirs("output", exist_ok=True)

# Gerar HTML com as relíquias
with open("output/relics.html", "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Relíquias Warframe</title>\n</head>\n<body>\n")
    f.write("<h1>Relíquias Atuais do Warframe (Missões)</h1>\n")
    for tier in ["Lith", "Meso", "Neo", "Axi"]:
        f.write(f"<h2>{tier}</h2>\n<ul>\n")
        for relic in sorted(relics[tier]):
            f.write(f"<li>{relic}</li>\n")
        f.write("</ul>\n")
    f.write("</body>\n</html>")
