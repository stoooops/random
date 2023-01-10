@echo off
REM Author: Cory Gabrielsen
REM Date: 2023-01-10
REM Description: This script will help you debug ssh issues by displaying the ssh config file
REM and the contents of the IdentityFile.  It will also run ssh -G test and display the results.
REM This script is intended to be run on a Windows machine.
REM

REM display the contents of the ssh config file located in the .ssh directory under
REM the user's profile.

REM Must pass the hostname as the first argument to this script
if "%1"=="" goto :usage

echo ^>        USERPROFILE: %USERPROFILE%
echo ^>        Running ssh -G %1...
ssh -G "%1" 2>&1 > ssh_G.txt
echo ^>        Result written to ssh_G.txt
echo ^>        ssh_G.txt contents:
set /p first_line=<ssh_G.txt
echo %first_line%
echo ....


echo ^>       Finding IdentityFile from ssh_G.txt...
set found=
rem search through the ssh_G.txt file for the IdentityFile line
for /f "tokens=2 delims= " %%i in ('findstr /i "identityfile" ssh_G.txt') do set found=%%i
for /f "tokens=2 delims= " %%i in ('findstr /i "identityfile" ssh_G.txt') do echo identityfile %%i
echo ^>       identityfile %found%

echo Connecting to host: %1...
ssh "%1"

rem usage instructions
:usage
echo.
echo Usage: debug_ssh.bat hostname
echo Example: debug_ssh.bat test.example.com
echo.
echo This script will help you debug ssh issues by displaying the ssh config file
echo and the contents of the IdentityFile.  It will also run ssh -G test and display the results.
echo This script is intended to be run on a Windows machine.
echo.
