# Safe Pedestrian Routing System

This project is a prototype pedestrian routing system designed to prioritise safety alongside walkability. Traditional navigation applications often focus solely on shortest or fastest paths, neglecting important safety-related factors such as lighting, local crime levels, and pedestrian infrastructure. This system combines spatial crime data with OpenStreetMap (OSM) features to suggest safer walking routes in urban areas.

## Project Overview

The system works by:

- Extracting and processing pedestrian infrastructure from OSM.
- Scoring each street segment using weighted features such as lighting, CCTV coverage, road types, and proximity to amenities.
- Calculating localised crime risk using Inverse Distance Weighting (IDW) based on recent crime reports.
- Merging infrastructure and crime risk into a single safety score.
- Generating both shortest and safest routes between origin-destination node pairs using `networkx`.

## Project Structure

| File / Notebook          | Description |
|--------------------------|-------------|
| `osm2.ipynb`             | Preprocesses OSM data, filters for pedestrian routes, and extracts features like lighting and road type. |
| `crime_data.py`          | Functions to download, clean, and weight crime data using the Police.uk API. |
| `Crime-routing.ipynb`    | Computes IDW crime scores for each network edge. |
| `merge-routing.ipynb`    | Merges crime and pedestrian data, generates routes, and performs analysis and evaluation. |
| `output/`                | (Optional) Contains saved figures, maps, and evaluation plots. |

## Features

- **Pedestrian Safety Weighting**: Scores edges based on OSM attributes such as `lit=yes`, `highway=footway`, `maxspeed`, etc.
- **Crime Risk Integration**: Incorporates crime risk using IDW based on proximity to recent incidents.
- **Customisable Scoring**: Feature weights are defined in code and can be modified.
- **Routing Engine**: Uses Dijkstra’s algorithm with custom weights to produce safest and shortest routes.
- **Evaluation Tools**: Includes functions to generate and analyse routes across multiple node pairs.

