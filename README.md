# GeoPulse — Hyper-Local Retail Mobility Analytics

> **Project:** GeoPulse (Project 2)  
> **Domain:** Retail Strategy & Geospatial Analytics  
> **Project type:** Individual project  
> **Organization:** Infotact Solutions  
> **Status:** Planning / Development

GeoPulse is a geospatial analytics project designed to help retailers understand how people move through a city and make better decisions about where to open new stores. It uses anonymized mobile GPS pings to analyze footfall patterns, identify high-traffic areas, understand hourly movement, and estimate potential customer overlap between store locations.

The project is based on the GeoPulse brief in *INFOTACT SOLUTIONS PROJECT DOCUMENT – ADVANCED DATA ANALYTICS (VOL. II)*.

---

## 1. Business Problem

Retailers may rely on static census information when choosing new store locations. This can miss how foot traffic changes by location and time of day. A new outlet may also be placed too close to an existing store and draw away customers who would otherwise visit that existing location.

GeoPulse aims to provide dynamic, location-based evidence to support retail site-selection decisions.

## 2. Project Objectives

- Generate a synthetic dataset of anonymized mobile GPS pings.
- Store geographic coordinates and timestamps in a geospatial data warehouse.
- Identify GPS pings that fall within store catchment areas.
- Aggregate unique visitors by store and hour.
- Analyze devices that visit multiple store locations to estimate customer overlap and possible cannibalization.
- Visualize footfall and movement patterns on an interactive map.
- Prepare the pipeline for scheduled daily updates.

## 3. Proposed Technology Stack

| Technology | Planned use |
|---|---|
| Python | Generate synthetic GPS ping data |
| Snowflake | Store raw GPS pings and use native `GEOGRAPHY` data types |
| PySpark | Distributed processing of large GPS datasets |
| Apache Sedona | Spatial operations such as point-in-polygon and spatial joins |
| SQL | Analyze store visits, hourly footfall, and customer overlap |
| dbt | Clean, model, and aggregate data in Snowflake |
| Kepler.gl | Geospatial visualization, including heatmaps and H3 hexagons |
| React | Optional frontend for embedding the map |
| Apache Airflow | Orchestrate scheduled PySpark and dbt workflows |
| H3 | Represent geographic areas as hexagonal cells |

**Implementation note:** The project brief proposes this full stack. The actual implementation will be built incrementally. Tools that require separate infrastructure or accounts may be introduced only when they are practical for the individual project.

## 4. High-Level Data Pipeline

```text
Synthetic GPS Ping Generator (Python)
                 |
                 v
       Raw GPS Ping Dataset
                 |
                 v
     Snowflake Raw Data Tables
       (GEOGRAPHY coordinates)
                 |
                 v
   PySpark + Apache Sedona
     (spatial processing)
                 |
                 v
       Spatially Enriched Data
                 |
                 v
          dbt Models
   (cleaning and aggregation)
                 |
                 v
       Analytics Tables
                 |
          +------+------+
          |             |
          v             v
   SQL Analysis     Kepler.gl
 (footfall, overlap,  Interactive maps,
  cannibalization)   heatmaps, H3
          |             |
          +------+------+
                 |
                 v
       Retail Site-Selection
          Insights

       Apache Airflow
  (planned workflow orchestration)
```

## 5. Planned Data Design

### GPS ping data

The synthetic mobile ping dataset is expected to contain the following fields, as specified in the project brief:

| Column | Description |
|---|---|
| `DeviceID` | An anonymized identifier for a mobile device |
| `Lat` | Latitude coordinate |
| `Long` | Longitude coordinate |
| `Timestamp` | Date and time when the ping was recorded |

Additional fields may be introduced if they are needed for analysis and are clearly documented.

### Store location data

A store reference dataset will be needed to represent target store locations and their catchment areas. Its exact schema will be finalized during implementation. It may include a store identifier, store name, latitude, longitude, and catchment geometry.

### Important privacy note

The project uses synthetic, anonymized device identifiers and generated location data. It should not use or attempt to identify real individuals or track real people's movements.

## 6. Development Roadmap

The project brief proposes a four-week development plan.

### Week 1 — Data Synthesis and Loading

- Generate a large synthetic dataset of anonymized mobile GPS pings.
- Include `DeviceID`, `Lat`, `Long`, and `Timestamp`.
- Set up Snowflake.
- Create tables using the `GEOGRAPHY` data type and load the raw ping data.

**Expected checkpoint:** A reproducible GPS dataset is available, and raw records can be loaded and queried.

### Week 2 — Spatial Joins and ELT Modeling

- Use PySpark and Apache Sedona for spatial processing.
- Create 500-meter catchment areas around target store locations.
- Intersect GPS pings with store catchment areas.
- Configure dbt with Snowflake.
- Build models that aggregate unique visitors per store per hour.

**Expected checkpoint:** Spatial intersections work, and hourly store-footfall metrics are produced.

### Mid-Project Review

- Demonstrate spatial intersection processing on the generated dataset.
- Check that the processing approach is suitable for larger datasets.
- Confirm that dbt models compile and that morning/evening traffic patterns are represented accurately.

### Week 3 — Cannibalization Analysis and Map UI

- Track unique `DeviceID` values over time.
- Identify devices that visit multiple store locations.
- Calculate customer overlap between stores.
- Integrate Kepler.gl into a React frontend, if feasible.
- Connect the map to the aggregated analytical data.

**Expected checkpoint:** Store overlap metrics and an interactive geospatial view are available.

### Week 4 — Automation and Final Refinement

- Orchestrate PySpark and dbt jobs using Apache Airflow.
- Configure Kepler.gl to render H3 hexagons.
- Add an animation or time slider to explore foot traffic over a 24-hour period.
- Refine the dashboard and document the final workflow.

**Expected checkpoint:** The completed project demonstrates an end-to-end geospatial analytics workflow and communicates useful retail site-selection insights.

## 7. Key Business Metrics

The following metrics are planned for analysis. Their exact definitions will be documented in the analytics stage.

- **Total GPS pings:** Number of generated location records.
- **Unique devices:** Number of distinct anonymized device IDs.
- **Hourly footfall:** Unique devices detected within a store's catchment area per hour.
- **Peak traffic hour:** Hour with the highest observed unique-device count for a store or area.
- **Store visitor overlap:** Number and proportion of devices observed in more than one store catchment area during the defined analysis period.
- **Potential cannibalization:** An estimate based on overlap between existing-store visitors and a proposed store's catchment area. This is an analytical indicator, not proof that a new store would cause lost sales.
- **High-footfall zones:** Geographic areas with comparatively high ping or unique-device density.

## 8. Repository Structure

The repository will evolve as development progresses. A proposed structure is:

```text
GeoPulse/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── src/
│   ├── data_generation/
│   │   └── generate_gps_data.py
│   └── spatial_processing/
│       └── spatial_analysis.py
│
├── sql/
│   └── analysis_queries.sql
│
├── dbt_project/
│   ├── models/
│   └── dbt_project.yml
│
├── dashboard/
│   └── README.md
│
├── airflow/
│   └── dags/
│
├── reports/
│   └── figures/
│
├── .gitignore
├── requirements.txt
└── README.md
```

This is a proposed structure, not a claim that all folders or files have already been implemented. It can be simplified or adjusted based on the final tools used.

## 9. GitHub Commit Plan

The goal is to make **at least 20 meaningful commits** across the project. Commits should represent real, reviewable changes—not empty commits or artificial changes made only to increase the count.

Suggested sequence:

| # | Suggested commit message | Work represented |
|---:|---|---|
| 01 | `docs: add GeoPulse project overview` | Add initial README and project objectives |
| 02 | `chore: initialize project structure` | Create folders and starter files |
| 03 | `chore: add gitignore and dependencies` | Add `.gitignore` and initial requirements |
| 04 | `feat: create synthetic GPS data generator` | Generate sample device pings |
| 05 | `feat: add configurable city movement simulation` | Make generated movement configurable |
| 06 | `test: validate generated GPS records` | Check required columns, ranges, and timestamps |
| 07 | `feat: add store location dataset` | Create sample store reference data |
| 08 | `docs: document dataset schema and assumptions` | Explain fields, coordinate assumptions, and limitations |
| 09 | `feat: add Snowflake raw table setup` | Add SQL for raw table creation |
| 10 | `feat: load GPS records into Snowflake` | Implement and document the loading workflow |
| 11 | `feat: add Snowflake geography conversion` | Convert coordinates into geographic values |
| 12 | `feat: configure spatial processing with Sedona` | Set up the spatial-processing environment |
| 13 | `feat: create store catchment areas` | Build 500-meter store catchment areas |
| 14 | `feat: implement GPS point spatial joins` | Match pings to store catchments |
| 15 | `feat: add dbt project configuration` | Configure dbt for Snowflake |
| 16 | `feat: add hourly store footfall model` | Aggregate unique visitors by store and hour |
| 17 | `feat: analyze visitor overlap across stores` | Identify devices appearing in multiple store areas |
| 18 | `feat: calculate store cannibalization indicators` | Add documented overlap-based indicators |
| 19 | `feat: prepare Kepler map dataset` | Export data in a format suitable for mapping |
| 20 | `feat: build interactive footfall visualization` | Add map layers and time-based exploration |
| 21 | `feat: add H3 hexagon aggregation` | Prepare hexagonal geographic summaries |
| 22 | `feat: orchestrate analytics workflow` | Add Airflow DAGs if Airflow is implemented |
| 23 | `test: validate end-to-end data pipeline` | Test the implemented pipeline and outputs |
| 24 | `docs: add project results and setup guide` | Document execution steps, findings, and limitations |

Some steps may be combined or split depending on the actual implementation. Only create a commit after the corresponding work has been completed and checked. If a technology is not used, do not create a commit claiming that it was implemented.

## 10. Setup and Execution

Setup instructions will be added after the repository structure, Python environment, and selected infrastructure are finalized.

The intended setup documentation will cover:

1. Required software and account access.
2. Python environment creation.
3. Dependency installation.
4. Synthetic data generation.
5. Snowflake configuration and data loading.
6. Spatial processing and dbt execution.
7. Analytical queries and dashboard launch.

Do not commit passwords, access tokens, private keys, account credentials, or local environment files. Use environment variables or an untracked `.env` file for secrets.

## 11. Assumptions and Limitations

- GPS pings are synthetic and do not represent actual individuals.
- A device ping inside a catchment area is an approximation of presence, not confirmation of a purchase or store visit.
- Device overlap is an indicator of shared movement patterns; it does not independently prove sales cannibalization.
- Results depend on the simulated movement patterns, catchment-area definitions, time window, and data quality.
- The project brief proposes processing millions of points. Dataset size and performance claims will be reported only after they have been measured.
- Cloud services and advanced tools may require accounts, configuration, credits, or local resources. Their use will be documented accurately.

## 12. Expected Outcome

The intended outcome is a geospatial analytics solution that turns anonymized location pings into actionable retail insights. It should help a retail decision-maker explore footfall by location and time, compare store catchments, identify visitor overlap, and assess candidate store locations with evidence rather than static assumptions.

---

## Project Progress

This section will be updated as milestones are completed.

- [ ] Project repository initialized
- [ ] Synthetic GPS dataset generated and validated
- [ ] Store reference dataset prepared
- [ ] Snowflake raw data tables created
- [ ] Geographic data loaded and validated
- [ ] Spatial catchment areas created
- [ ] GPS-to-store spatial joins completed
- [ ] dbt hourly footfall model completed
- [ ] Store visitor overlap analysis completed
- [ ] Cannibalization indicators documented
- [ ] Kepler.gl visualization completed
- [ ] H3 hexagon visualization completed
- [ ] Airflow orchestration completed, if used
- [ ] End-to-end testing and final documentation completed

**Current status:** Project planning. Progress checkboxes should be updated only after each item is actually completed.
