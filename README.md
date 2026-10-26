![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

# PokeGutkowo
![logo](logo.png)\
Aplikacja mająca na celu zrzeszenie gutkowiańskich graczy PokemonGO.\
*Cii, mam fobię społeczną i pewnie jej nigdy nie użyję, ale może się uda XD*

## Wymagania

- Python **3.15.1** zarządzany przez **pyenv** (plik `.python-version`).
- Node.js **22.12+** i npm. Lokalnie sprawdzono Node.js 26.12.1 / npm 11.20.0.
- Django **6.1.2**, Django REST Framework **3.18.3**.
- React **19.3.1**, React Router **7.18.4**, Bootstrap **5.3.8**.
- Vite **8.3.5** zamiast Create React App, Vitest **5.0.5** do testów interfejsu.

Zależności bezpośrednie są przypięte do wersji sprawdzonych 26.10.2026.
`frontend/package-lock.json` przechowuje komplet zależności npm.

## Instalacja

W katalogu repozytorium:

```sh
pyenv install -s 3.15.1
pyenv exec python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_dev.txt
python manage.py migrate
npm --prefix frontend ci
```

Do instalacji samego backendu wystarczy `requirements.txt`. Domyślna lokalna baza
to SQLite (`db.sqlite3`), więc PostgreSQL i `settings_local.py` nie są wymagane.
Nowa baza jest pusta; API zwraca puste listy i pusty obiekt ustawień.

Jeśli kompilacja Pythona na macOS zgłasza brak `gdbm-ndbm.h`, sprawdzony wariant to:

```sh
env ac_cv_header_gdbm_dash_ndbm_h=no ac_cv_header_gdbm_slash_ndbm_h=no \
  PYTHON_CONFIGURE_OPTS='--with-dbmliborder=ndbm' pyenv install -s 3.15.1
```

## Uruchomienie lokalne

W pierwszym terminalu, w katalogu repozytorium:

```sh
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

W drugim terminalu:

```sh
npm --prefix frontend start
```

Otwórz [aplikację](http://127.0.0.1:3000/).
[Panel administracyjny](http://127.0.0.1:8000/admin/) umożliwia dodawanie graczy,
postów i pojedynczego rekordu ustawień strony. Konto administratora tworzysz przez:

```sh
.venv/bin/python manage.py createsuperuser
```

Vite przekazuje API, media i panel administracyjny do Django na porcie 8000.
Adres widoku graczy to `/players`, a adres API to `/players/`.
Pozostałe endpointy API: `/posts/` oraz `/settings/`.

## Testy i kompilacja

```sh
.venv/bin/python manage.py check --fail-level WARNING
.venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python -m pytest --cov=pokegutkowo --cov-report=term-missing
.venv/bin/ruff check .
.venv/bin/python -m pip check
npm --prefix frontend run test:coverage
npm --prefix frontend run build
npm --prefix frontend audit
npm --prefix frontend outdated
```

Testy obejmują puste i wypełnione API, serializację autorów, ustawienia strony,
panel administracyjny z CKEditor 5, zachowanie HTML po migracji, ograniczenia uploadu i CORS, routing Reacta,
paginację, błędy sieci/HTTP/JSON, StrictMode oraz oczyszczanie HTML postów.

Gotowy frontend powstaje w `frontend/dist/`. Podgląd kompilacji, przy działającym
backendzie, uruchamia `npm --prefix frontend run preview` (port 3000; wcześniej
zatrzymaj serwer developerski frontendu).

## Konfiguracja i zgodność danych

- PostgreSQL: ustaw `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`,
  `POSTGRES_HOST` i opcjonalnie `POSTGRES_PORT`. Sterownik to `psycopg` 3.
- Własne ustawienia można też wpisać do `project/settings_local.py`, kopiując
  `project/settings_local.example`. Ten plik jest ignorowany przez Git.
- `DJANGO_DEBUG`, `DJANGO_SECRET_KEY` i `DJANGO_ALLOWED_HOSTS` sterują podstawową
  konfiguracją. Zmienne należy wyeksportować w terminalu; plik `.env` nie jest
  automatycznie wczytywany. Domyślne ustawienia i klucz służą do pracy lokalnej.
- Migracja `0003_alter_post_context` zachowuje HTML istniejących postów w polu
  tekstowym. Panel korzysta z CKEditor 5. Pakiet `django-ckeditor` pozostaje jedynie
  do odczytu historycznej migracji `0001`; aplikacja i pliki CKEditor 4 nie są
  udostępniane. Frontend oczyszcza HTML przez DOMPurify.
- Dawne, nieużywane integracje Codecov/Coveralls i zestaw wtyczek flake8 zastąpił
  aktualny zestaw pytest / pytest-cov / Ruff. Aktualne narzędzia developerskie są
  w `requirements_dev.txt`.

Lokalną weryfikację wykonano na macOS 27.0.1, Pythonie 3.15.1 z pyenv oraz SQLite.
