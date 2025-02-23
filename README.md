# Drugstoc Store

A Django-based inventory management system with RESTful API endpoints for managing products, orders, and generating reports.

## Features

- **User Authentication**: Register, login, and role-based access control
- **Product Management**: Create, read, update, and delete products
- **Order Management**: Create orders, track order status
- **Reporting**: Low stock reports and sales reports by time period

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework
- SQLite (for development)

## Setup and Installation

### Option 1: Standard Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/preciousimo/drugstoc_store.git
   cd drugstoc_store
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the API**
   - The API will be available at `http://127.0.0.1:8000/api/`
   - Django admin interface: `http://127.0.0.1:8000/admin/`

### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/preciousimo/drugstoc_store.git
   cd drugstoc_store
   ```

2. **Create a Dockerfile**
   Create a file named `Dockerfile` with the following content:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Create a superuser in Docker**
   In a new terminal while the container is running:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Access the API**
   - The API will be available at `http://localhost:8000/api/`
   - Django admin interface: `http://localhost:8000/admin/`

## API Endpoints

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get session
- `POST /api/logout` - Logout and clear session

### Users
- `GET /api/users` - List all users (admin only)
- `GET/PUT/DELETE /api/user/{id}/` - Get, update, or delete user (admin only)

### Products
- `GET /api/products/` - List all products (all authenticated users)
- `POST /api/products/` - Create new product (admin only)
- `GET/PUT/DELETE /api/product/{id}/` - Get, update, or delete product

### Orders
- `GET /api/orders/` - List orders (users see their own, admins see all)
- `POST /api/orders/` - Create new order
- `GET /api/order/{id}/` - Get order details
- `PATCH /api/order/{id}/status/` - Update order status (admin only)

### Reports
- `GET /api/reports/low-stock/` - Get low stock report (admin only)
- `GET /api/reports/sales/` - Get sales report by period (admin only)

## Running Tests

### Without Docker
```bash
python manage.py test
```

### With Docker
```bash
docker-compose exec web python manage.py test
```

## App Preview :

<table width="100%"> 
<tr>
<td width="100%">      
&nbsp; 
<br>
<p align="center">
  Landing Page
</p>
<img width="1428" alt="Screenshot 2025-02-23 at 6 18 20 PM" src="https://github.com/user-attachments/assets/212a6efc-53da-4dfc-b4b5-c9c70187cf47" />
</td> 
</table>
