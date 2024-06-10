# Blog

This project is a simple blog application built with Django, accessible at [hsup.me](https://hsup.me/). The application is deployed using Docker, which simplifies the setup and management of the environment.

# Environment variables requirements for local installation

1. SendGrid API_KEY
2. Cloudinary API_KEY
3. Database Credentials (We utilized MySQL)

# Local Installation

1. Clone repository

```bash
git clone https://github.com/lsocpb/blog.git
cd your-repository-name
```
2. Run Docker
   
```bash
docker-compose up --build
```
3. The application will be available at http://localhost:8000.

# Testing

1. Run pytest for unit tests.

```bash
pytest
```

