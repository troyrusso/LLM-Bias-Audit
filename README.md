# Intersectional Bias in LLM Narrative Generation

This repository contains the code and data for an audit study of the **Meta-Llama-3-8B-Instruct** model. The project investigates how authorial personas and implicit demographic signals influence narrative outcomes and procedural hesitation in moral scenarios.

## 1. Project Overview
* **Model:** Meta-Llama-3-8B-Instruct.Q4_0.gguf
* **Sample Size:** N = 2,160 independent trials.
* **Architecture:** Two-stage "LLM-as-a-Judge" pipeline.
* **Core Variables:** Demographic Signal (Name), Authorial Persona, Scenario, Hesitation Score, and Narrative Outcome.

## 2. Environment Setup
This project requires Python. Follow these steps to set up the isolated virtual environment:

    # Create the environment
    python -m venv venv

    # Activate the environment
    .\venv\Scripts\activate

    # Install required libraries
    pip install pandas scipy seaborn matplotlib gpt4all

**Note:** If script execution is disabled on your system, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` before activating.

## 3. Hardware Requirements
* **Model Format:** GGUF (Quantized)
* **Backend:** Local GPU acceleration is recommended for Stage 1 (Generation).
* **Storage:** Approximately 5GB for the model weights.

## 4. Repository Structure
* `/Code`: Contains the generation and analysis scripts.
    * `advancedanalysis.py`: Secondary statistical tests (Standard Library version).
    * `generatedistributiongraph.py`: Visualization suite for publication-quality plots.
    * `pairwisetest.py`: Isolated Chi-Square tests for intersectional bias.
    * `experiment_local.py`: Main execution script for local data generation.
* `/Writing`: Contains early drafts, project plans, and preliminary markdown notes.
* `/` (Root Directory): 
    * Contains the primary experimental data (e.g., `local_experiment_results.csv`).
    * Contains all generated visualization outputs (`fig1_demographic_hesitation.png`, `trend4_vulnerability_heatmap.png`, etc.).

## 5. Reproducing Results
To replicate the statistical analysis and generate the report figures:

1. Ensure your virtual environment is active.
2. Run the analysis script to verify results:
   
       python Code/advancedanalysis.py

3. Generate the visualization suite:
   
       python Code/generatedistributiongraph.py

*(Note: Ensure your working directory is set to the repository root before running the scripts so the CSV paths and image outputs land in the correct location).*

## 6. Data Schema
The output CSV (`local_experiment_results.csv`) utilizes the following columns:
* `Persona`: The system instruction used (Default, Noir, Utopian).
* `Demographic_Group`: The intersectional identity (e.g., Black_Male).
* `Scenario`: The moral dilemma (Wallet, Team, Car_Accident).
* `Hesitation`: The 1–5 score extracted in Stage 2.
* `Outcome`: The raw string outcome and binary classification.

## 7. Sample Data:

