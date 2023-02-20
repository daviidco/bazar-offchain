# Bazar off-chain 

This project is a microservice flask which manager the business logic off-chain

There are implemented an API Rest.

## Table of content
1. [Overview](https://github.com/bazarnetwork/bazar-offchain/src/master/#Overview)  
2. [Requirements](https://github.com/bazarnetwork/bazar-offchain/src/master/#Requirements)
3. [Download](https://github.com/bazarnetwork/bazar-offchain/src/master/#Download)
4. [Structure](https://github.com/bazarnetwork/bazar-offchain/src/master/#Project_structure)
5. [Configure bazar-offchain](https://github.com/bazarnetwork/bazar-offchain/src/master/#Configure_bazar-offchain)
6. [Run bazar-offchain](https://github.com/bazarnetwork/bazar-offchain/src/master/#Run_bazar-offchain")

## 	📜 Overview

It is an **Api-Rest** being developed with **Python** and framework **Flask-Restful**. **Bazar off-chain** administer information of application users bazar that is out blockchain. The information can be: Basic company information, Documents, Products, transaction history trough data models.

**Api-Rest bazar-offchain** not authenticate users and have no domain over all information of main porject bazar.

**Bazar-offchain** uses external services to authenticate and to store objects like AWS s3. 


## ✅ Requirements

1. PyCharm 2022.1.3 (Community Edition)
2. Python (versio 3.9.13)
3. Poetry (version 1.2.1)

**Main libraries used:**
1. Flask-Migrate - for handling all database migrations.
2. Flask-RESTful - restful API library.
3. Flask-SQLAlchemy - adds support for SQLAlchemy ORM.


## ⬇️ Download
Clone project with ssh key:
```
git clone git@github.com:bazarnetwork/bazar-offchain.git
```
or clone project using http:
```
git clone https://github.com/bazarnetwork/bazar-offchain.git
```

## 📁 Project structure:
```
.
├── alembic.ini
├── application.py
├── poetry.lock
├── pyproject.toml
├── src
│   ├── application
│   │   ├── user
│   │   │   └── user_uc.py
│   ├── domain
│   │   ├── entities
│   │   │   ├── common_entity.py
│   │   │   └── user_interface.py
│   │   └── ports
│   │       └── user_interface.py
│   └── infrastructure
│       ├── adapters
│       │   ├── auth0
│       │   │   └── auth0_service.py
│       │   ├── database
│       │   │   ├── adapter_postgresql.py
│       │   │   ├── alembic
│       │   │   │   ├── README
│       │   │   │   ├── env.py
│       │   │   │   ├── script.py.mako
│       │   │   │   └── versions
│       │   │   ├── models
│       │   │   │   ├── __all_models.py
│       │   │   │   ├── model_base.py
│       │   │   │   └── user.py
│       │   │   └── repositories
│       │   │       └── user_repository.py
│       │   ├── flask
│       │   │   ├── app
│       │   │   │   ├── controllers
│       │   │   │   │   └── user
│       │   │   │   │       ├── blueprints
│       │   │   │   │       │   └── user_blueprint_v1.py
│       │   │   │   │       └── user_resources.py
│       │   │   │   └── utils
│       │   │   │       ├── error_handling.py
│       │   │   │       ├── errors_definition.py
│       │   │   │       ├── logger.py
│       │   │   │       └── ultils.py
│       │   │   ├── configuration_injector.py
│       │   │   ├── entrypoint.py
│       │   │   └── migrations
│       │   │       ├── README
│       │   │       ├── alembic.ini
│       │   │       ├── env.py
│       │   │       ├── script.py.mako
│       │   │       └── versions
│       │   └── storage
│       │       └── s3_service.py
│       └── config
│           ├── default.py
│           ├── default_infra.py
│           ├── development.py
│           ├── local.py
│           ├── production.py
│           ├── staging.py
│           └── testing.py
└── tests
└── .ebxtensions
```

## ⚙️ Configure bazar-offchain
Set environment variables in virtual environment if you want to do testing
```
set -a
source .flaskenv
set +a
```

Install dependencies poetry from poetry.lock
```
poetry install
```
or install dependencies poetry from requirements.txt
```
poetry add $( cat requirements.txt )
```

Configure the database with the commands
```
alembic revision --autogenerate -m "Create models name_model" 
alembic upgrade head  
```


## ▶️ Run API bazar-offchain
Run Api:

```
flask run
```