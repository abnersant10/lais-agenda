import xml.etree.ElementTree as ET
tree = ET.parse(
    'C:\\Users\\abner\\Desktop\\lais-agenda\\lais\\templates\\estabelecimentos_pr.xml')
xml = tree.getroot()
unidades = {}
i = 1
for filho in xml:
    unidades[str(i)] = filho[0].text
    i = i + 1

print(xml)
print(unidades)
