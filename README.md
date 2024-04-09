# E-commerce Backend System  (ecommerce_backend)

Develop a backend system for an e-commerce platform using Python and Django. The system should support product management, user orders, and an analytics dashboard. 

## Programming Language and Framework
- Python
- Django Rest Framework

## List of Apps in the Project
- `authentication`
- `product_management`
- `order_processing`

## Services
- Google OAuth 2.0

## Databases
- MySQL

## List of APIs

- **Get All Products**: Fetches all products available in the store.
  - Endpoint: `/products/`
  - Method: GET

- **Get Product by ID**: Fetches details of a specific product by its ID.
  - Endpoint: `/products/<int:pk>/`
  - Method: GET

- **Add Product**: Allows adding a new product to the store.
  - Endpoint: `/products/create/`
  - Method: POST

- **Update Product**: Allows updating an existing product in the store.
  - Endpoint: `/products/update/<int:pk>/`
  - Method: PUT

- **Delete Product**: Deletes a product from the store based on its ID.
  - Endpoint: `/products/delete/<int:pk>/`
  - Method: DELETE


- **Add Product to Cart**: Adds a product to the user's shopping cart.
  - Endpoint: `/cart/add/`
  - Method: POST

- **Update Cart Product**: Updates the quantity of a product in the user's shopping cart.
  - Endpoint: `/cart/update/<int:pk>/`
  - Method: PUT

- **Get All Cart Products**: Fetches all products in the user's shopping cart.
  - Endpoint: `/cart/view/`
  - Method: GET

- **Delete Cart Product**: Removes a product from the user's shopping cart.
  - Endpoint: `/cart/delete/<int:pk>/`
  - Method: DELETE

- **Place Order**: Allows users to place an order for the items in their shopping cart.
  - Endpoint: `/order/`
  - Method: POST


## Dependencies

- `Django`
- `sqlparse`
- `django-filter`
- `djangorestframework`
- `django-cors-headers`
- `PyMySQL`
- `requests`
- `django-countries`
- `PyJWT`
- `requests`

## Running the Project Locally

To run the ecommerce_backend project locally, follow these steps:

### Prerequisites

- Install Python (3.7 or higher): https://www.python.org/downloads/

### Setting up the Environment

1. Clone this repository to your local machine:

   
   git clone https://github.com/arpita-tudip/E-Commerce-Backend.git
   

2. Navigate to the project directory:

   
   cd ecommerce_backend
   

3. Create a virtual environment (optional but recommended):

   
   python -m venv myenv
   

4. Activate the virtual environment:

   - On Windows:

     
     myenv\Scripts\activate
     

   - On macOS and Linux:

     
     source myenv/bin/activate
     

### Installing Dependencies

1. Install required Python packages using pip:

   
   pip install -r requirements.txt
   

### Database Configuration

1. Configure the database settings in the `ecommerce_backend/settings.py` file. You'll need to set up your MySQL connection details.

### Running Migrations

1. Run the database migrations to create the necessary database schema:
    
   python3 manage.py makemigrations
   

   
   python3 manage.py migrate
   

### Running the Development Server

1. Start the Django development server:

   
   python3 manage.py runserver
   

2. Your ecommerce_backend should now be running locally at `http://127.0.0.1:8000/`.


