# Philosophers Cleaners — Backend

![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![Python](https://img.shields.io/badge/Python-3.9-blue)
![Pydantic](https://img.shields.io/badge/Pydantic-Stable-lightgrey)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-blueviolet)
![REST API](https://img.shields.io/badge/RESTAPI-Implemented-orange)
![Auth](https://img.shields.io/badge/Auth-JWT-red)
![Email](https://img.shields.io/badge/Notifications-Enabled-blue)
![QR](https://img.shields.io/badge/QR-Scan%20Enabled-black)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)

A modern, scalable backend for **Philosophers Cleaners** — a premium dry cleaning and laundry booking platform.

Built with **:contentReference[oaicite:0]{index=0}**, **async SQLAlchemy 2.0**, and **:contentReference[oaicite:1]{index=1}** to deliver high-performance REST APIs for booking management, customer handling, operational workflows, and QR-based order tracking.

---

## 📌 Overview

This backend service powers the core operations of Philosophers Cleaners, including:

- 🧼 Pickup scheduling
- 👤 Customer data management
- 🛎 Service request handling
- 🛠 Admin management
- 📧 Email notifications
- 🔐 Secure authentication
- 📱 QR code-based order scanning

Designed with scalability, clean architecture, and production-readiness in mind.

---

## ✨ Features

### 🧼 Pickup Scheduling

- Customers can book laundry & dry cleaning pickups
- Select preferred date and time
- Automatic booking status initialization

### 👤 Customer Management

- Secure profile creation
- Booking history tracking
- Encrypted password storage (BCrypt)

### 🛎 Service Requests

- Laundry
- Dry Cleaning
- Ironing
- Specialty garment services

### 🔐 Authentication & Security

- JWT-based authentication
- Protected API routes
- Role-ready architecture
- Secure password hashing

---

## 📧 Email Notification Flow

When a booking is created:

1. ✅ Customer receives a booking confirmation email
2. 📩 Admin receives a new pickup request notification
3. 📦 Booking status is initialized as `Pending Pickup`

---

## 📱 QR Code Scan System

Each order is automatically assigned a **unique QR code**.

### 🔄 How It Works

- A QR code is generated when a booking is created.
- The QR is linked to the unique `order_id`.
- Staff can scan the QR code during:
  - Pickup
  - Processing
  - Quality check
  - Delivery
- Scanning updates order status in real-time.

### 🎯 Benefits

- Faster order lookup
- Reduced manual errors
- Real-time status updates
- Improved operational efficiency
- Seamless order tracking

### ⚙ Example QR Flow

1. Booking Created → QR Generated
2. Staff Scans QR at Pickup → Status: `Picked Up`
3. Scan at Facility → Status: `Processing`
4. Scan at Delivery → Status: `Delivered`

QR implementation can be extended to integrate with mobile scanning apps or internal admin dashboards.

---

## 🏗 Architecture

- Async-first design (SQLAlchemy 2.0 + asyncpg)
- RESTful API structure
- Modular service-based architecture
- Automatic OpenAPI documentation
- Cloud-ready deployment design
- Scalable QR token mapping system

---
