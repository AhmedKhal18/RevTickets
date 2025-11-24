# Backend Setup and Seed Data

## Running the Seed Data Script

To populate the database with demo data for development and demos:

```bash
# From the backend directory
cd backend
python src/seed_data.py
```

This will create:
- 6 demo users (3 regular users, 3 agents)
- Categories and subcategories
- Sample tickets
- Tags for organization

## Demo Login Credentials

### Regular Users:
- `john.doe@company.com` / `password123`
- `jane.smith@company.com` / `password123`
- `mike.johnson@company.com` / `password123`

### Agents:
- `sarah.wilson@company.com` / `password123`
- `david.brown@company.com` / `password123`
- `lisa.davis@company.com` / `password123`

## Running with Docker

```bash
# From project root
docker-compose up --build
```

This will start:
- MongoDB on port 27017
- Backend API on port 8000
- Frontend on port 3000

## API Documentation

Once running, visit:
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## SLA Business-Time Calculation

The SLA system uses business-time calculations that exclude weekends to prevent false breaches while maintaining 24/7 monitoring on weekdays.

### How It Works

- **Business Days**: Monday through Friday are considered business days
- **Weekends**: Saturday and Sunday are excluded from SLA calculations
- **24/7 Monitoring**: The system continuously monitors tickets but only counts business time toward SLA deadlines

### Example

If a ticket is created on Friday at 4:00 PM with a 4-hour SLA:
- The SLA due date will be calculated as Monday at 12:00 PM (skipping the weekend)
- The ticket will not breach over the weekend, even though calendar time has passed

### Implementation Details

- Business-time utilities are in `src/utils/business_date.py`
- SLA calculations are handled by `src/services/sla_service.py`
- To add holiday support in the future, extend the `is_business_day()` function in `business_date.py`

### Testing

Run the business date utility tests:
```bash
python test_business_date.py
```