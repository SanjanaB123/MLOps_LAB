# Terraform Beginner Lab (GCP)

## Overview
This lab covers the fundamentals of Terraform by creating, modifying, and destroying GCP infrastructure resources using Infrastructure as Code (IaC).

---

## Environment
- **OS:** macOS (Apple Silicon - darwin_arm64)
- **Terraform Version:** v1.14.8
- **GCP Project:** sanjana-terraform-lab
- **Region:** us-central1
- **Zone:** us-central1-a

---

## Prerequisites Completed
- GCP account with billing enabled (Billing Account for Education)
- Google Cloud CLI installed via Homebrew
- Terraform installed via Homebrew
- Service account created with Editor role
- Compute Engine API enabled on GCP project

---

## Part 1: Setup & Initialization

Installed the Google Cloud SDK and Terraform:
```bash
brew install --cask google-cloud-sdk
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

Authenticated with GCP and configured the project:
```bash
gcloud auth login
gcloud config set project sanjana-terraform-lab
gcloud services enable compute.googleapis.com
```

Set up credentials using a service account JSON key:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/sanjana/Downloads/sanjana-terafform-lab.json"
```

Created the working directory and `main.tf` configuration file:
```bash
mkdir terraform-lab-gcp
cd terraform-lab-gcp
```

Initialized Terraform (downloaded Google provider v7.25.0):
```bash
terraform init
```

---

## Part 2: Creating Infrastructure

**`main.tf` configuration:**
```hcl
provider "google" {
    project = "sanjana-terraform-lab"
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_compute_instance" "vm_instance" {
    name         = "terraform-vm"
    machine_type = "e2-micro"
    zone         = "us-central1-a"

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
        }
    }

    network_interface {
        network = "default"
    }
}
```

Previewed and applied the infrastructure:
```bash
terraform plan
terraform apply
```

**Result:** `1 added, 0 changed, 0 destroyed` — VM created successfully in 29 seconds.

---

## Part 3: Modifying Resources

Added labels and increased boot disk size in `main.tf`:
```hcl
resource "google_compute_instance" "vm_instance" {
    name         = "terraform-vm"
    machine_type = "e2-micro"
    zone         = "us-central1-a"

    labels = {
        environment = "development"
        owner       = "team-terraform"
    }

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
            size  = 12
        }
    }

    network_interface {
        network = "default"
    }
}
```

Applied the changes:
```bash
terraform apply
```

**Result:** `0 added, 1 changed, 0 destroyed` — VM modified in place after 23 seconds.

---

## Part 4: Adding a Cloud Storage Bucket

Added a new storage bucket resource to `main.tf`:
```hcl
resource "google_storage_bucket" "terraform-lab-bucket" {
    name          = "sanjana-terraform-lab-bucket-2025"
    location      = "us-central1"
    force_destroy = true
}
```

Applied the changes:
```bash
terraform apply
```

**Result:** `1 added, 0 changed, 0 destroyed` — Bucket created in 1 second.

---

## Part 5: Destroying Resources

Destroyed all Terraform-managed infrastructure:
```bash
terraform destroy
```

**Result:** `2 destroyed` — VM destroyed after 1m53s, bucket destroyed after 1s.

---

## Key Concepts Learned
- **`terraform init`** — Initializes the working directory and downloads providers
- **`terraform plan`** — Previews changes without applying them
- **`terraform apply`** — Creates or modifies infrastructure
- **`terraform destroy`** — Tears down all managed resources
- **State file (`terraform.tfstate`)** — Tracks the current state of all managed resources
- **Provider** — The GCP plugin that lets Terraform interact with Google Cloud

---

## Challenges Encountered & Solutions
| Challenge | Solution |
|---|---|
| `gcloud: command not found` | Re-sourced the SDK path with `source "$(brew --prefix)/share/google-cloud-sdk/path.zsh.inc"` |
| Billing not linked to project | Linked billing account via GCP Console > Billing > My Projects |
| Service account key creation blocked by org policy | Created a new project outside the organization |
| Wrong project ID in `main.tf` | Found correct ID via `gcloud projects list` and updated the config |
| Compute Engine API not enabled | Ran `gcloud services enable compute.googleapis.com` |