# STI Web Scrapper

[Português](./README.md)

> This project was developed during university, but it was a real solution used in production by the company where the author worked at the time. The automation was created to solve a concrete operational need in fleet monitoring.

Python application designed to automate the collection of STI tracking data, enrich it with fleet spreadsheet information, and send the records to AppSheet.

## Overview

This project was built to monitor and update vehicle information in real time, including:

- Vehicle
- Driver
- Trailer 1 and Trailer 2
- Status
- Speed
- Location
- State/UF

The application performs the following steps:

1. Accesses the STI portals through Selenium
2. Collects information from HTML/JavaScript pages
3. Reads the Excel fleet planning sheet
4. Combines the data by vehicle
5. Sends the data to AppSheet tables
6. Displays operational status in a desktop graphical interface

## Technologies

- Python 3
- Selenium
- Pandas
- Tkinter + ttkbootstrap
- AppSheet API

## Requirements

- Python 3.10 or newer
- Google Chrome or Chromium installed
- Project dependencies installed

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/hugoMiquilino/sti-web-scrapper.git
cd sti-web-scrapper
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
USER=your_sti_user
PASSWD=your_sti_password
APPSHEET_APP_ID=your_appsheet_app_id
APPSHEET_ACCESS_KEY=your_appsheet_access_key
APPSHEET_TABLE_NAME_FROTA=fleet_table_name
APPSHEET_TABLE_NAME_VEICULOS=vehicles_table_name
```

These variables are used in:

- `src/modules/sti_module.py` for authentication to the STI portal
- `src/modules/request_module.py` for authentication and data upload to AppSheet

## Running the app

To start the application:

```bash
python main.py
```

When executed, the application:

- starts the data collection cycle in the background
- records logs
- opens the status graphical interface
- keeps the process running in a loop with update intervals

## Project structure

```text
sti-web-scrapper/
├─ gui/
│  ├─ assets/
│  ├─ base.py
│  └─ log_handler.py
├─ src/
│  ├─ docs/
│  │  └─ conversion_dict.json
│  ├─ logs/
│  │  └─ logger.py
│  ├─ modules/
│  │  ├─ __init__.py
│  │  ├─ sti_module.py
│  │  ├─ plan_module.py
│  │  └─ request_module.py
│  └─ utils/
│     └─ path.py
├─ main.py
├─ requirements.txt
├─ .gitignore
├─ README.md
├─ README.en.md
└─ .env
```

## Application flow

- `main.py` starts the application and the background worker
- `sti_module.py` accesses the STI portal and transforms the data into a DataFrame
- `plan_module.py` reads the Excel fleet data sheet
- `request_module.py` builds the payload and sends the information to AppSheet
- the system also saves a `r.csv` file with the merged result for analysis

## Important notes

- STI data collection depends on the availability and structure of the external portal.
- The project uses Selenium in headless mode.
- The Excel file path is defined in `src/modules/plan_module.py` and may need adjustment depending on the local environment.
- The project is focused on a Windows environment, especially because of local path usage and the desktop interface.

## License

This project does not currently have a license defined in the repository.

[Back to Portuguese](./README.md)
