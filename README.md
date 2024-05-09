# Vendor Management System

Setup Instructions:
1. Fork the repository in your account.
2. Open the terminal or git bash and change the directory where you want to clone the directory.
3. Clone the repository. (git clone https://github.com/ruthkapse004/Vendor-Management-System.git)
4. Create a virtual environment. (python -m venv ENV)
5. Activate virtual environment. (ENV\Scripts\activate)
6. Install libraries using the requirements.txt file. (pip install -r requirements.txt)
7. Create db.sqlite3 file. Run the migrations. (python manage.py migrate)
8. Run the Django development server. (python manage.py runserver)
9. Visit the URL that appears in the terminal. (http://127.0.0.1:8000/)
10. Create an admin user from the terminal. (python manage.py createsuperuser.)


Endpoints:
- /api/login/
- /api/vendors/
- /api/vendors/vendor_code/
- /api/vendors/vendor_code/performance/
- /api/purchase_orders/
- /api/purchase_orders/po_number/
- /api/purchase_orders/po_number/acknowledge/

Note - Install the ModHeader extension (Google Chrome) to send a token in the header of an API request. 

Using API endpoints:
1. /api/login/ -
   - POST request: Include username & password inside the body to receive the token.
   - Use this token in ModHeader to authenticate the API request.

2. /api/vendors/ -
   - GET request: List all Vendors.
   - POST request: Create a new Vendor. Include Name, Contact details & Address in the body.

3. /api/vendors/vendor_code/ -
   - GET request: Retrieve Vendor details.
   - PUT request: Update Vendor details.
   - DELETE request: Delete Vendor.

4. /api/vendors/vendor_code/performance/ -
   - GET request: List Vendor's performance metrics.
  
5. /api/purchase_orders/ -
   - GET request: List all Purchase Orders.
   - POST request: Create a new Purchase Order. Include Vendor, Expected Delivery date, Items & Quantity.

6. /api/purchase_orders/po_number/ -
   - GET request: Retrieve Purchase Order details.
   - PUT request: To change the PO status to Issued, Canceled, or Delivered & other details.
   - DELETE request: Delete Purchase Order.
  
6. /api/purchase_orders/po_number/acknowledge/ -
   - POST request: Send empty body to acknowledge the Purchase Order.
  
Running the Tests: 
- To run all tests. (pytest vendor_management/tests)
- To run specific tests. (pytest file_path::test_class_name::test_function_name)