efile-app/
├── app/
|   |
│   ├── core/
│   │   └── config.py
│   ├── models/					# Defines the MySQL tables
│   │   └── admin.py
│   ├── schemas/                # Defines request and response validation
│   │   └── admin.py
│   ├── routes/                 # Handles HTTP requests
│   │   └── admin_router.py
│   ├── services/               # Queries the database
│   │   └── admin.py
│   ├── db/                     # Creates the database connection and session
│       └── database.py           
├── main.py                     # Initializes FastAPI and registers routers 
├── .env         
├── pyproject.toml
└── README.md