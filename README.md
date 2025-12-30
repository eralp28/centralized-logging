# Centralized Logging System (VM → Cloud Storage)

## Project Overview
This project implements a **centralized logging system** where application logs generated on a virtual machine are collected by a **custom log agent** and sent to a **central cloud storage bucket**.

The system is designed to be:
- **Cloud-native** (AWS EC2 → Amazon S3)
- **Secure** (IAM Role, no hard-coded credentials)
- **Portable** (local demo using Docker + MinIO)
- **Reproducible** (professor can run it locally)

---

## Architecture

### Cloud Mode (Public Cloud)
Application (EC2 Ubuntu VM)
↓
Custom Python Log Shipper (Agent)
↓
Amazon S3 (Central Log Storage)

- The log shipper runs as a **systemd service** on the VM
- Authentication is handled via **IAM Role**
- Logs are batched, compressed, and uploaded to S3

### Local Mode 
Application (Docker)
↓
Custom Python Log Shipper
↓
MinIO (S3-compatible local storage)

This mode allows the project to be tested **without any AWS account**.

---

## Features
- Custom Python log agent (no managed logging service)
- Structured JSON logs
- Batching and gzip compression
- Secure IAM-based authentication
- Partitioned storage layout in S3
- Local demo using Docker + MinIO
- Production deployment using systemd

---

## Local Demo (No Cloud Required)

### Requirements
- Docker
- Docker Compose

### Run
```bash
cp .env.example .env
docker compose up --build

Verify

Open MinIO Console:
http://localhost:9001

Username: minioadmin
Password: minioadmin

Open bucket central-logs

Log files appear under:
logs/

Cloud Deployment (AWS)
Environment

AWS EC2 (Ubuntu Server)

Amazon S3

IAM Role (no access keys)

Log Agent

The log shipper runs as a background service:
sudo systemctl status logshipper
Status:
Active: active (running)


Storage Layout

Logs are stored in Amazon S3 using a partitioned structure:
s3://central-app-logs-eralp/
└── logs/
    └── year=YYYY/
        └── month=MM/
            └── day=DD/
                └── *.json.gz


Security Considerations

No AWS credentials stored on the VM

Authentication via IAM Role

Least-privilege permissions (S3 write-only access)

Encrypted storage (S3 default encryption)


