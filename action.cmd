@echo off
@if not “%~0″==”%~dp0.\%~nx0″ start /min cmd /u /k "py ./codes/main.py & pause & exit",”%~dp0.\%~nx0” %* & goto :eof


