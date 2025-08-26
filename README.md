# 📊 Survey Explorer App

Aplikacja w Streamlit do interaktywnej eksploracji wyników ankiety powitalnej.

## 🚀 Jak uruchomić lokalnie
0. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/TWOJ_LOGIN/survey-explorer.git
   cd survey-explorer

1. Upewnij się, że masz zainstalowane wymagane biblioteki:

   Możesz utworzyć nowe środowisko:
   ```
   conda create -n survey-explorer python=3.11
   ```
   Później aktywuj środowisko i doinstaluj biblioteki:
   ```
   conda activate survey-explorer
   pip install -r requirements.txt
   ```
   
   Jeśli używasz środowiska Conda, możesz od razu utworzyć nowe środowisko wraz z bibliotekami:
   ```
   conda env create -f environment.yml
   ```

   Lub zaktualizować istniejące środowisko
   ```
   conda env update -f environment.yml --prune
   
2. Plik env.template zawiera dwie zmienne środowiskowe PATH_DATA oraz FILE_NAME, które należy uzupełnić odpowiednio:
   - ścieżką do katalogu w którym znajduje się plik csv,
   - nazwą pliku csv dostarczonego wraz z projektem.

   Po uzupełniu nazwę env.template należy zmienić na .env.
   ```

3. Uruchom aplikację:
   ```
   streamlit run app.py
   ```

   Aplikacja powinna otworzyć się automatycznie w Twojej przeglądarce internetowej pod adresem `http://localhost:8501`.

## Zawartość aplikacji
Aplikacja survey-explorer zawiera dwa panele do przeglądania wyników ankiety z pliku .csv:
* Pierwszy panel (filtry) zawiera listę filtrów za pomocą których *wybieramy interesujące na cechy ankietowanej populacji do analizy.
* Drugi panel (prezentacja) przedstawia nam wyniki ankiety w postaći kilku wybranych statystyk, wykresu kołowego i histogramu oraz formie tabelarycznej.

## Eksperymentowanie z kodem

Zachęcamy do eksperymentowania z kodem źródłowym aplikacji:

1. Otwórz plik `app.py` w swoim ulubionym edytorze kodu
2. Modyfikuj istniejące komponenty lub dodaj własne
3. Zapisz zmiany - aplikacja automatycznie się przeładuje w przeglądarce

## Przydatne zasoby

- [Oficjalna dokumentacja Streamlit](https://docs.streamlit.io/)
- [Galeria przykładów Streamlit](https://streamlit.io/gallery)
- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)