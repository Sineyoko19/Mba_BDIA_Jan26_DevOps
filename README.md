# Plateforme d'Analyse Airbnb

## Table des matières

1. Présentation du projet
2. Installation et exécution
3. Description des fonctionnalités
4. Répartition des tâches


## Présentation du projet

### Vue générale

La Plateforme d'Analyse Airbnb est une solution complète de business intelligence conçue pour extraire, transformer et analyser les données Airbnb (annonces, avis clients, informations sur les hôtes). Le projet est développé dans le cadre d'une formation MBA en Business Data Intelligence et DevOps.

### Objectifs

- Centraliser et normaliser les données Airbnb provenant de sources multiples
- Mettre en place un pipeline de transformation de données fiable et maintenable
- Fournir un tableau de bord interactif pour l'exploration et l'analyse des données
- Assurer la qualité et la cohérence des données tout au long du processus

## Objectif fonctionnel

L’utilisateur peut :
- filtrer les annonces Airbnb en temps réel
- comparer les prix par type de logement
- analyser les tendances des avis
- identifier les hôtes les plus performants

### Architecture générale

Le projet suit une architecture en trois couches:

1. **Raw Data:** Données brutes chargées à partir de fichiers CSV
2. **Silver Layer:** Données nettoyées, normalisées et validées (déduplication, formatage)
3. **Gold Layer:** Données transformées et enrichies, prêtes pour l'analyse

**Stack technologique:**
- dbt (data build tool): Orchestration et transformation des données SQL
- DuckDB: Base de données analytique locale
- Streamlit: Interface web pour la visualisation et l'exploration
- Plotly: Bibliothèque de visualisation avancée


## Installation et exécution

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Accès en lecture/écriture au répertoire du projet

### Procédure d'installation

#### 1. Cloner le repository

```bash
git clone https://github.com/Sineyoko19/Mba_BDIA_Jan26_DevOps
cd Mba_BDIA_Jan26_DevOps
```

#### 2. Créer et activer l'environnement virtuel

```bash
python -m venv venv
source venv\Scripts\activate
```

#### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Dépendances principales:**
- dbt-core
- dbt-duckdb
- pandas
- streamlit
- plotly

#### 4. Configurer dbt

Créez le fichier `~/.dbt/profiles.yml` avec la configuration suivante:

```yaml
airbnb_analytics_platform:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: 'dev.duckdb'
      threads: 4
      schema: main
```

Validez la configuration:

```bash
dbt debug
```

### Procédure d'exécution

#### Charger et transformer les données

```bash
# Charger les données brutes (CSV -> Base DuckDB)
dbt seed

# Exécuter les transformations (Raw -> Silver -> Gold)
dbt run

#### Lancer le dashboard

```bash
cd streamlit_app
streamlit run app.py
```

Le dashboard sera accessible à l'adresse `http://localhost:8501`

---

## Description des fonctionnalités

### Transformation des données

#### Modèles Silver (nettoyage et normalisation)

- **silver_hosts:** Nettoyage des données hôte (déduplication, formatage des dates, validation)
- **silver_listings:** Normalisation des annonces (formatage des prix, validation des champs)
- **silver_reviews:** Traitement des avis (déduplication, ajout du sentiment basique)
- **silver_full_moon_dates:** Génération des dates de pleine lune

#### Modèles Gold (agrégation et enrichissement)

- **gold_hosts:** Profils hôte enrichis avec métriques de performance
  - Nombre d'annonces actives
  - Nombre total d'avis
  - Taux d'avis positifs
  - Score de performance global

- **gold_listings:** Annonces enrichies avec données associées
  - Informations détaillées de l'hôte
  - Statistiques d'avis (sentiment moyen, nombre total)
  - Prix moyen et fourchette
  - Score de popularité

- **gold_reviews:** Avis avec contexte complet
  - Informations de l'annonce associée
  - Données de l'hôte
  - Classification du sentiment
  - Dates normalisées

- **gold_full_moon_dates:** Enrichissement des avis avec l'impact de la pleine lune

### Dashboard Streamlit

Le tableau de bord interactif offre les fonctionnalités suivantes:

#### Filtres et paramètres (barre latérale)
- Filtrage par type de chambre/propriété
- Plage de prix (min/max)
- Statut de Superhost
- Proximité avec les dates de pleine lune

#### Sections d'analyse
- **Vue d'ensemble:** Indicateurs clés (nombre d'annonces, hôtes, avis, prix moyen)
- **Analyses géographiques:** Distribution des annonces par type, analyse des prix
- **Performance des hôtes:** Classement des Superhosts, métriques individuelles
- **Analyse du sentiment:** Distribution et tendances des avis positifs/négatifs/neutres
- **Données brutes:** Exploration complète des tables avec filtrage dynamique

#### Mise à jour en temps réel
- Les visualisations se mettent à jour automatiquement lors de la modification des filtres
- Rechargement des données possible sans redémarrage du dashboard

### Contrôle de qualité

Le module `src/data_quality.py` exécute des vérifications automatiques:
- Validation de l'unicité des identifiants (host_id, listing_id)
- Vérification de la complétude des données
- Détection des anomalies dans les distributions
- Contrôle de l'intégrité référentielle

---

## Répartition des tâches


### "Assitan SINEYOKO" <a_sineyoko@stu-mba-esg.com> - Développement des modèles Silver

**Périmètre de responsabilité:**
- Conception et développement des modèles SQL de nettoyage (silver_hosts, silver_listings, silver_reviews, silver_full_moon_dates)
- Validation des règles de nettoyage et normalisation
- Assurance de la qualité des données en sortie de couche Silver
- Documentation des transformations appliquées

**Livrables:**
- Modèles `.sql` dans `airbnb_analytics_platform/models/silver_*.sql`
- Tests unitaires dbt pour valider la qualité Silver
- Documentation des logiques de transformation

**Points de contrôle:**
- Exécution sans erreur: `dbt run --select silver_*`
- Zéro doublons après déduplication
- Absence de valeurs NULL critiques

---

### "Nassima DHAIMAN" <n_dhaiman@stu-mba-esg.com> - Développement des modèles Gold et Dashboard

**Périmètre de responsabilité:**

**Modèles Gold:**
- Conception et développement des modèles d'analyse (gold_hosts, gold_listings, gold_reviews, gold_full_moon_dates)
- Agrégation et enrichissement des données pour l'analyse
- Création des métriques de business
- Optimisation des requêtes pour la performance

**Dashboard Streamlit:**
- Développement du dashboard interactif (`streamlit_app/app.py`)
- Création et maintenance des visualisations (filtres, graphiques, tableaux)
- Validation de la pertinence des informations affichées
- Optimisation de l'expérience utilisateur

**Livrables:**
- Modèles `.sql` dans `airbnb_analytics_platform/models/gold_*.sql`
- Application Streamlit complète et fonctionnelle
- Documentation utilisateur du dashboard
- Tests de validation des métriques Gold

**Points de contrôle:**
- Exécution sans erreur: `dbt run --select gold_*`
- Cohérence des métriques avec les données Silver
- Dashboard responsive et performant
- Filtres fonctionnels et intuitifs

---

### Collaboration et échanges

**Interfaces:**
- Les modèles Silver doivent être validés avant utilisation dans les modèles Gold
- Communication sur les nouvelles colonnes/métriques requises
- Tests conjoints du pipeline complet (Silver → Gold → Dashboard)

**Processus de validation:**
1. Développement et test en local
2. Code review par l'autre membre
3. Intégration et test end-to-end
4. Merge et déploiement

