cd /d "%~dp0"
call direnv\Scripts\activate.bat
start cmd /k "streamlit run main_wb_you.py"
