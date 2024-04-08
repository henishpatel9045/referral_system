# Referral System

## Description

This is a referral system API that allows users to refer other users to a platform and earn rewards for doing so. The system is built using Django and Django Rest Framework.

## Usage

### Installation

1. Clone the repository

```bash
git clone https://github.com/henishpatel9045/referral_system.git
```

2. Create .env file

```bash
cp .env.example .env
```

2. Run Via Docker

```bash
docker-compose up --build -d
```

3. Create Superuser

```bash
docker exec -it referral_system-web-1 sh -c "python manage.py createsuperuser"
```

4. Access the API

The API will be available at `http://localhost:8000/`
The admin panel will be available at `http://localhost:8000/admin/`
The swagger documentation will be available at `http://localhost:8000/doc/`
