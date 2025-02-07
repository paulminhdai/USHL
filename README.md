# USHL Report

## Introduction

Hello...

## Test Data

You can access the test data [here](https://drive.google.com/drive/folders/1k5DFcgBe62dAvTToKlrrdpJElkOn78Sk?usp=sharing).

## Setup Instructions

To set up the project, follow these steps:

1. Create a virtual environment:
    ```bash
    python3 -m venv myenv
    ```

2. Activate the virtual environment:
    ```bash
    source myenv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip3 install -r requirements.txt
    ```

4. Run the main script:
    ```bash
    python3 main.py
    ```
    
5. Export application to exe file:
    ```bash
    pyinstaller --onefile --name YourDesiredName main.py
    ```
    OR if you want to include an icon for your executable, you can use the --icon option
    ```bash
   pyinstaller --onefile --name my_app --icon=icon.ico app.py
    ```
    try this
   ```bash
   pyinstaller --add-data="static:static" --onefile --windowed --name USHLReport_v main.py
   ```
    
7. Deactivate the virtual environment when done:
    ```bash
    deactivate
    ```

## Contributor

Dai Vuong

## License

This project is licensed under the MIT License.
