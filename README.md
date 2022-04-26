* **Activate the virtual environment**

*Bash*
```
source blockchain-env/bin/activate
```
*Powershell*
```
.\blockchain-env\Scripts\Activate.ps1
```

* **Install all packages**
```
pip3 install -r requirements.txt
```

* **Run the tests**

Make sure to activate the virtual environment

```
python3 -m pytest backend/tests
```

* **Run the application and API**

```
python3 -m pytest backend.app
```