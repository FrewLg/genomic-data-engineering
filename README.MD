# Genomic Data Engineering Platform

## 📌 Overview
The **Genomic Data Engineering Platform** is a Django-based application designed to manage and streamline genomic research projects. It provides a structured way to track project submissions, approvals, metadata, and associated documentation. The system ensures transparency, accountability, and efficient collaboration between researchers, organizations, and regulatory bodies.

---

## 🚀 Features
- **Project Management**
  - Unique project identifiers
  - Titles, descriptions, and organizational details
  - Duration tracking and IRB codes

- **Submission Workflow**
  - Submission dates, sample submission dates
  - Automatic tracking of created and updated timestamps
  - Attachments and Memorandum of Understanding (MoU) files

- **Approval Process**
  - Approval by designated users
  - Metadata type association
  - Approval confirmation dates

- **User Integration**
  - Submitted by and approved by linked to Django’s `User` model
  - Role-based access control via Django’s authentication system

- **Status Tracking**
  - Project status linked to a dedicated `ProjectStatus` model
  - Metadata type linked to a `MetadataType` model

---

## 🛠 Tech Stack
- **Backend Framework**: Django (Python)
- **Database**: PostgreSQL / MySQL (configurable)
- **Authentication**: Django’s built-in `User` model
- **Admin Interface**: Django Admin for managing projects, statuses, and metadata
- **Version Control**: Git + GitHub

---

## 📂 Project Structure
