## Starting the app:

1. start a virtual env:

```
    python -m virtualenv .
    source ./bash/activate
```
Or using a shell like fish (my personal case)

```
    source ./bin/activate.fish
```

2. Install the packages described in the requirements.txt:

```
pip install -r requirements.txt
```

3. Set the flask global variable

```
export FLASK_APP=app
```

4. Start the application

```
flask run
```