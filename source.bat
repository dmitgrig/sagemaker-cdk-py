@echo off

rem The sole purpose of this script is to make the command
rem
rem     source .venv/bin/activate
rem
rem (which activates a Python virtualenv on Linux or macOS) work on Windows.
rem On Windows, this command just runs this batch file (the argument is ignored).
rem
rem Now we don't need to document a separate Windows command for activating a virtualenv.

echo Executing .venv\Scripts\activate.bat for you
call .venv\Scripts\activate.bat