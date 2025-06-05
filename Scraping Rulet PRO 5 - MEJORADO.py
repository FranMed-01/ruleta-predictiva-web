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
LIMITE_NUMEROS = 10150  # Cambia este valor si necesitas más
SHEET_ID = "1CyihTSL1PLmRC9DvVS-al17FIn9Wy5T9o-80IDLhjI0"  # 👈 Reemplaza con el ID real de tu hoja

# === CREDENCIALES INCRUSTADAS ===
json_credenciales = {
  "type": "service_account",
  "project_id": "scraping-sheets-461821",
  "private_key_id": "3912a9d477d8fff95aa9c0cfbd1d782554f51eeb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2ak1vrXg+/+Jj\nn0GRHJrnFcaKC3QRCoBJfq3o9KuLuOIDs8tRkfuR+06KUuLL5UdYougmfTQubDdD\nclZ24Kcjm43F3N6uWUvgHaySKZzFrji1cb83OSEhLwKLXBiuS3Iy3iWBvSOLKETE\nLl5KHd3Kkuq6bT1z/s3on5c9SdSjfCv73zjHlaXLBUYk8PGD48IMdiXxmYDEknfy\nsjgck/sAwzcOuJdz9BvkT2oii/N3wyGA60uR7v6aAcVX4nN46QxmwPqWE2DoLO0F\nIqAg7u/KQ/6wnIfUFlygh05Cpktahkb1SDDKl6a4wcVn6nVnTiIC1HGpH3d24LWb\nszuoulY3AgMBAAECggEASvnsdB+P0g0oxxu5PmTMgnjfzvOgNDTlv8+SubJ/JAHM\n3Aq1YgSnqzvo70/cKkRGC/eBhfhmT0JpgI5pXZk++ZLBNfdvi6fmWOq5eKYj6tiO\nNH3ZQ2B27oW8/PzQpCsceC34qpfMGTFm+l+4n6wg8ldqpU+rN5cemSOnbSiAfuUj\nIoCahxT2+NxUvVGAElbaEhGN6tFG8RABbBzUzhMt7YmHqlcwl/NYveBP/IgaxGii\nFsXqEm8vPTc4biRvjS6I+JwKiIQ8V8LynGtcH7QMOnGzoODuySmf5cGqAj5sFlNS\nmursh6aJzm5DI9vGT0FM/5YQWZ99Qr6A+I3I/+tb0QKBgQDwdTRrU0Ym0r2lhZuP\nC/MCFmFcjC/qrxlJhTBxassva68I9vf5FzSVC2WBQxP6oSADeIwPcb4hJ2PousfR\nBpFBxhTLp19FwC5ur/CpDhCFsyyf8aVxQ5IxFhore31z4kO1FyzRH25qIjJWUv/W\nRpecsbQfWvorgRSJqK4AwBMNTwKBgQDCNK5/yx8rW7uQ+5LhDJtbCH5L4ydKgfBo\n3VfziwnAsZ+bNJtdabihSMy8F9pcTH9qtr69E9pKMbsWwOyyYN/YK0E6Um/mUOBH\nH2BRnUwk79nygNgNaV3oZM41W8YMSyH97nBNutAd1aeHnna2oUqpTu4pbGqWx7xN\no6OCHO3+mQKBgG6LY3Ln0LtubPNYjiBgPPK7uTzj0e+RWg27pn6tuwVs+wYjC/M+\n4NSYbazUWq4BPwd5duJuxxrU0hCfNdd5rnPPjaXmp10Ysf/+8KO3rI7axWwumoGM\nr/vTDmrpFc6ducTaB6eITKmMWRnohGdNAsxtwcIcgCBZ8kgq/PupUdjvAoGAMzPu\nmhT019qsvlIF7L4FK+A2ZE20q0lNGGjbaoPLA3oRabtaByv7mNJ34FOtp84nffxG\nl9VnJU6tVBdzkKhH/FeTMAxSInhKWZYlL/939vkiDnT4Abk5IC+LyreypMUeZjP6\nehP6EROmwvP9urMV20PLOTKze6OXuySc1I5KFWkCgYEA7mJNfZViUzM8WAUfD3yD\nO45TlthLP93USV/y6AtxyNgl2r+YViFt2ntb/tpqQIo8DXXt5qTOEB8I8bDM8a0X\nmsDM/CJwBdeFFzxUTp9GsfpbGiTc8xKSSIBTo/D7Kh4KuFQSxzGwWC+OBhKq+f0X\nZsNDpaPeLv4SV9dP9CYwn3Q=\n-----END PRIVATE KEY-----\n",
  "client_email": "sheets-bot@scraping-sheets-461821.iam.gserviceaccount.com",
  "client_id": "115275273133076245999",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sheets-bot%40scraping-sheets-461821.iam.gserviceaccount.com",
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
numeros_guardados_en_ejecucion = 0  # Nuevo contador local
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
            numeros_guardados_en_ejecucion += len(valores)  # 👈 Contar los iniciales

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
            if numeros_guardados_en_ejecucion >= LIMITE_NUMEROS:
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
                        numeros_guardados_en_ejecucion += 1  # Sumar al contador solo si fue guardado
                        print(f"🧮 Números guardados en esta ejecución: {numeros_guardados_en_ejecucion}/{LIMITE_NUMEROS}")
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
