# 🔒 Security Checks Microservice (Java)

A lightweight microservice for **mocking security scans** and **policy compliance** checks for IT assets.  
Built with love using **Spring Boot**, **Docker**, and **RESTful APIs**. ☕

![Java](https://img.shields.io/badge/Java-17+-orange?style=for-the-badge&logo=java)
![Spring Boot](https://img.shields.io/badge/SpringBoot-3.x-brightgreen?style=for-the-badge&logo=spring)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge&logo=docker)

---

## 📡 API Endpoints

- `GET /security/scan/{assetId}`  
  🔍 **Scan an asset** for mock vulnerabilities (returned in CVE format).

- `GET /security/policy/{assetId}`  
  ✅ **Check encryption policy** compliance for a given asset.

- `POST /security/test`  
  🛠️ **Add a hardcoded test security result** (for development).

---

## 🛠️ Tech Stack

- **Java 17+**
- **Spring Boot 3.x**
- **Docker**
- **REST API**

---

## 🚀 Getting Started

1. Clone the repository
2. Build using Maven:

   ```bash
   mvn clean install
