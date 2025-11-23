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

## Environment Variables

### Required:
- `MONGODB_URI` - MongoDB connection string (e.g., `mongodb://mongo:27017/ticketing_db`)

### Optional:
- `GOOGLE_API_KEY` - Required only for AI features (ticket summarization, closing comments generation)
  - If not set, the application will start successfully but AI endpoints will return 503 errors
  - Get your API key from: https://makersuite.google.com/app/apikey

## IDE Setup for Frontend Development

If you're working on the frontend and seeing TypeScript errors in your IDE (like "Cannot find module 'date-fns'"), you'll need to install dependencies locally:

```bash
cd frontend
npm install
```

**Note:** This is only needed for IDE IntelliSense/type checking. The application runs fine in Docker without local node_modules since dependencies are installed in the container.

### Alternative IDE Setup Options:
1. **VS Code Dev Containers** - Use the Dev Containers extension for full IDE integration with Docker
2. **Ignore IDE Errors** - If only developing in Docker, you can safely ignore these TypeScript errors as they're false positives