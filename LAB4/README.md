# LAB4: Data Version Control (DVC) with Google Cloud Storage

This lab demonstrates how to use DVC (Data Version Control) for data versioning in a machine learning project, with Google Cloud Storage as the remote backend.

## Overview
- **DVC** is used to track and version large datasets, enabling reproducibility and collaboration.
- **Google Cloud Storage (GCS)** is configured as the remote storage for versioned data.
- **Service account credentials** are securely managed for GCS access.

## Steps Performed

### 1. Google Cloud Storage Setup
- Created a GCS bucket in the `us-east1` region for remote data storage.
- Generated a service account with Owner permissions and downloaded the credentials as `gcp-key.json`.

### 2. DVC Installation
- Installed DVC with Google Cloud support using:
  ```bash
  pip install dvc[gs]
  ```
- Added DVC and related dependencies to `requirements.txt`.

### 3. DVC Initialization
- Initialized DVC in the project:
  ```bash
  dvc init
  ```
- This created the `.dvc/` directory and configuration files.

### 4. DVC Remote Configuration
- Added a GCS bucket as the default DVC remote:
  ```bash
  dvc remote add -d sanjbucket gs://sanjana-lab4
  dvc remote modify sanjbucket credentialpath ../gcp-key.json
  ```
- The `.dvc/config` file contains the remote configuration and credential path.

### 5. Data Tracking with DVC
- Placed the dataset (`dvc_test.csv`) in the `data/` folder.
- Started tracking the dataset with DVC:
  ```bash
  dvc add data/dvc_test.csv
  ```
- This generated `data/dvc_test.csv.dvc` for version tracking.

### 6. Git Integration
- Added DVC files and `.gitignore` to version control:
  ```bash
  git add data/dvc_test.csv.dvc data/.gitignore .dvc/config
  git commit -m "Track data with DVC"
  ```
- The `.gitignore` ensures large data files and credentials are not committed.

### 7. Pushing Data to Remote
- Uploaded the tracked data to the GCS remote:
  ```bash
  dvc push
  ```

## How to Update Data
1. Replace or update `data/dvc_test.csv` as needed.
2. Run `dvc add data/dvc_test.csv` to update tracking.
3. Commit changes with Git.
4. Run `dvc push` to upload the new version to GCS.

## How to Revert to Previous Versions
- Use Git to checkout the desired commit:
  ```bash
  git checkout <commit-hash>
  dvc checkout
  ```
- DVC will restore the dataset version associated with that commit.

## Security
- The `gcp-key.json` file is included in `.gitignore` to prevent accidental commits of sensitive credentials.

## Requirements
- Python environment with dependencies from `requirements.txt`.
- DVC with Google Cloud support (`dvc[gs]`).

---
This setup ensures robust, reproducible, and collaborative data management for machine learning workflows using DVC and Google Cloud Storage.
