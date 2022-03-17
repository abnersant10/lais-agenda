import xml.etree.ElementTree as ET
# codigo auxiliar extrair dados do XML
tree = ET.parse('grupos_atendimento.xml')
xml = tree.getroot()
grp_atend = {}
i = 1
for filho in xml:
    grp_atend[i] = filho[0].text
    i = i + 1
    #print(filho[0].tag, filho[0].text)
    # print("-------")
    pass


for ide in grp_atend:
    print(ide, grp_atend[ide])
