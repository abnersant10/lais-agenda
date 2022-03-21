import xml.etree.ElementTree as ET
tree = ET.parse(
    'C:\\Users\\abner\\Desktop\\lais-agenda\\lais\\templates\\estabelecimentos_pr.xml')
xml = tree.getroot()
unidades = {}
i = 0
for filho in xml:
    unidades[filho[6].text] = filho[1].text
    i = i+1
print(xml)
print(unidades)
print(i)
