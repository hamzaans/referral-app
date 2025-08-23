from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "referral.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Doctor model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    fax = db.Column(db.String(20), nullable=False)
    
    # Insurance acceptance fields (boolean for each insurance)
    takes_carefirst_community_healthplan = db.Column(db.Boolean, default=False)
    takes_united_healthcare_community = db.Column(db.Boolean, default=False)
    takes_priority_partners = db.Column(db.Boolean, default=False)
    takes_maryland_physicians_care = db.Column(db.Boolean, default=False)
    takes_aetna_betterhealth = db.Column(db.Boolean, default=False)
    takes_maryland_medical_assistance = db.Column(db.Boolean, default=False)
    takes_wellpoint = db.Column(db.Boolean, default=False)
    takes_aetna_medicare = db.Column(db.Boolean, default=False)
    takes_carefirst_medicare = db.Column(db.Boolean, default=False)
    takes_cigna_medicare = db.Column(db.Boolean, default=False)
    takes_humana = db.Column(db.Boolean, default=False)
    takes_john_hopkins = db.Column(db.Boolean, default=False)
    takes_united_healthcare_medicare = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'address': self.address,
            'phone': self.phone,
            'fax': self.fax,
            'insurance': {
                'carefirst_community_healthplan': self.takes_carefirst_community_healthplan,
                'united_healthcare_community': self.takes_united_healthcare_community,
                'priority_partners': self.takes_priority_partners,
                'maryland_physicians_care': self.takes_maryland_physicians_care,
                'aetna_betterhealth': self.takes_aetna_betterhealth,
                'maryland_medical_assistance': self.takes_maryland_medical_assistance,
                'wellpoint': self.takes_wellpoint,
                'aetna_medicare': self.takes_aetna_medicare,
                'carefirst_medicare': self.takes_carefirst_medicare,
                'cigna_medicare': self.takes_cigna_medicare,
                'humana': self.takes_humana,
                'john_hopkins': self.takes_john_hopkins,
                'united_healthcare_medicare': self.takes_united_healthcare_medicare
            }
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/specialties')
def get_specialties():
    """Get all available specialties"""
    # Predefined list of medical specialties
    specialties = [
        'Allergy and Immunology',
        'Anesthesiology',
        'Cardiology',
        'Cardiothoracic Surgery',
        'Dermatology',
        'Emergency Medicine',
        'Endocrinology',
        'Family Medicine',
        'Gastroenterology',
        'General Surgery',
        'Geriatrics',
        'Hematology/Oncology',
        'Infectious Disease',
        'Internal Medicine',
        'Nephrology',
        'Neurology',
        'Neurosurgery',
        'Obstetrics and Gynecology',
        'Ophthalmology',
        'Orthopedic Surgery',
        'Otolaryngology (ENT)',
        'Pathology',
        'Pediatrics',
        'Physical Medicine and Rehabilitation',
        'Plastic Surgery',
        'Psychiatry',
        'Pulmonology',
        'Radiology',
        'Rheumatology',
        'Urology',
        'Vascular Surgery'
    ]
    return jsonify(sorted(specialties))

@app.route('/api/insurances')
def get_insurances():
    """Get all available insurance options"""
    return jsonify([
        'carefirst_community_healthplan',
        'united_healthcare_community',
        'priority_partners',
        'maryland_physicians_care',
        'aetna_betterhealth',
        'maryland_medical_assistance',
        'wellpoint',
        'aetna_medicare',
        'carefirst_medicare',
        'cigna_medicare',
        'humana',
        'john_hopkins',
        'united_healthcare_medicare'
    ])

@app.route('/api/doctors')
def get_doctors():
    """Get doctors by specialty and insurance"""
    specialty = request.args.get('specialty')
    insurance = request.args.get('insurance')
    
    if not specialty or not insurance:
        return jsonify({'error': 'Both specialty and insurance are required'}), 400
    
    # Build query based on specialty and insurance
    query = Doctor.query.filter(Doctor.specialty == specialty)
    
    # Filter by insurance acceptance
    insurance_mapping = {
        'carefirst_community_healthplan': Doctor.takes_carefirst_community_healthplan,
        'united_healthcare_community': Doctor.takes_united_healthcare_community,
        'priority_partners': Doctor.takes_priority_partners,
        'maryland_physicians_care': Doctor.takes_maryland_physicians_care,
        'aetna_betterhealth': Doctor.takes_aetna_betterhealth,
        'maryland_medical_assistance': Doctor.takes_maryland_medical_assistance,
        'wellpoint': Doctor.takes_wellpoint,
        'aetna_medicare': Doctor.takes_aetna_medicare,
        'carefirst_medicare': Doctor.takes_carefirst_medicare,
        'cigna_medicare': Doctor.takes_cigna_medicare,
        'humana': Doctor.takes_humana,
        'john_hopkins': Doctor.takes_john_hopkins,
        'united_healthcare_medicare': Doctor.takes_united_healthcare_medicare
    }
    
    if insurance in insurance_mapping:
        query = query.filter(insurance_mapping[insurance] == True)
    else:
        return jsonify({'error': 'Invalid insurance type'}), 400
    
    doctors = query.all()
    return jsonify([doctor.to_dict() for doctor in doctors])

@app.route('/api/doctors/all')
def get_all_doctors():
    """Get all doctors for admin purposes"""
    doctors = Doctor.query.all()
    return jsonify([doctor.to_dict() for doctor in doctors])

@app.route('/api/doctors', methods=['POST'])
def add_doctor():
    """Add a new doctor"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'specialty', 'address', 'phone', 'fax']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create new doctor
        doctor = Doctor(
            name=data['name'],
            specialty=data['specialty'],
            address=data['address'],
            phone=data['phone'],
            fax=data['fax'],
            takes_carefirst_community_healthplan=data.get('takes_carefirst_community_healthplan', False),
            takes_united_healthcare_community=data.get('takes_united_healthcare_community', False),
            takes_priority_partners=data.get('takes_priority_partners', False),
            takes_maryland_physicians_care=data.get('takes_maryland_physicians_care', False),
            takes_aetna_betterhealth=data.get('takes_aetna_betterhealth', False),
            takes_maryland_medical_assistance=data.get('takes_maryland_medical_assistance', False),
            takes_wellpoint=data.get('takes_wellpoint', False),
            takes_aetna_medicare=data.get('takes_aetna_medicare', False),
            takes_carefirst_medicare=data.get('takes_carefirst_medicare', False),
            takes_cigna_medicare=data.get('takes_cigna_medicare', False),
            takes_humana=data.get('takes_humana', False),
            takes_john_hopkins=data.get('takes_john_hopkins', False),
            takes_united_healthcare_medicare=data.get('takes_united_healthcare_medicare', False)
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        return jsonify({'message': 'Doctor added successfully', 'doctor': doctor.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Update an existing doctor"""
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            doctor.name = data['name']
        if 'specialty' in data:
            doctor.specialty = data['specialty']
        if 'address' in data:
            doctor.address = data['address']
        if 'phone' in data:
            doctor.phone = data['phone']
        if 'fax' in data:
            doctor.fax = data['fax']
        
        # Update insurance fields
        if 'takes_carefirst_community_healthplan' in data:
            doctor.takes_carefirst_community_healthplan = data['takes_carefirst_community_healthplan']
        if 'takes_united_healthcare_community' in data:
            doctor.takes_united_healthcare_community = data['takes_united_healthcare_community']
        if 'takes_priority_partners' in data:
            doctor.takes_priority_partners = data['takes_priority_partners']
        if 'takes_maryland_physicians_care' in data:
            doctor.takes_maryland_physicians_care = data['takes_maryland_physicians_care']
        if 'takes_aetna_betterhealth' in data:
            doctor.takes_aetna_betterhealth = data['takes_aetna_betterhealth']
        if 'takes_maryland_medical_assistance' in data:
            doctor.takes_maryland_medical_assistance = data['takes_maryland_medical_assistance']
        if 'takes_wellpoint' in data:
            doctor.takes_wellpoint = data['takes_wellpoint']
        if 'takes_aetna_medicare' in data:
            doctor.takes_aetna_medicare = data['takes_aetna_medicare']
        if 'takes_carefirst_medicare' in data:
            doctor.takes_carefirst_medicare = data['takes_carefirst_medicare']
        if 'takes_cigna_medicare' in data:
            doctor.takes_cigna_medicare = data['takes_cigna_medicare']
        if 'takes_humana' in data:
            doctor.takes_humana = data['takes_humana']
        if 'takes_john_hopkins' in data:
            doctor.takes_john_hopkins = data['takes_john_hopkins']
        if 'takes_united_healthcare_medicare' in data:
            doctor.takes_united_healthcare_medicare = data['takes_united_healthcare_medicare']
        
        db.session.commit()
        
        return jsonify({'message': 'Doctor updated successfully', 'doctor': doctor.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Delete a doctor"""
    try:
        doctor = Doctor.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        
        return jsonify({'message': 'Doctor deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        # Drop all tables and recreate them to handle schema changes
        db.drop_all()
        db.create_all()
        
        # Check if data already exists
        if Doctor.query.first():
            return
        
        # Sample doctors data with Maryland-specific insurance plans
        sample_doctors = [
            {
                'name': 'Dr. John Smith',
                'specialty': 'Cardiology',
                'address': '123 Heart Lane, Waldorf, MD 20602',
                'phone': '301-555-0101',
                'fax': '301-555-0102',
                'takes_carefirst_community_healthplan': True,
                'takes_aetna_medicare': True,
                'takes_maryland_medical_assistance': True
            },
            {
                'name': 'Dr. Sarah Johnson',
                'specialty': 'Gastroenterology',
                'address': '456 Stomach St, Silver Spring, MD 20910',
                'phone': '301-555-0201',
                'fax': '301-555-0202',
                'takes_priority_partners': True,
                'takes_united_healthcare_medicare': True,
                'takes_maryland_physicians_care': True
            },
            {
                'name': 'Dr. Michael Brown',
                'specialty': 'Cardiology',
                'address': '789 Cardiac Ave, Bethesda, MD 20814',
                'phone': '301-555-0301',
                'fax': '301-555-0302',
                'takes_humana': True,
                'takes_carefirst_medicare': True,
                'takes_aetna_betterhealth': True
            },
            {
                'name': 'Dr. Emily Davis',
                'specialty': 'Dermatology',
                'address': '321 Skin Way, Rockville, MD 20850',
                'phone': '301-555-0401',
                'fax': '301-555-0402',
                'takes_united_healthcare_community': True,
                'takes_wellpoint': True,
                'takes_john_hopkins': True
            }
        ]
        
        for doctor_data in sample_doctors:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
        
        db.session.commit()
        print("Database initialized with sample data")

# Initialize database when the app starts
init_db()

# For Vercel deployment
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
