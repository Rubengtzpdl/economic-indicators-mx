import requests
import pandas as pd
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("Extrayendo indicadores económicos de México")

INDICADORES = {
    "inflacion": "FP.CPI.TOTL.ZG",
    "pib_crecimiento": "NY.GDP.MKTP.KD.ZG",
    "desempleo": "SL.UEM.TOTL.ZS",
    "tipo_cambio": "PA.NUS.FCRF",
    "deuda_pib": "GC.DOD.TOTL.GD.ZS"
}

BASE_URL = "https://api.worldbank.org/v2/country/MX/indicator/{}?format=json&mrv=5"

resultados = []

for nombre, codigo in INDICADORES.items():
    try:
        response = requests.get(BASE_URL.format(codigo), verify=False, timeout=10)
        data = response.json()
        registros = data[1]
        for r in registros:
            if r["value"] is not None:
                resultados.append({
                    "indicador": nombre,
                    "valor": round(r["value"], 2),
                    "anio": r["date"]
                })
        print(f" {nombre}: OK")
    except Exception as e:
        print(f" {nombre}: Error - {e}")

df = pd.DataFrame(resultados)
df["fecha_extraccion"] = datetime.now().strftime("%Y-%m-%d %H:%M")
df.to_excel("data/raw/indicadores_mx.xlsx", index=False)
print("\n Datos guardados en data/raw/indicadores_mx.xlsx")
print(df.head(10))
