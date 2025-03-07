# E-Commerce Website for Fashion

A beautiful and easy-to-use e-commerce website for men's, women's, and kids' wear built with Flask, HTML, and CSS.

## Features

- Browse products by category (Men, Women, Kids)
- View product details
- Add products to cart
- Update cart quantities
- Checkout process
- Responsive design for all devices

## Setup Instructions

1. Clone this repository
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

```
E-Commerce Website/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── app/
│   ├── static/             # Static files (CSS, JS, images)
│   │   ├── css/            # CSS stylesheets
│   │   ├── js/             # JavaScript files
│   │   └── images/         # Product and site images
│   ├── templates/          # HTML templates
│   └── models/             # Data models (for future database integration)
└── README.md               # This file
```

## Future Enhancements

- User authentication and profiles
- Product search functionality
- Product filtering and sorting
- Payment gateway integration
- Admin panel for product management
- Database integration (SQLite, PostgreSQL, etc.)

## License

MIT 