# saca la tabla de parcelas del docx del profe y la guarda como csv
from docx import Document
import csv

doc = Document("entrada/Proyecto_PSO_Riego_Agricultura_Documento_Final.docx")
tabla = doc.tables[0]
with open("entrada/parcelas_guasave.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    for fila in tabla.rows:
        w.writerow([c.text.strip() for c in fila.cells])
print("filas:", len(tabla.rows) - 1)
