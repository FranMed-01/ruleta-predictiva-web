import time
import hashlib
import os
import gspread
import undetected_chromedriver as uc
import time, hashlib
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# === CONFIGURACIÓN ===
INTERVALO_SEGUNDOS = 6
LIMITE_NUMEROS = 800  # Cambia este valor si necesitas más
SHEET_ID = "1CyihTSL1PLmRC9DvVS-al17FIn9Wy5T9o-80IDLhjI0"  # 👈 Reemplaza con el ID real de tu hoja

# === CREDENCIALES INCRUSTADAS ===
json_credenciales = {
  "type": "service_account",
  "project_id": "scraping-ruleta",
  "private_key_id": "afff5ead20556da5196db3e07b68c5f87ee489fe",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDhbV3tqO84kvT9\\nPUpx9z8lXkQ6oXZxSX3zr455Vv/2Qdv+2gC31ZYp0oUqmCI2hOaQMrKGPPE5XeSw\\nACEluPEj38kHad29mIho6oE/SEEbYRlamri3Qg3ko0Dhrb2t6hHdQNVo2RCGL6ZO\\n4opnN/EBF5iwWaa4YbIyNqxq2bMV5oel4jT1fewE28bHgN/TqzVTKS9OM3X78W6D\\nIlQTnyb2wEVAIH8c6vlVbqr7HtSSgSGQlJIBG0pOVoEW3h+H3T/PYdhhm+ySNSZ1\\n0GawmQR1/xbnM2GDHAgLS6tnkW7FUwj4SbqXpmSiCJYv8QfFep0CLZrWiqZsKpdc\\nrYIJn3X9AgMBAAECggEAA4NY0Liulwsd658Q50XFzidHQ5f7PeNkpcTj9jAiPQw5\\ntCG28SZ6+Jvh8g/84yyfCzrpsqiFzzG6EU7Eis9JssLCDJjcbnVPauh8qyfNG/LK\\nGly0PubgoIzgGKREgyQACJqsuL2T7FjBwWj2ZIq9TsRiCh2GOPQM0DYvPwW1ghnW\\nIPJUDs9iUTbIBJ0ZeX/ysMKN3SvJfkD8zDa8ln/RqNyrOq/Ux8mkUkOtdgp0PoiL\\nOQCdWEFWLV/B809owroC86Z15EZkjuUr+PthNBTakMgVeXQofkTMbemT3wpFi1vE\\nOGPksqtxDIMlPbemYDCZz+505ZgsfXOnf9sz28S+YQKBgQD0GkET+oLo5f5hX+Od\\njM29im2rhrFn/h2U0NUmzVmJvyt9W9/XpcVznlJVWn8y6BKTEb3Y46ty76TPnGtP\\nXMWUDYOy2znJYI0HPZkwX17LGXQBeSleyHKznW2gtUU8iRysaW+HvSJzLtCbRb01\\nu1RoBJHbq6x+afDWe1Erq5/xOwKBgQDsahgwEYMVr6JEeGDpus+3xhTCApUa2Ryc\\nPHG9Aah/ovIAMwai4dGcIWNBJP1N3gkv3MpwCmIymLHc0wGAF66k/auhKbzVAG3r\\ni+3O2WatlrL09fwnjThccF9EBlBk9bN1lYIHxGxJBeKnJc0yVJlW8i2WDC/ZEDnZ\\nZl1pVynCJwKBgQDpHWWG6dc5CePsJEHgRQZ6e4eOpjwoHwMrCmB1BOj8Zmfm+OWF\\nMRem+cyRHLKa8AxFDU1roskqI3gWmL/Wc7dwU5OxLDE8gotMHeR80KdbeHxTp9z9\\nWppHtBFsx5BOZnbOpIZRcCtFKrEnh+tRNAxAphSRX5qEwzGv8uaquOUu3wKBgHDy\\nJuggFa4woKdxk2tW0pIL0jL2JOIUw7RotDYGKsf/wvoRZqQ+mnOrB85Bq7qdz2nM\\nY/KvI0bk6GSFcnwN1GQCxRJT7GEeuWUFDvH5rzJTgt/A/Vyv/TM8hGbtVU9Gixwr\\n91laoBkq9KPCTYw0GqYNQXYkEF/1fo28d/gxqkOVAoGBANPySfeBos4Pm0s2j0WY\\nb9t/MlsIsX876/7na5OH9bGXlyBmzOpiMf6yFCxF+rk+fleW96Ylx5ADEfDNsYPB\\nPe1DXf00vhjj0je+KwC5HGn0tSuPRGHSOzadsizhMtCgjm7TYCLQB/T8sNvX8aH1\\nQV1Gz/sVnotcOFl8vWfuS0Hl\\n-----END PRIVATE KEY-----\\n",
  "client_email": "cuenta-ruleta@scraping-ruleta.iam.gserviceaccount.com",
  "client_id": "115496302833819515642",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cuenta-ruleta%40scraping-ruleta.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

json_credenciales["private_key"] = json_credenciales["private_key"].replace("\\n", "\n")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(json_credenciales, scope)
cliente = gspread.authorize(credenciales)
sheet = cliente.open_by_key(SHEET_ID).sheet1

# === SELENIUM CONFIG ===
URL = "https://gamblingcounting.com/immersive-roulette"

def iniciar_driver():
    options = Options()
    
    # ✅ No usar headless: evita ser detectado como bot
    # options.add_argument("--headless")  # Comentado para pruebas visibles

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=es-CL")
    options.add_argument("--window-size=1920,1080")

    # ✅ User-Agent real de navegador Chrome
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

    # ✅ Opciones para ocultar que es Selenium
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Crear el driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # ✅ Eliminar propiedad "navigator.webdriver"
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    # Abrir la URL de la ruleta
    URL = "https://gamblingcounting.com/immersive-roulette"
    driver.get(URL)

    return driver

def extraer_textos_validos(elems):
    return [e.text.strip() for e in elems if e.text.strip()]

def generar_firma(lista):
    return hashlib.sha256("|".join(lista).encode("utf-8")).hexdigest()

def obtener_numeros_ruleta(driver):
    try:
        container_css = 'section[aria-labelledby="live-game-result-label"] .live-game-page__block__results--roulette.live-game-page__block__content'
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, container_css)))
        container = driver.find_element(By.CSS_SELECTOR, container_css)
        small_selector = "div.roulette-number--small"
        WebDriverWait(container, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, small_selector)))

        for intento in range(3):
            try:
                elementos = container.find_elements(By.CSS_SELECTOR, small_selector)
                numeros = extraer_textos_validos(elementos)
                if numeros:
                    firma = generar_firma(numeros[:5])
                    return numeros, firma
            except StaleElementReferenceException:
                time.sleep(1)

        raise Exception("No se pudo extraer elementos válidos tras varios intentos.")

    except Exception as e:
        if "invalid session id" in str(e).lower() or "disconnected" in str(e).lower():
            print("⚠️ Navegador desconectado. Reiniciando sesión...")
            try:
                driver.quit()
            except:
                pass
            nuevo_driver = iniciar_driver()
            return obtener_numeros_ruleta(nuevo_driver)
        else:
            print(f"❌ Error al extraer datos: {e}")
            return [], None


def contar_numeros_actuales():
    return len(sheet.col_values(1)) - 1  # Restamos encabezado

def guardar_en_sheets(numero):
    try:
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.insert_row([str(numero), fecha_hora], 2)  # Inserta número y fecha/hora
        print(f"✅ Guardado en Google Sheets: {numero} - {fecha_hora}")
        return True
    except Exception as e:
        print(f"❌ Error al guardar en Sheets: {e}")
        return False

def esta_pegado(historial, nuevo):
    if len(historial) < 10:
        return False
    return all(str(n) == str(nuevo) for n in historial[-10:])

# === INICIO ===
historial_numeros = []
ciclos_iguales = 0  # 👈 Esto debe ir fuera del if también

if __name__ == "__main__":
    print("🚀 Iniciando monitoreo de ruleta...")
    driver = iniciar_driver()

    opcion = input("¿Deseas cargar los primeros 200 números iniciales? (s/n): ").lower()
    if opcion == "s":
        iniciales, _ = obtener_numeros_ruleta(driver)
        if iniciales:
            iniciales = iniciales[:200]
            print(f"📥 Cargando {len(iniciales)} números iniciales...")

            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            valores = [[str(n), ahora] for n in iniciales]
            sheet.insert_rows(valores, 2)
            print(f"✅ Guardados {len(valores)} números en bloque.")

            firma_anterior = generar_firma([str(n) for n in iniciales[:5]])
        else:
            print("⚠️ No se pudieron obtener números iniciales.")
            firma_anterior = None
    else:
        actuales = obtener_numeros_ruleta(driver)
        numeros_actuales, _ = actuales if actuales else ([], None)
        firma_anterior = generar_firma(numeros_actuales[:5]) if numeros_actuales else None

    try:
        while True:
            if contar_numeros_actuales() >= LIMITE_NUMEROS:
                print("🎯 Límite alcanzado. Cerrando script.")
                driver.quit()
                exit(0)

            numeros, nueva_firma = obtener_numeros_ruleta(driver)

            if numeros and nueva_firma:
                if nueva_firma != firma_anterior:
                    ciclos_iguales = 0  # Reiniciamos contador
                    numero_nuevo = numeros[0]
                    firma_anterior = nueva_firma
                    if guardar_en_sheets(str(numero_nuevo)):
                        historial_numeros.append(str(numero_nuevo))
                        if len(historial_numeros) >= 10 and all(n == str(numero_nuevo) for n in historial_numeros[-10:]):
                            print("⚠️ Mismo número repetido 10 veces. Reiniciando navegador por seguridad...")
                            try:
                                driver.quit()
                            except:
                                pass
                            driver = iniciar_driver()
                            historial_numeros = []
                            time.sleep(5)
                        else:
                            time.sleep(3)
                else:
                    ciclos_iguales += 1
                    print("⏳ Mismo número anterior, esperando nuevo...")

                    if ciclos_iguales >= 10:
                        print("⚠️ No hay cambio en los números tras 10 ciclos. Reiniciando navegador por posible congelamiento de Selenium...")
                        try:
                            driver.quit()
                        except:
                            pass
                        driver = iniciar_driver()
                        ciclos_iguales = 0
                        historial_numeros = []
                        time.sleep(5)
            else:
                print("❌ No se pudo extraer número nuevo.")

            time.sleep(INTERVALO_SEGUNDOS)

    except KeyboardInterrupt:
        print("🛑 Script detenido por el usuario.")
        driver.quit()