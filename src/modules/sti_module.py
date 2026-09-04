from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
from time import sleep
import logging
import pandas as pd
import json
import os

from src.utils.path import resource_path
from gui.base import StatusGUI
from gui.log_handler import GuiLogHandler
from src.logs.logger import setup_logger

logger = logging.getLogger("tnb")

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def setup():

    chrome_options = Options()
    chrome_options.add_argument("headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.page_load_strategy = "eager"

    service = Service(log_path=os.devnull)

    return webdriver.Chrome(service=service, options=chrome_options)


def teardown(driver):
    driver.quit()


def collector():

    STI_URLS = [
        "https://svc1.stirastreamento.com.br/portal/Login", # site indisponível
        "https://svc2.stirastreamento.com.br/portal/Login",
        "https://serverca1.serveirc.com/Portal/Login",
    ]

    load_dotenv(resource_path(".env"))

    user = os.getenv("USER")
    passwd = os.getenv("PASSWD")

    if not user or not passwd:
        logger.warning("[STI] Variáveis de ambiente USER/PASSWD não encontradas. Verifique o arquivo .env ou as variáveis do sistema.")
        return None

    for url in STI_URLS:
        driver = setup()
        try:
            wait = WebDriverWait(driver, 60)
            
            driver.get(url)
            
            wait.until(EC.presence_of_element_located((By.ID, "usuario")))
            driver.find_element(By.XPATH, '//*[@id="usuario"]').send_keys(user), sleep(0.2)
            driver.find_element(By.XPATH, '//*[@id="senha"]').send_keys(passwd, Keys.RETURN)

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shortcut")))
            driver.find_element(
                By.XPATH, "/html/body/div[6]/div[1]/div/div/div[1]/div/div[2]/div/a[1]"
            ).click()

            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[2]/div[2]/div/table/tbody/tr[5]")))

            Select(driver.find_element(By.ID, "pageLength")).select_by_visible_text("100")

            sleep(.5)

            complete_table = []
            rows = driver.find_elements(
                By.XPATH, "/html/body/div[4]/div/div/div[2]/div[2]/div/table/tbody/tr"
            )
            for row in rows:
                columns = [col.text.strip() for col in row.find_elements(By.XPATH, ".//td")]

                if len(columns) > 10:
                    try:
                        lg_element = row.find_element(By.XPATH, ".//td[11]/img")
                        alt_value = lg_element.get_attribute("alt")

                        columns[10] = (
                            "\U0001f7e2" if alt_value == "Ligada" else "\U0001f518"
                        )
                    except Exception:
                        columns[10] = "\U0001f518"

                complete_table.append(columns)

            logger.info(f"[STI] Coletando dados em: {url}")
            teardown(driver)
            return complete_table

        except (WebDriverException, TimeoutException) as e:
            logger.warning(f"[STI] Falha ao acessar {url}: {e}. Tentando próxima URL...")
        except Exception as e:
            logger.exception(f"[STI] Erro ao processar dados de {url}: {e}")
        finally:
            try:
                teardown(driver)
            except Exception:
                pass

    logger.warning(f"[STI] Nenhuma URL conseguiu coletar dados válidos")
    return None


def transform_data(data):

    data = data[1:] if len(data) > 1 else data

    if len(data) > 0 and len(data[0]) >= 9:
        df = pd.DataFrame(
            data,
            columns=[
                "-",
                "Conta",
                "Divisão",
                "Veiculo",
                "Operador",
                "Matricula?",
                "Data",
                "Evento",
                "Velocidade",
                "Local",
                "Status",
                "Rota",
                "Hodometro",
                "Horimetro",
                "RPM",
                "Temperatura",
                "Bateria Externa",
                "Bateria Interna",
            ],
        )

        # print(df.to_string())

        df = df[["Veiculo", "Data", "Velocidade", "Status", "Local"]]
        df = df[df["Veiculo"] != "MXT-15175"]

        df["Veiculo"] = df["Veiculo"].str[:3] + " " + df["Veiculo"].str[3:]
        df["Veiculo"] = df["Veiculo"].str.rstrip("-")

        df["Velocidade"] = df["Velocidade"].str.replace(" km/h", "").astype(str)

        df["UF"] = df["Local"].apply(
            lambda loc: (
                "RJ"
                if "RJ" in loc.upper() or "RIO DE JANEIRO" in loc.upper()
                else (
                    "SP"
                    if "SP" in loc.upper()
                    or "PAULO" in loc.upper()
                    or "SA, BRASIL" in loc.upper()
                    else (
                        "MG"
                        if "MG" in loc.upper() or "MINAS GERAIS" in loc.upper()
                        else "-"
                    )
                )
            )
        )

        df["Local"] = df["Local"].str.title()

        df = converter(df, load_json(resource_path("src/docs/conversion_dict.json")))

        df = df.drop_duplicates(subset="Veiculo")

        return df

    else:
        raise Exception(
            f"Erro: Dados inconsistentes, esperado 18 colunas, mas encontrado {len(data[0])} colunas"
        )


def converter(df, conversion_dict):

    def convert_location(loc):
        loc_normalized = " ".join(loc.split()).lower()
        for key, value in conversion_dict.items():
            key_normalized = " ".join(key.split()).lower()
            if key_normalized in loc_normalized:
                return value
        return loc

    df["Local"] = df["Local"].apply(convert_location)

    return df


def sti_module():
    df = collector()
    
    if df is None:
        return None
    
    df = transform_data(df)
    return df
