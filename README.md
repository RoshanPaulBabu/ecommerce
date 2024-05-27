# Django E-Commerce Application

This Django-based E-Commerce application offers a comprehensive platform for managing online stores. Below are the main features and functionalities:

## Features

- **User Authentication**: Allows users to register, login, and manage their accounts. Supports three user roles: customers, sellers, and admins.

- **Customer and Seller Management**: Stores information about customers and sellers, including name, contact details, and email.

- **Product Management**: Enables admin to add, edit, and manage products with details such as name, description, price, quantity, and images.

- **Category and Subcategory Management**: Provides a hierarchical structure for organizing products into categories and subcategories.

- **Cart Management**: Allows customers to add products to their shopping carts and tracks the quantity of each product.

- **Order Management**: Facilitates placing orders, managing shipping addresses, order dates, and order statuses.

- **Purchase Order Management**: Automatically generates purchase orders when a product's quantity falls below the reorder level.

- **Admin Messages**: Sends messages to admins regarding purchase orders, allowing them to confirm orders and update quantities.

- **Email Confirmation and Cancellation**: Sends email notifications to customers confirming their orders and notifying them of order cancellations.

## Admin Panel

- **Seller Admin Panel**: Allows admins to view and manage sellers, including search functionality.

- **Category Admin Panel**: Enables admins to manage product categories and subcategories, displaying counts of subcategories.

- **Customer Admin Panel**: Allows admins to view and manage customer accounts, including search functionality.

- **Product Admin Panel**: Enables admins to manage products, including images and quantities, with low stock alerts.

- **Order Admin Panel**: Allows admins to view and manage customer orders, search by customer name, and view order details.

- **Purchase Order Admin Panel**: Enables admins to manage purchase orders and related items, confirm orders, and update quantities.

## Additional Functionality

- **Email Alerts**: Sends email alerts to admins for low stock levels and new purchase orders.

- **Session Management**: Prevents duplicate alerts for low stock levels using session management.

- **Image Display**: Displays product images as thumbnails in the admin panel.

- **Read-only Fields**: Configures read-only fields for certain admin panels.

## Setup Instructions

To set up this project locally:

```bash
# 1. Clone the repository.
git clone https://github.com/RoshanPaulBabu/ecommerce.git

# 2. Navigate to the project directory.
cd ecom-master

# 3. Install the required dependencies.
pip install -r requirements.txt

# 4. Apply database migrations.
python manage.py migrate

# 5. Create a superuser for accessing the admin panel.
python manage.py createsuperuser

# 6. Start the development server.
python manage.py runserver
```

# Usage

1. Access the admin panel in your browser by navigating to [http://localhost:8000/admin/](http://localhost:8000/admin/).
2. Log in with the superuser credentials created in step 5.
3. Start adding products, categories, and managing orders through the admin panel.

# Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.

# License

This project is licensed under the MIT License.
