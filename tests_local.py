import xml.etree.ElementTree as ET
# codigo auxiliar extrair dados do XML
tree = ET.parse('grupos_atendimento.xml')
xml = tree.getroot()
for filho in xml:
    print(filho[0].text)
    # print("-------")
    pass
