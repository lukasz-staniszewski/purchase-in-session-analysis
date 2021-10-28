<h1 align="center"> ANALYSIS AND PREDICTION ON USER PURCHASE DEPENDING ON HIS SHOP'S SESSION </h1>
<h3 align="center">Łukasz Staniszewski & Bartosz Cywiński</h1>
<h3 align="center">Warsaw University of Technology</h1>

------------
Project Description (PL)
------------
Projekt realizowany jest w ramach przedmiotu Inżynieria Uczenia Maszynowego (IUM).

W ramach projektu wcielamy się w rolę analityka pracującego w firmie „eSzoppping” – sklepu internetowego z elektroniką i grami komputerowymi. Praca na tym stanowisku nie jest łatwa – zadanie dostajemy w formie enigmatycznego opisu i to do nas należy doprecyzowanie szczegółów tak, aby dało się je zrealizować. To oczywiście wymaga zrozumienia problemu, przeanalizowania danych, czasami negocjacji z szefostwem. Poza tym, oprócz przeanalizowania zagadnienia i wytrenowania modeli, musimy przygotować je do wdrożenia produkcyjnego – zakładając, że w przyszłości będą pojawiać się kolejne ich wersje, z którymi będziemy
eksperymentować. Jak każda szanująca się firma internetowa, eSzoppping zbiera dane dotyczące swojej działalności –
są to:
+ baza użytkowników,
+ katalog produktów,
+ historia sesji użytkowników,
+ dane dotyczące wysyłki zakupionych produktów.

<b>Zadanie: Dobrze byłoby wiedzieć czy dana sesja użytkownika zakończy się zakupem. Dzięki temu
nasi konsultanci będą mogli baczniej przyglądać się tym sesjom i szybciej rozwiązywać
potencjalne problemy.</b>

------------

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── project_name       <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── tests              <- Unit tests
    |
    ├── poetry.lock        <- Lockfile which allows complete environment reproduction
    │
    └── pyproject.toml     <- file with settings and dependencies for the environment


--------


Setting up the environment
------------

1. Install `poetry`: https://python-poetry.org/docs/#installation
2. Create an environment with `poetry install`
3. Run `poetry shell`
4. To add a new package run `poetry add <package>`. Don't forget to commit the lockfile.
5. To run unit tests for your service use `poetry run pytest` or simply `pytest` within `poetry shell`.

<p><small>Project partially based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
