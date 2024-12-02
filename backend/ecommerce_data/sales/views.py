import csv
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from .models import Product, Customer, Order, Delivery
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.db.models import Sum, Count, F
import logging

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@method_decorator(csrf_exempt, name="dispatch")
class ImportCSVView(View):
    def post(self, request):
        try:
            files = request.FILES.getlist('files')  # Get all uploaded files
            if not files:
                logger.error('No files uploaded.')
                return JsonResponse({'error': 'No files uploaded.'}, status=400)

            for csv_file in files:
                # Validate file extension
                if not csv_file.name.endswith('.csv'):
                    logger.error(f'Invalid file format: {csv_file.name}. Please upload a CSV file.')
                    return JsonResponse({'error': f'Invalid file format: {csv_file.name}. Please upload a CSV file.'}, status=400)

                logger.info(f'Processing file: {csv_file.name}')
                # Process each file
                self._process_csv_file(csv_file)

            logger.info('All CSV files processed successfully')
            return JsonResponse({"message": "All CSV files processed successfully"})

        except Exception as e:
            logger.exception('Error processing CSV files.')
            return JsonResponse({'error': str(e)}, status=500)

    def _process_csv_file(self, csv_file):
        """Processes a single CSV file."""
        file_data = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(file_data)

        platform_column = self._detect_platform(csv_reader.fieldnames)
        if not platform_column:
            error_msg = f'Platform column not found in {csv_file.name}'
            logger.error(error_msg)
            raise ValueError(error_msg)

        with transaction.atomic():  # Wrap the entire processing in a transaction
            products = []
            customers = []
            orders = []
            deliveries = []

            for row in csv_reader:
                logger.info(f'Processing row: {row}')
                platform = row[platform_column]

                # Parse dates
                try:
                    date_of_sale = self._parse_date(row['DateOfSale'])
                    delivery_date = self._parse_date(row['DeliveryDate'])
                except ValueError as e:
                    logger.error(f"Error parsing date for row {row['OrderID']}: {str(e)}")
                    raise

                # Create or get product and customer
                product = self._get_or_create_product(row)
                customer = self._get_or_create_customer(row)

                # Prepare order data
                order_data = self._prepare_order_data(row, product, customer, platform, date_of_sale)
                order = self._get_or_create_order(row, order_data)

                # Process delivery details
                street, city, state_pincode = self._split_address(row['DeliveryAddress'])
                delivery = self._prepare_delivery(order, delivery_date, row, street, city, state_pincode)

                # Collect objects for bulk creation later
                products.append(product)
                customers.append(customer)
                orders.append(order)
                deliveries.append(delivery)

            # Perform bulk insertions after processing the file
            Product.objects.bulk_create(products, ignore_conflicts=True)
            Customer.objects.bulk_create(customers, ignore_conflicts=True)
            Order.objects.bulk_create(orders, ignore_conflicts=True)
            Delivery.objects.bulk_create(deliveries, ignore_conflicts=True)

    def _detect_platform(self, headers):
        """Detects the platform column from the CSV headers."""
        for header in headers:
            if header.lower() == 'platform':
                return header
        return None

    def _parse_date(self, date_str):
        """Parses a date string and converts it to 'YYYY-MM-DD' format."""
        try:
            # Try parsing as DD-MM-YY
            return datetime.strptime(date_str, "%d-%m-%y").strftime("%Y-%m-%d")
        except ValueError:
            try:
                # Try parsing as already in YYYY-MM-DD
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format: {date_str}")

    def _get_or_create_product(self, row):
        """Create or get product object."""
        return Product.objects.get_or_create(
            product_id=row['ProductID'],
            defaults={'product_name': row['ProductName'], 'category': row['Category']}
        )[0]

    def _get_or_create_customer(self, row):
        """Create or get customer object."""
        return Customer.objects.get_or_create(
            customer_id=row['CustomerID'],
            defaults={
                'customer_name': row['CustomerName'],
                'contact_email': row['ContactEmail'],
                'phone_number': row['PhoneNumber']
            }
        )[0]

    def _prepare_order_data(self, row, product, customer, platform, date_of_sale):
        """Prepare order data based on platform."""
        order_data = {
            'product': product,
            'customer': customer,
            'platform': platform,
            'quantity_sold': int(row['QuantitySold']),
            'selling_price': float(row['SellingPrice']),
            'date_of_sale': date_of_sale,
        }

        # Handle platform-specific fields
        if platform == 'Amazon':
            order_data['prime_delivery'] = row['PrimeDelivery'] == 'TRUE'
            order_data['warehouse_location'] = row['WarehouseLocation']
        elif platform == 'Meesho':
            order_data['reseller_name'] = row['ResellerName']
            order_data['commission_percentage'] = float(row['CommissionPercentage'])
        elif platform == 'Flipkart':
            order_data['coupon_used'] = row['CouponUsed'] == 'TRUE'
            order_data['return_window'] = int(row['ReturnWindow'])

        return order_data

    def _get_or_create_order(self, row, order_data):
        """Create or get order object."""
        return Order.objects.get_or_create(
            order_id=row['OrderID'],
            defaults=order_data
        )[0]

    def _prepare_delivery(self, order, delivery_date, row, street, city, state_pincode):
        """Prepare delivery data."""
        return Delivery(
            order=order,
            delivery_date=delivery_date,
            delivery_status=row['DeliveryStatus'],
            delivery_address_street=street,
            delivery_address_city=city,
            delivery_address_state=state_pincode,
        )

    def _split_address(self, address):
        """Splits the address into street, city, and state-pincode."""
        try:
            parts = address.split(',')
            street = parts[0].strip()  # First part is the street
            city = parts[1].strip() if len(parts) > 1 else ''  # Second part is the city
            state_pincode = parts[2].strip() if len(parts) > 2 else ''  # Combine state and pincode
            return street, city, state_pincode
        except Exception as e:
            logger.error(f"Error splitting address '{address}': {str(e)}")
            return address, None, None

@method_decorator(csrf_exempt, name="dispatch")
class LineChartView(View):
    """API to fetch monthly sales volume (Quantity Sold)."""

    def get(self, request):
        data = (
            Order.objects.annotate(month=F("date_of_sale__month"), year=F("date_of_sale__year"))
            .values("month", "year")
            .annotate(total_quantity=Sum("quantity_sold"))
            .order_by("year", "month")
        )

        response = [{"month": f"{item['year']}-{item['month']:02}", "quantity_sold": item["total_quantity"]} for item in data]
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class BarChartView(View):
    """API to fetch monthly revenue (Total Sale Value)."""

    def get(self, request):
        data = (
            Order.objects.annotate(month=F("date_of_sale__month"), year=F("date_of_sale__year"))
            .values("month", "year")
            .annotate(total_revenue=Sum(F("quantity_sold") * F("selling_price")))
            .order_by("year", "month")
        )

        response = [{"month": f"{item['year']}-{item['month']:02}", "revenue": item["total_revenue"]} for item in data]
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class FilterableDataTableView(View):
    """API to retrieve sales data with filtering options."""

    def get(self, request):
        filters = {}
        date_range = request.GET.get("date_range", "")
        category = request.GET.get("category", "")
        delivery_status = request.GET.get("delivery_status", "")
        platform = request.GET.get("platform", "")
        state = request.GET.get("state", "")

        # Apply filters
        if date_range:
            try:
                start_date, end_date = date_range.split(",")
                filters["date_of_sale__range"] = [datetime.strptime(start_date, "%Y-%m-%d"), datetime.strptime(end_date, "%Y-%m-%d")]
            except ValueError:
                return JsonResponse({"error": "Invalid date range format. Use YYYY-MM-DD,YYYY-MM-DD."}, status=400)

        if category:
            filters["product__category"] = category
        if delivery_status:
            filters["delivery__delivery_status"] = delivery_status
        if platform:
            filters["platform"] = platform
        if state:
            filters["delivery__delivery_address_state"] = state

        data = Order.objects.filter(**filters).values(
            "order_id",
            "product__product_name",
            "platform",
            "quantity_sold",
            "selling_price",
            "date_of_sale",
            "delivery__delivery_status",
            "delivery__delivery_address_state",
        )

        return JsonResponse(list(data), safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class SummaryMetricsView(View):
    """API to fetch summary metrics."""

    def get(self, request):
        total_revenue = Order.objects.aggregate(total_revenue=Sum(F("quantity_sold") * F("selling_price")))["total_revenue"] or 0
        total_orders = Order.objects.count()
        total_products_sold = Order.objects.aggregate(total_products=Sum("quantity_sold"))["total_products"] or 0
        canceled_orders = Order.objects.filter(delivery__delivery_status="Canceled").count()

        canceled_percentage = (canceled_orders / total_orders * 100) if total_orders > 0 else 0

        response = {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_products_sold": total_products_sold,
            "canceled_order_percentage":canceled_percentage
        }
        return JsonResponse(response)
