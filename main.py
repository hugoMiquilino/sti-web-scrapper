from threading import Thread
from queue import Queue
from time import sleep
import pandas as pd
import logging
import traceback
import sys


from src.modules import sti_module, plan_module, request_module
from gui.base import StatusGUI
from gui.log_handler import GuiLogHandler
from src.logs.logger import setup_logger

logger = logging.getLogger("tnb")

def worker():

    while True:
        try:

            logger.info("Iniciando novo ciclo")
            
            sti_df = sti_module()
            # sti_df.to_csv("sti.csv", index=False)
            logger.info("Dados STI carregados.")
            
            try:
                plan_df = plan_module()
                # plan_df.to_csv("plan.csv")
                if plan_df is not None:
                    logger.info("Dados PLAN carregados.")
            except Exception:
                logger.warning("Erro ao coletar dados da Planilha.")

            if sti_df is not None and plan_df is not None:
                df = pd.merge(plan_df, sti_df, on="Veiculo", how="outer")
                df.to_csv("r.csv", index=False)
                logger.info("Realizando merge dos dados")
            elif sti_df is not None:
                df = sti_df
                logger.info("Apenas dados da STI coletados.")
            elif plan_df is not None:
                df = plan_df
                logger.info("Apenas dados da tabela coletados.")
            else:
                logger.warning("Nenhum dado coletado. Aguardando próximo ciclo.")
                sleep(10)
                continue

            logger.info("Iniciando envio dos dados")
            request_module(df)

            logger.info("Ciclo finalizado. Aguardando próximo ciclo...\n")
            sleep(10)

        except Exception as e:
            logger.exception("Erro no ciclo")
            sleep(10)


if __name__ == "__main__":
    
    gui_queue = Queue()

    logger, _, listener = setup_logger()

    gui_handler = GuiLogHandler(gui_queue)
    logger.addHandler(gui_handler)

    Thread(target=worker, daemon=True).start()

    app = StatusGUI(gui_queue)
    app.mainloop()

    listener.stop()
