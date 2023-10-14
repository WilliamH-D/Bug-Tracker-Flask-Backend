@ECHO OFF
$env:FLASK_APP = "application.py"
ECHO Starting application: %FLASK_APP%...
flask run