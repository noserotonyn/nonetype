import requests
from bs4 import BeautifulSoup

URL = "https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/uploads/cms/hnfvc0o3jnfvc873njb03enrf56.html#missionRewards"

print("🔄 Baixando página oficial...")
response = requests.get(URL)
response.raise_for_status()
html = response.text

soup = BeautifulSoup(html, "html.parser")

print("🔍 Procurando seção 'Mission Rewards'...")
section = soup.find(id="missionRewards")
if not section:
    raise Exception("❌ Seção 'Mission Rewards' não encontrada.")

# A seção tem várias linhas de recompensas (exemplo para ilustrar)
# Vamos pegar todos os textos que mencionem Lith, Meso, Neo ou Axi e eliminar os radiant

print("🧹 Extraindo reliquias...")

eras = {
    "Lith": set(),
    "Meso": set(),
    "Neo": set(),
    "Axi": set(),
}

# Aqui vou assumir que as relíquias aparecem como texto dentro da seção,
# e que os nomes tem as eras no início: "Lith G17", "Meso Ceti", etc.
# Também ignoraremos as que terminam com "Radiant"

texts = section.stripped_strings
for text in texts:
    # Checa se é reliquia de alguma era
    for era in eras.keys():
        if text.startswith(era):
            # Ignora radiant
            if "Radiant" not in text:
                # Remove possíveis detalhes extras depois do nome (se quiser)
                eras[era].add(text.strip())
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

# Vamos calcular o número máximo de linhas entre as colunas para montar a tabela alinhada
max_rows = max(len(eras["Lith"]), len(eras["Meso"]), len(eras["Neo"]), len(eras["Axi"]))

# Convertendo sets para listas e ordenando
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

# Salvar em arquivo
with open("output/relics.html", "w", encoding="utf-8") as f:
    f.write(html_table)

print("✅ Arquivo 'output/relics.html' gerado com sucesso.")
