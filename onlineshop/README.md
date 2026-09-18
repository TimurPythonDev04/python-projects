# Online Shop

A simple e-commerce web application built with Django. Users can browse a product catalog, search and filter by category, add items to a session-based cart, check out as a guest or as a registered user, and view their order history.

## Tech stack

- Python 3
- Django 5.2
- SQLite (default database)
- Pillow (for product image uploads)

## Features

- **Product catalog** — browse all products, filter by category, search by title/description
- **Shopping cart** — add items to a cart stored in the session, view and clear the cart
- **Checkout** — place an order with name, email, and shipping address
- **User accounts** — register, log in, log out
- **Order history** — logged-in users can view their own past orders and order details (orders are scoped to the logged-in user)
- **Admin panel** — manage products, categories, and orders via Django admin

## Getting started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository and go to the project directory:

   ```bash
   git clone https://github.com/TimurPythonDev04/python-projects.git
   cd python-projects/onlineshop
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. (Optional) Create an admin user:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open the site at `http://127.0.0.1:8000/`. The admin panel is available at `http://127.0.0.1:8000/admin/`.

## Running tests

```bash
python manage.py test store
```
