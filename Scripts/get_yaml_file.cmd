@echo off
setlocal enabledelayedexpansion

:: 1. Hardcode your permanent CML credentials here
set "CML_URL=192.168.178.99"
set "CML_USER=george"
set "CML_PASS=Geo19mai1977"

:: Initialize variables
set "LAB_ID="
set "LAB_NAME="

echo ==========================================
echo       CML Fetch Script Initialized        
echo ==========================================
echo.

:ASK_ID
set /p "HAS_ID=Do you have the Lab ID? (Y/N): "
if /i "%HAS_ID%"=="Y" (
    set /p "LAB_ID=Please enter the Lab ID: "
    goto :BUILD_COMMAND
)
if /i "%HAS_ID%"=="N" (
    goto :ASK_NAME
)
echo Invalid choice. Please enter Y or N.
goto :ASK_ID

:ASK_NAME
set /p "HAS_NAME=Do you have the Lab Name instead? (Y/N): "
if /i "%HAS_NAME%"=="Y" (
    set /p "LAB_NAME=Please enter the Lab Name: "
    goto :BUILD_COMMAND
)
if /i "%HAS_NAME%"=="N" (
    echo.
    echo Error: You must provide either a Lab ID or a Lab Name to proceed.
    echo Exiting script...
    pause
    exit /b 1
)
echo Invalid choice. Please enter Y or N.
goto :ASK_NAME

:BUILD_COMMAND
:: Build the core Python command with static credentials
set "CMD_ARGS=--cmlUrl "%CML_URL%" --cmlUsername "%CML_USER%" --cmlPassword "%CML_PASS%""

:: Append Lab ID if it was provided
if not "%LAB_ID%"=="" (
    set "CMD_ARGS=!CMD_ARGS! --labID %LAB_ID%"
)

:: Append Lab Name if it was provided
if not "%LAB_NAME%"=="" (
    set "CMD_ARGS=!CMD_ARGS! --labName "%LAB_NAME%""
)

echo.
echo Running Python script with your parameters...
echo.

:: Execute the python script
python "Z:\Cisco\CML GIT\CML\Python\fetch.py" !CMD_ARGS!

endlocal
pause