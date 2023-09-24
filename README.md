# Search Engine
One of the projects in **Computation Methods for Science and Technology**, Computer Science AGH UST course

## Theoretical report
[Theoretical report (with search queries examples)](report.pdf)

## Technologies used
**Python** with **Django** framework

## How to run

### Wikipedia articles download
Run `python3 wiki_data/wiki_download.py`.<br>
In order to modify the quantity of articles add or remove elements from `KEYWORDS` list in aforementioned file.  

### Search initialization
Initialization parameters can be altered in `config.py` file.<br>
To start the initialization, run `python3 engine/main.py`.

### Django aplication start
Run `python3 manage.py runserver 8000` in order to start application on `http://localhost:8000/`.
