Project Overview:-

This project is a Django-based web application that supports:
    1-Importing and processing CSV files with platform-specific data.
    2-APIs to fetch and manipulate data for dashboards (line charts, bar charts, data tables, and summary metrics).
    3-Exporting filtered data as a CSV file.

Features:-

    1-CSV Import: Supports importing and processing CSV files with platform-specific fields (e.g., Amazon, Meesho, Flipkart).
    2-Data Handling:
        *Filters sales data based on date range, platform, and other parameters.
        *Generates summary metrics like total revenue, orders, and products sold.
    3-CSV Export: Enables exporting filtered data as a CSV file.
    4-API for Dashboard Components:
        *Line chart: Monthly sales volume.
        *Bar chart: Monthly revenue.
        *Filterable data table with support for multiple filters.
        *Summary Metrics

Tech Stack:-
    *Backend: Python, Django, Django REST Framework
    *Database: MySQL
    *Frontend: React 

Setup Instructions:-

    *Prerequisites
        1-Python 3.9+ (for Backend)
        2-MySQL (for Database)
        3-Node.js and npm (for frontend)

Backend Setup:-

    #Clone the repository from command "git clone https://github.com/sh-maker/ecommerce-sales-data.git"
    #Change the directory to your project from command "cd backend\ecommerce_data"
    #Install the dependencies from command "pip install -r requirements.txt"
    #Run Database Migrations:
        *python manage.py makemigrations
        *python manage.py migrate
    #Run the Development Server from command "python manage.py runserver"

Frontend Setup:-
    #Navigate to the Frontend Directory from command "cd frontend\sales-dashboard"
    #Install Dependencies from command "npm install"
    #Start the React App from command "npm start"

CSV Import/Export Usage
    *CSV Import: Use the provided API endpoint CSV files.
    *CSV Export: Use the export button to download filtered data.

API Endpoints:-
    #Dashboard APIs:-
        #Use: Fetch monthly sales volume
        #Endpoint: "/api/sales/line-chart/"	
        #Method: GET	
        
        #Use: Fetch monthly revenue
        #Endpoint: "/api/sales/bar-chart/"	
        #Method: GET

        #Use: Retrieve sales data with filters
        #Endpoint: "/api/sales/filterable-data/"	
        #Method: GET

        #Use: Retrieve Summary Metrics
        #Endpoint: "/api/sales/summary-metrics/"	
        #Method: GET
        
    #CSV API
        #Use: Upload and process a CSV file
        #Endpoint: "/api/sales/import-csv/"	
        #Method: POST

Folder Structure:-

├── backend/ecommerce-data
│   ├── manage.py
│   ├── app/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   ├── urls.py
│   ├── settings.py
├── frontend/sales-dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   ├── package.json
├── requirements.txt
├── README.md