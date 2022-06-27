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

- First you must set environment variable in the terminal


*Bash*
```
export PEER=True 
```

*Powershell*
```
$Env:PEER = "True"
```

- Then run the code below
```
python -m backend.app
```