import os
import logging
from pathlib import Path
from app.source import FREDSource, QuandlSource, FileSource
from app.transformers import FractionalDifferentiationEW, FractionalDifferentiationFFD, Differentiation, PercentageChange
from app.managers import ManagerDashboard
from app.views import DashboardView


if __name__ == '__main__':
    # Config Logging
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

    BASE_DIR = Path(__file__).resolve().parent

    ANALYSIS_PATH = os.path.join(BASE_DIR, 'dashboards')

    if not os.path.exists(ANALYSIS_PATH):
        logging.info("[+] The directory has been created.")
        os.mkdir(ANALYSIS_PATH)

    # Define Manager
    manager = ManagerDashboard(path=ANALYSIS_PATH)

    # **************** Register Transformers ***************************
    differentiation_transform = Differentiation(units_show='Returns')
    fractional_diff_transform = FractionalDifferentiationEW(units_show='Fractional Return')
    fractional_diff_ffd_transform = FractionalDifferentiationFFD(units_show='FFD Return')
    percentage_change_transform = PercentageChange(units_show='Percentage Change')
    percentage_change_from_year_transform = PercentageChange(name="Percentage Change from Year Ago", units_show='Percentage Change from Year Ago', periods=12)

    manager.transformers.register(fractional_diff_transform)
    manager.transformers.register(fractional_diff_ffd_transform)
    manager.transformers.register(differentiation_transform)
    manager.transformers.register(percentage_change_transform)
    manager.transformers.register(percentage_change_from_year_transform)


    # ******************* Create Source Managers ******************************
    fred_credentials = os.path.join(BASE_DIR, "yPcGSNxzHWLUDx--Wwxp")
    fred_source = FREDSource(fred_credentials=fred_credentials)
    quandl_source = QuandlSource(api_key="<462c9e430957fbc1f835c6bc7e7c3e64>")

    # File source
    file_source_dir = os.path.join(BASE_DIR, "datasets", 'yields')
    file_source = FileSource(dir=file_source_dir)

    manager.source.register(fred_source)
    manager.source.register(quandl_source)
    manager.source.register(file_source)

    manager.load()

    # ******************************************** Create Figures *************************************
    logging.info("[+] Render dashboards...")

    dashboard_view = DashboardView(title="Dashboard", manager=manager)

    dashboard_view.show()
