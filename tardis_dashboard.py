import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px #interactive charts
import joblib
from datetime import datetime
st.set_page_config (
    page_title = "Real-Time Data Dashboard Trains Delay",
    page_icon = "Active",
    layout = "wide",
)

TARGET = "Retard moyen de tous les trains à l'arrivée"

CAUSE_COLS = [
    "Prct retard pour causes externes",
    "Prct retard pour cause infrastructure",
    "Prct retard pour cause gestion trafic",
    "Prct retard pour cause matériel roulant",
    "Prct retard pour cause gestion en gare et réutilisation de matériel",
    "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)",
]
CAUSE_LABELS = [
    "Causes externes",
    "Infrastructure",
    "Gestion trafic",
    "Matériel roulant",
    "Gestion en gare",
    "Voyageurs",
]

@st.cache_data #anything you CAN store in a database(python, dataframe, API call)
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")
    df["Annee"] = df["Date"].dt.year
    df["Mois"] = df["Date"].dt.month
    df["liaison"] = df["Gare de départ"] + " -> " + df["Gare d'arrivée"]
    return df


@st.cache_resource #anything you CAN'T store in a database(ML models, database connections)
def load_model():
    return joblib.load("model.joblib")


df = load_data()
model_data = load_model()
model = model_data["model"]
X_columns = model_data["X_columns"]

st.sidebar.title("Filtres")

annees = sorted(df["Annee"].dropna().unique().astype(int))
selected_years = st.sidebar.multiselect("Annees", annees, default=annees)

gares_dep = sorted(df["Gare de départ"].dropna().unique())
selected_gare = st.sidebar.selectbox("Gare de depart", ["Toutes"] + list(gares_dep))

services = sorted(df["Service"].dropna().unique())
selected_service = st.sidebar.multiselect("Service", services, default=services)

df_f = df[df["Annee"].isin(selected_years)]
if selected_gare != "Toutes":
    df_f = df_f[df_f["Gare de départ"] == selected_gare]
if selected_service:
    df_f = df_f[df_f["Service"].isin(selected_service)]

st.title("TARDIS - Prediction des retards SNCF")
st.markdown(f"Analyse des retards TGV sur le reseau national francais - **{len(df_f):,}** trajets")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Retard moyen a l'arrivee", f"{df_f[TARGET].mean():.1f} min")
col2.metric("Trajets analyses", f"{len(df_f):,}")
col3.metric("Ponctualite (<=5 min)", f"{(df_f[TARGET] <= 5).mean() * 100:.1f}%")
col4.metric("Taux annulation moyen", f"{(df_f['Nombre de trains annulés'] / df_f['Nombre de circulations prévues']).mean() * 100:.1f}%")
#shows the average of all cumulative years with the number of identified trips, put in minute and percentage with the graphic
st.divider()

tab1, tab2, tab3 = st.tabs(["Visualisations", "Prediction", "Donnees"])

with tab1:
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.subheader("Distribution des retards moyens")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(df_f[TARGET].dropna(), bins=40, color="steelblue", edgecolor="white", alpha=0.85)
        ax.axvline(df_f[TARGET].mean(), color="red", linestyle="--",
                   label=f"Moyenne : {df_f[TARGET].mean():.1f} min")
        ax.axvline(df_f[TARGET].median(), color="orange", linestyle="--",
                   label=f"Mediane : {df_f[TARGET].median():.1f} min")
        ax.set_xlabel("Retard moyen (min)")
        ax.set_ylabel("Frequence")
        ax.legend()
        st.pyplot(fig)
        plt.close()

    with col_v2:
        st.subheader("Evolution du retard moyen par annee")
        retard_annee = df_f.groupby("Annee")[TARGET].mean().reset_index().sort_values("Annee")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(retard_annee["Annee"].astype(str), retard_annee[TARGET],
               color="steelblue", alpha=0.8, edgecolor="white")
        ax.plot(retard_annee["Annee"].astype(str), retard_annee[TARGET],
                color="red", marker="o", linewidth=2)
        ax.set_xlabel("Annee")
        ax.set_ylabel("Retard moyen (min)")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)
        plt.close()

    col_v3, col_v4 = st.columns(2)

    with col_v3:
        st.subheader("Saisonnalite mensuelle")
        retard_mois = df_f.groupby("Mois")[TARGET].mean().reset_index()
        mois_labels = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun",
                       "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(retard_mois["Mois"], retard_mois[TARGET],
                marker="o", color="steelblue", linewidth=2.5)
        ax.fill_between(retard_mois["Mois"], retard_mois[TARGET], alpha=0.15, color="steelblue")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(mois_labels, rotation=45)
        ax.set_xlabel("Mois")
        ax.set_ylabel("Retard moyen (min)")
        st.pyplot(fig)
        plt.close()

    with col_v4:
        st.subheader("liaisons les plus en retard")
        top_n = st.slider("Nombre de liaisons", 5, 20, 10, key="top_liaison")
        top_retard = (
            df_f.groupby("liaison")[TARGET]
            .mean()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )
        fig, ax = plt.subplots(figsize=(7, max(4, top_n * 0.4)))
        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(top_retard)))
        ax.barh(top_retard["liaison"], top_retard[TARGET], color=colors, edgecolor="white")
        ax.set_xlabel("Retard moyen (min)")
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.subheader("Repartition des causes de retard")
    cause_means = df_f[CAUSE_COLS].mean()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(cause_means, labels=CAUSE_LABELS, autopct="%1.1f%%",
           startangle=45, colors=plt.cm.tab10.colors)
    ax.set_title("Causes de retard (moyennes sur la selection)")
    st.pyplot(fig)
    plt.close()
#all partie of the graph for analysie
with tab2:
    st.subheader("Predire le retard d'un trajet")
    st.markdown("Renseignez les caracteristiques du trajet pour obtenir une estimation du retard moyen a l'arrivee")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Trajet**")
        gare_dep = st.selectbox("Gare de depart", sorted(df["Gare de départ"].dropna().unique()))
        gare_arr = st.selectbox("Gare d'arrivee", sorted(df["Gare d'arrivée"].dropna().unique()))
        service = st.selectbox("Type de service", sorted(df["Service"].dropna().unique()))
        #choice your traject for predict the potentiel delay
    with col_b:
        st.markdown("**Temporel**")
        mois_pred = st.slider("Mois", 1, 12, 6)
        annee_pred = st.selectbox("Annee", list(range(min(annees), max(annees) +11)), index=len(annees) - 1)#time of choice your prediction

    st.divider()

    if st.button("Predire le retard", type="primary"):
        cleaned_df = pd.read_csv("cleaned_dataset.csv")

        df_test = pd.DataFrame({
            "Gare de départ": [gare_dep],
            "Gare d'arrivée": [gare_arr],
            "Service": [service],
            "Date": [f"{annee_pred}-{str(mois_pred).zfill(2)}"],
            "Durée moyenne du trajet": [None],
            "Nombre de circulations prévues": [None],
            "Nombre de trains annulés": [None],
            "Commentaire annulations": [None],
            "Nombre de trains en retard au départ": [None],
            "Retard moyen des trains en retard au départ": [None],
            "Retard moyen de tous les trains au départ": [None],
            "Commentaire retards au départ": [None],
            "Nombre de trains en retard à l'arrivée": [None],
            "Retard moyen des trains en retard à l'arrivée": [None],
            "Commentaire retards à l'arrivée": [None],
            "Nombre trains en retard > 15min": [None],
            "Retard moyen trains en retard > 15 (si liaison concurrencée par vol)": [None],
            "Nombre trains en retard > 30min": [None],
            "Nombre trains en retard > 60min": [None],
            "Prct retard pour causes externes": [None],
            "Prct retard pour cause infrastructure": [None],
            "Prct retard pour cause gestion trafic": [None],
            "Prct retard pour cause matériel roulant": [None],
            "Prct retard pour cause gestion en gare et réutilisation de matériel": [None],
            "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)": [None],
        })

        def search_similate(cdf, df_t):
            GD = df_t["Gare de départ"].iloc[0]
            GA = df_t["Gare d'arrivée"].iloc[0]
            S = df_t["Service"].iloc[0]
            Date = df_t["Date"].iloc[0]

            target_date = datetime.strptime(Date, "%Y-%m")
            year = target_date.year
            month = target_date.month

            df_t["Annee"] = year
            df_t["Mois"] = month

            cdf["Date"] = pd.to_datetime(cdf["Date"], format="%Y-%m")
            cdf["Annee"] = cdf["Date"].dt.year
            cdf["Mois"] = cdf["Date"].dt.month

            filters = [
                (cdf["Gare d'arrivée"] == GA),
                (cdf["Mois"] == month),
                (cdf["Gare de départ"] == GD),
                (cdf["Annee"] == year),
                (cdf["Service"] == S),
            ]

            for i in range(len(filters), 0, -1):
                mask = filters[:i][0]
                for f in filters[:i][1:]:
                    mask = mask & f
                result = cdf[mask]
                if not result.empty:
                    for col in df_t.columns:
                        if col in result.columns and pd.isna(df_t[col].iloc[0]):
                            df_t.at[0, col] = result.iloc[0][col]
                    return True
            return False

        search_similate(cleaned_df, df_test)

        df_test = pd.get_dummies(
            df_test,
            columns=[
                "Gare de départ",
                "Gare d'arrivée",
                "Service",
                "Commentaire annulations",
                "Commentaire retards à l'arrivée",
                "Commentaire retards au départ",
            ],
            drop_first=True,
        )

        df_test = df_test.drop("Date", axis=1)
        df_test = df_test.reindex(columns=X_columns, fill_value=0)

        prediction = model.predict(df_test)[0]

        if prediction < 5:
            st.success(f"Retard estime : **{prediction:.1f} minutes** - Trajet ponctuel")
        elif prediction < 15:
            st.warning(f"Retard estime : **{prediction:.1f} minutes** - Leger retard previsible")
        else:
            st.error(f"Retard estime : **{prediction:.1f} minutes** - Retard important previsible")

        df_liaison = df[
            (df["Gare de départ"] == gare_dep) & (df["Gare d'arrivée"] == gare_arr)
        ]
        if len(df_liaison) > 0:
            moy_liaison = df_liaison[TARGET].mean()
            st.info(
                f"Retard moyen historique sur **{gare_dep} → {gare_arr}** : "
                f"**{moy_liaison:.1f} min** ({len(df_liaison)} observations)"
            )

with tab3:
    st.subheader("Donnees filtrees")
    st.markdown(f"**{len(df_f):,}** lignes selon les filtres")

    DISPLAY_COLS = [
        "Date", "Service", "Gare de départ", "Gare d'arrivée",
        "Annee", "Mois", TARGET,
        "Retard moyen de tous les trains au départ",
    ]
    display_cols_existing = [c for c in DISPLAY_COLS if c in df_f.columns]
    st.dataframe(
        df_f[display_cols_existing].sort_values(TARGET, ascending=False).head(500),
        use_container_width=True,
    )

    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Telecharger les donnees filtrees (CSV)",
        data=csv,
        file_name="sncf_retards_filtres.csv",
        mime="text/csv",
    ) #for user of the application for why whatch the data using for prediction with posibility download the csv