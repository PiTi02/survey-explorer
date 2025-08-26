import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from config.settings import settings
from pathlib import Path

# --------------------------------
# --- BODY PANEL ---
# --------------------------------
def body_panel(df_filtered):

    ordered_all_columns=[
        'age', 'edu_level', 'years_of_experience', 'industry', 
        'gender','sweet_or_salty',
        'fav_animals', 'fav_place','hobby_art',
        'hobby_books', 'hobby_movies', 'hobby_other', 'hobby_sport',
        'hobby_video_games', 'learning_pref_books',
        'learning_pref_chatgpt', 'learning_pref_offline_courses',
        'learning_pref_online_courses', 'learning_pref_personal_projects',
        'learning_pref_teaching', 'learning_pref_teamwork',
        'learning_pref_workshops', 'motivation_career', 'motivation_challenges',
        'motivation_creativity_and_innovation', 'motivation_money_and_job',
        'motivation_personal_growth', 'motivation_remote'
    ]   
    # Lista wszystkich kolumn demograficznych
    demographic_columns = [
        "Przedział wiekowy",
        "Poziom wykształcenia",
        "Branża",
        "Doświadczenie zawodowe",
        "Płeć",
        "Ulubione miejsce wypoczynku",
        "Słodkie vs słone",
        "Ulubione zwierzęta"
    ]
    col_names = {
        "Przedział wiekowy": "age",
        "Poziom wykształcenia": "edu_level",
        "Branża": "industry",
        "Doświadczenie zawodowe": "years_of_experience",
        "Płeć": "gender",
        "Ulubione miejsce wypoczynku": "fav_place",
        "Słodkie vs słone": "sweet_or_salty",
        "Ulubione zwierzęta": "fav_animals"    
    }
    
    # Reorder columns
    df_filtered = df_filtered[ordered_all_columns]

    if "selected_column" not in st.session_state:
        st.session_state["selected_column"] = demographic_columns[0]
    # --- Selectbox ---
    c0, c1 = st.columns([1, 2])
    with c0:
        selected_column = st.selectbox(
            "Zmienna do analizy",
            options=demographic_columns,
            key="selected_column", # teraz trzymamy w session_state
            label_visibility="collapsed"
        )
    with c1:
        st.markdown(
            f"📑 Wybrana kolumna: **{col_names[selected_column]}**"
        )
    # --- Dane do wykresów ---
    col_name = col_names[selected_column]
    counts = df_filtered[col_name].value_counts().reset_index()
    counts.columns = [col_name, "Liczba"]
    counts["Procent"] = counts["Liczba"] / counts["Liczba"].sum() * 100

    # --- Pie chart ---
    fig_pie = px.pie(
        counts,
        names=col_name,
        values="Liczba",
        color=col_name,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(
        textinfo="percent",
        texttemplate="%{percent:.0%}",
        textposition="outside",
        hovertemplate=f"{col_name}: %{{label}}<br>Udział: %{{percent}}<extra></extra>"
    )
    # --- Bar chart ---
    fig_bar = px.bar(
        counts,
        x=col_name,
        y="Liczba",
        color=col_name,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text="Liczba"
    )
    fig_bar.update_traces(
        texttemplate="%{text:.0f}",
        textposition="outside",
        hovertemplate=f"{col_name}: %{{x}}<br>Liczba ankietowanych: %{{y}}<extra></extra>"
    )
    fig_bar.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )
    fig_bar.update_xaxes(showticklabels=False)
    fig_bar.update_yaxes(showticklabels=False)

    # --- Wyświetlenie wykresów ---
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie, use_container_width=True)     
    with c2:
        event_bar = st.plotly_chart(
            fig_bar,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points"
        )
    if event_bar and event_bar.selection and event_bar.selection["points"]:
        selected_points = [point["x"] for point in event_bar.selection["points"]]
        df_filtered = df_filtered[df_filtered[col_name].isin(selected_points)]
        st.success(f"Wybrano: {', '.join(map(str, selected_points))}")
    else:
        st.info("Kliknij kategorię na wykresie słupkowym, aby przefiltrować dane.")
                    
    # --- Podświetlenie tabeli ---
    def highlight(s):
        if s.name == col_name:
            return ['background-color: #ffeeba'] * len(s)
        else:
            return [''] * len(s)

    styled_df = df_filtered.style.apply(highlight, axis=0)

    return styled_df

#--------------------------------
# --- LEFT PANEL --- SIDEBAR
#--------------------------------
def left_panel(df):
    
    with st.sidebar: 
        st.header("🔎 Filtry")
        
        if "resetuj_filter" not in st.session_state:
            st.session_state["resetuj_filter"] = 0

        if st.session_state["resetuj_filter"]:
            st.session_state["age_filter"] = []
            st.session_state["edu_filter"] = []
            st.session_state["industry_filter"] = []
            st.session_state["experience_filter"] = []
            st.session_state["gender_filter"] = "Wszystkie"
            st.session_state["place_filter"] = []
            st.session_state["sweet_salty_filter"] = []
            st.session_state["animal_filter"] = []
            st.session_state["resetuj_filter"] = 0
            
        # Przedział wiekowy
        ages = sorted(df["age"].dropna().unique())
        age_filter = st.multiselect("Przedział wiekowy", options=ages, key="age_filter")
        # Wykształcenie
        edu_levels = sorted(df["edu_level"].dropna().unique())
        edu_filter = st.multiselect("Wykształcenie", options=edu_levels, key="edu_filter")

        # Branża
        industries = sorted(df["industry"].dropna().unique())
        industry_filter = st.multiselect("Branża", options=industries, key="industry_filter")

        # Doświadczenie zawodowe
        experience = sorted(df["years_of_experience"].dropna().unique())
        experience_filter = st.multiselect("Doświadczenie zawodowe", options=experience, key="experience_filter")

        # Płeć
        gender_filter = st.radio("Płeć", options=['Wszystkie','Mężczyźni','Kobiety'], key="gender_filter")

        # Wypoczynek
        fav_places = sorted(df["fav_place"].dropna().unique())
        place_filter = st.multiselect("Wypoczynek", options=fav_places, key="place_filter")

        # Słodkie czy słone
        sweet_or_salty = sorted(df["sweet_or_salty"].dropna().unique())
        sweet_salty_filter = st.multiselect("Słodkie czy słone", options=sweet_or_salty, key="sweet_salty_filter")

        #Ulubione zwierzęta
        fav_animals = sorted(df["fav_animals"].dropna().unique())
        animal_filter = st.multiselect("Ulubione zwierzęta", options=fav_animals, key="animal_filter")        
        
        # przycisk resetu

        if st.button("♻️ Resetuj filtry"):
            st.session_state["resetuj_filter"] = 1
            st.rerun()  # przeładowanie strony


    # --- FILTROWANIE ---
    df_filtered = df.copy()
    if age_filter:
        df_filtered = df_filtered[df_filtered["age"].isin(age_filter)]
    if edu_filter:
        df_filtered = df_filtered[df_filtered["edu_level"].isin(edu_filter)]
    if industry_filter:
        df_filtered = df_filtered[df_filtered["industry"].isin(industry_filter)]
    if experience_filter:
        df_filtered = df_filtered[df_filtered["years_of_experience"].isin(experience_filter)]
    
    if gender_filter == "Kobiety":
        df_filtered = df_filtered[df_filtered["gender"] == 1]
    elif gender_filter == "Mężczyźni":
        df_filtered = df_filtered[df_filtered["gender"] == 0]
    
    if place_filter:
        df_filtered = df_filtered[df_filtered["fav_place"].isin(place_filter)]
    if sweet_salty_filter:
        df_filtered = df_filtered[df_filtered["sweet_or_salty"].isin(sweet_salty_filter)]
    if animal_filter:
        df_filtered = df_filtered[df_filtered["fav_animals"].isin(animal_filter)]

    return df_filtered

# --------------------------------
# --- METRIC WITH DELTA --- 
# --------------------------------
def metric_with_delta(col, title, df, df_filtered, column, help_text):
    """
    Wyświetla metrykę w kolumnie Streamlit z tooltipem i deltą względem całej populacji.
    """
    with col:
        if df_filtered[column].dropna().empty:
            st.metric(title, "brak danych", help=help_text)
        else:
            # moda w próbie przefiltrowanej
            filt_mode = df_filtered[column].mode()[0]

            # udział tej kategorii w populacji
            total_share = round((df[column] == filt_mode).mean() * 100, 1)

            # udział tej kategorii w próbie przefiltrowanej
            filt_share = round((df_filtered[column] == filt_mode).mean() * 100, 1)

            # różnica udziałów (w punktach procentowych)
            delta = round(filt_share - total_share, 1)

            # wyświetlenie metryki
            st.metric(
                title,
                f"{filt_mode}",
                f"{delta:+}%",  # np. +12.3%
                help=help_text
            )

# --------------------------------
# --- HEAD PANEL ---
# --------------------------------
def head_panel(df, df_filtered):
    col1, col2, col3, col4, col5 = st.columns(5)

    # liczba respondentów
    with col1:
        total = len(df)
        filtered = len(df_filtered)
        delta = round((filtered/total)*100 - 100, 1)
        st.metric(
            "Ankietowani", 
            filtered, 
            f"{delta:+}%", 
            help="Liczba ankietowanych po zastosowaniu lub nie filtrów. Delta = zmiana % względem wszystkich ankietowanych."
        )

    # pozostałe metryki
    metric_with_delta(col2, "Przedział wiekowy", df, df_filtered, "age",
        "Pokazuje najczęściej występujący przedział wiekowy. Delta = różnica udziału względem wszystkich ankietowanych.")

    metric_with_delta(col3, "Wykształcenie", df, df_filtered, "edu_level",
        "Pokazuje najczęściej występujący poziom wykształcenia. Delta = różnica udziału względem wszystkich ankietowanych.")

    metric_with_delta(col4, "Branża", df, df_filtered, "industry",
        "Pokazuje najczęściej występującą branżę. Delta = różnica udziału względem wszystkich ankietowanych.")

    metric_with_delta(col5, "Doświadczenie", df, df_filtered, "years_of_experience",
        "Pokazuje najczęściej wskazywany poziom doświadczenia zawodowego. Delta = różnica udziału względem wszystkich ankietowanych.")

# --------------------------------
# --- MAIN FUNCTION ---
# --------------------------------
def main():

st.write(sys.path)
st.write(sys.executable)

    PATH_DATA = Path(settings.PATH_DATA)
    FILE_NAME = settings.FILE_NAME
    file_csv = PATH_DATA / FILE_NAME
    
    # wczytanie danych raz
    if "df" not in st.session_state:
        if file_csv.exists():
            st.session_state["df"] = pd.read_csv(file_csv, sep=";")
        else:
            st.error(f"❌ Nie znaleziono pliku: {file_csv}")
            st.stop()  # zatrzymuje aplikację, żeby nie leciała dalej bez danych

    st.set_page_config(layout="wide")  # szeroki widok
    st.title("📊 Eksploracja ankiety powitalnej") 

    # --- FILTROWANIE DANYCH --- SIDEBAR
    df = st.session_state["df"]
    df_filtered = left_panel(df)

    # --- PODSTAWOWE STATYSTYKI ---
    st.subheader("📝 Ogólne statystyki ankiety")
    head_panel(df, df_filtered)

    # ------- PRZEGLĄD ANKIET ------- WYKRESY
    st.subheader("📈 Wizualizacja danych ankiety")
    df_styled = body_panel(df_filtered)
    
    # ------- PRZEGLĄD ANKIET ------- TABELA
    st.subheader("📑 Dane z ankiety w tabeli")
    st.dataframe(df_styled, hide_index=True)
        
if __name__ == "__main__":
    main()

