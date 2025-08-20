# Medical Referral Finder

A simple web application for primary care offices to manage and search doctor referrals based on medical specialty and insurance acceptance.

## Features

- **Simple Interface**: Two dropdown menus for specialty and insurance selection
- **Comprehensive Search**: Find doctors by specialty and insurance acceptance
- **Doctor Information**: Display doctor's name, address, phone, and fax numbers
- **Flexible Insurance Handling**: Boolean fields for each insurance type
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Styling**: Modern, clean CSS with responsive design

## Installation & Setup

1. **Navigate to the project directory:**
   ```bash
   cd /home/hamzaans/referral-app
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://localhost:5000`

## Database Schema

### Doctor Model
- **id**: Primary key
- **name**: Doctor's full name
- **specialty**: Medical specialty (e.g., Cardiology, Gastroenterology)
- **address**: Full address
- **phone**: Phone number
- **fax**: Fax number
- **Insurance acceptance fields** (Boolean):
  - takes_carefirst
  - takes_united_healthcare
  - takes_aetna
  - takes_cigna
  - takes_bcbs
  - takes_medicare
  - takes_medicaid

## API Endpoints

- `GET /`: Main application page
- `GET /api/specialties`: Get all available medical specialties
- `GET /api/insurances`: Get all available insurance types
- `GET /api/doctors?specialty=X&insurance=Y`: Get doctors by specialty and insurance

## Sample Data

The application comes pre-loaded with sample doctor data including:
- Cardiologists
- Gastroenterologists
- Dermatologists
- Neurologists

Each doctor has various insurance acceptance patterns to demonstrate the filtering functionality.

## Usage

1. **Select Medical Specialty**: Choose from the dropdown (e.g., Cardiology, Gastroenterology)
2. **Select Insurance**: Choose the insurance type (e.g., CareFirst, United Healthcare)
3. **Click "Find Doctors"**: View matching doctors with their contact information

## Adding New Data

To add new doctors or modify existing data, you can:
1. Edit the `sample_doctors` list in `app.py`
2. Add new insurance types by modifying the Doctor model
3. Restart the application to reload the database

## Customization

- **Add Insurance Types**: Modify the Doctor model in `app.py` to add new boolean fields
- **Modify Specialties**: Add doctors with new specialties to the sample data
- **Styling**: Update the CSS in `templates/index.html` to match your office branding
