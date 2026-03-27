provider "google" {
    project = "sanjana-terraform-lab"
    region  = "us-central1"
    zone    = "us-central1-a"
}

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
resource "google_storage_bucket" "terraform-lab-bucket" {
    name          = "sanjana-terraform-lab-bucket-2025"
    location      = "us-central1"
    force_destroy = true
}