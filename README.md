**Activate the virtual environment**

*Bash*
```
source blockchain-env/bin/activate
```
*Powershell*
```
.\blockchain-env\Scripts\Activate.ps1
```

**Install all packages**
```
pip3 install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment

```
python3 -m pytest backend/tests
```

**Run the application and API**

```
python3 -m backend.app
```

**Running multiple peer instances (from the same computer)**

- Use the --trainer, --validator, --peer, parameters when running the app. If no parameter is given, the server starts as root user.
