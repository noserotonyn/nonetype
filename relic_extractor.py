import requests
from bs4 import BeautifulSoup
import re
import os

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "relics.html")

print("🔄 Baixando página oficial...")
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

print("🔍 Procurando a tabela de missões...")
table = soup.find("table")
if not table:
    raise Exception("❌ Tabela de missões não encontrada.")

# Regex para relíquias válidas (ex: Axi G7 Relic)
relic_pattern = re.compile(r"^(Lith|Meso|Neo|Axi) [A-Z]\d+ Relic$")

# Separar relíquias por era
columns = {"Lith": [], "Meso": [], "Neo": [], "Axi": []}

for row in table.find_all("tr")[1:]:
    cells = row.find_all("td")
    for cell in cells:
        text = cell.get_text(strip=True)
        if relic_pattern.match(text):
            era = text.split()[0]
            if text not in columns[era]:
                columns[era].append(text)

print("✅ Relíquias extraídas com sucesso!")

# Criar diretório se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Criar tabela HTML
html_output = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Relíquias Atuais</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        table { width: 100%%; border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }
        th { background-color: #f0f0f0; }
    </style>
</head>
<body>
    <h1>Relíquias Atuais por Era</h1>
    <table>
        <tr>
            <th>Lith</th>
            <th>Meso</th>
            <th>Neo</th>
            <th>Axi</th>
        </tr>
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
    </table>
</body>
</html>
""".format(
    "<br>".join(columns["Lith"]),
    "<br>".join(columns["Meso"]),
    "<br>".join(columns["Neo"]),
    "<br>".join(columns["Axi"]),
)

# Salvar arquivo
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"💾 Arquivo salvo em: {OUTPUT_FILE}")
