# Django API Project

## Setup Instructions

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/KillianFvt/mspr_covid_ekym.git
    cd mspr_covid_ekym
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

1. Apply migrations:
    ```bash
    python manage.py migrate
    ```

2. Start the development server:
    ```bash
    python manage.py runserver
    ```

3. Open your browser and navigate to `http://127.0.0.1:8000/` to see the API in action.

## API Documentation

[http://127.0.0.1:8000/openapi](http://127.0.0.1:8000/openapi)