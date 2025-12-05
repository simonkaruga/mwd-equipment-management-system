# MWD Equipment Management System

A comprehensive web application for managing Measurement While Drilling (MWD) equipment and tools in oil and gas operations. Built with FastAPI (backend), Jinja2 templates (frontend), and SQLAlchemy for database management.

🚀 **Live Demo**: [MWD Equipment Management System](https://mwd-equipment-management-system-1.onrender.com/)

## Features

- **User Management**: Add, edit, delete users with role-based access (technician, engineer, manager, administrator)
- **Tool Type Management**: Organize equipment into categories (drilling bits, MWD tools, LWD tools, etc.)
- **Tool Inventory**: Track tool locations, status, and serial numbers with search functionality
- **Equipment Checkouts**: Manage tool lending and returns with due date tracking
- **Responsive Design**: Bootstrap-based UI with mobile-friendly interface
- **Database Seeding**: Pre-populated with sample data for demonstration

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy
- **Frontend**: Jinja2 templates, Bootstrap 5
- **Database**: SQLite (development)
- **Language**: Python 3.12+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/mwd-equipment-management.git
cd mwd-equipment-management-system/mwd_fullstack
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app:app --reload
```

5. Open your browser and navigate to `http://localhost:8000`

## Usage

The application includes pre-seeded data for demonstration:
- **Users**: Sample personnel (internationally diverse profiles)
- **Tool Types**: 10 predefined categories of MWD equipment
- **Tools**: Sample tools across different categories with realistic serial numbers and locations

### Navigation
- **Home**: Dashboard showing major tool categories
- **Users**: Staff management interface
- **Tool Types**: Equipment category administration
- **Tools**: Main inventory with search and filter capabilities
- **Checkouts**: Equipment lending system

## API Endpoints

The application provides RESTful API endpoints for integration:

### Users
- `GET /users` - List all users
- `POST /users/add` - Add new user
- `POST /users/edit/{id}` - Update user
- `POST /users/delete/{id}` - Delete user

### Tool Types
- `GET /tool-types` - List tool categories
- `POST /tool-types/add` - Add tool type
- `POST /tool-types/edit/{id}` - Update tool type
- `POST /tool-types/delete/{id}` - Delete tool type

### Tools
- `GET /tools?search=query` - List/filter tools
- `POST /tools/add` - Add tool

### Checkouts
- `GET /checkouts` - Active checkouts
- `GET /checkouts/new` - Checkout form
- `POST /checkouts/checkout` - Process checkout
- `POST /checkouts/return` - Return tool

## Database Schema

- **users**: Personnel information and roles
- **tool_types**: Equipment categories
- **tools**: Individual tool inventory
- **checkouts**: Lending history and status
- **users_tools (junction)**: Many-to-many relationships

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Features in Development

- Equipment maintenance scheduling
- Real-time inventory alerts
- Barcode scanning integration
- Audit trails and reporting
- Multi-location support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bootstrap framework for responsive UI
- FastAPI for high-performance async API
- SQLAlchemy for robust ORM
- FontAwesome for icons
