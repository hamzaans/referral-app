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
    takes_carefirst = db.Column(db.Boolean, default=False)
    takes_united_healthcare = db.Column(db.Boolean, default=False)
    takes_aetna = db.Column(db.Boolean, default=False)
    takes_cigna = db.Column(db.Boolean, default=False)
    takes_bcbs = db.Column(db.Boolean, default=False)
    takes_medicare = db.Column(db.Boolean, default=False)
    takes_medicaid = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'address': self.address,
            'phone': self.phone,
            'fax': self.fax,
            'insurance': {
                'carefirst': self.takes_carefirst,
                'united_healthcare': self.takes_united_healthcare,
                'aetna': self.takes_aetna,
                'cigna': self.takes_cigna,
                'bcbs': self.takes_bcbs,
                'medicare': self.takes_medicare,
                'medicaid': self.takes_medicaid
            }
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/specialties')
def get_specialties():
    """Get all unique specialties"""
    specialties = db.session.query(Doctor.specialty).distinct().all()
    return jsonify([s[0] for s in specialties])

@app.route('/api/insurances')
def get_insurances():
    """Get all available insurance options"""
    return jsonify([
        'carefirst',
        'united_healthcare', 
        'aetna',
        'cigna',
        'bcbs',
        'medicare',
        'medicaid'
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
        'carefirst': Doctor.takes_carefirst,
        'united_healthcare': Doctor.takes_united_healthcare,
        'aetna': Doctor.takes_aetna,
        'cigna': Doctor.takes_cigna,
        'bcbs': Doctor.takes_bcbs,
        'medicare': Doctor.takes_medicare,
        'medicaid': Doctor.takes_medicaid
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
            takes_carefirst=data.get('takes_carefirst', False),
            takes_united_healthcare=data.get('takes_united_healthcare', False),
            takes_aetna=data.get('takes_aetna', False),
            takes_cigna=data.get('takes_cigna', False),
            takes_bcbs=data.get('takes_bcbs', False),
            takes_medicare=data.get('takes_medicare', False),
            takes_medicaid=data.get('takes_medicaid', False)
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
        if 'takes_carefirst' in data:
            doctor.takes_carefirst = data['takes_carefirst']
        if 'takes_united_healthcare' in data:
            doctor.takes_united_healthcare = data['takes_united_healthcare']
        if 'takes_aetna' in data:
            doctor.takes_aetna = data['takes_aetna']
        if 'takes_cigna' in data:
            doctor.takes_cigna = data['takes_cigna']
        if 'takes_bcbs' in data:
            doctor.takes_bcbs = data['takes_bcbs']
        if 'takes_medicare' in data:
            doctor.takes_medicare = data['takes_medicare']
        if 'takes_medicaid' in data:
            doctor.takes_medicaid = data['takes_medicaid']
        
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
        db.create_all()
        
        # Check if data already exists
        if Doctor.query.first():
            return
        
        # Sample doctors data
        sample_doctors = [
            {
                'name': 'Dr. John Smith',
                'specialty': 'Cardiology',
                'address': '123 Heart Lane, Waldorf, MD 20602',
                'phone': '301-555-0101',
                'fax': '301-555-0102',
                'takes_carefirst': True,
                'takes_united_healthcare': False,
                'takes_aetna': True,
                'takes_medicare': True
            },
            {
                'name': 'Dr. Sarah Johnson',
                'specialty': 'Gastroenterology',
                'address': '456 Stomach St, Silver Spring, MD 20910',
                'phone': '301-555-0201',
                'fax': '301-555-0202',
                'takes_carefirst': True,
                'takes_united_healthcare': True,
                'takes_cigna': True,
                'takes_medicare': True
            },
            {
                'name': 'Dr. Michael Brown',
                'specialty': 'Cardiology',
                'address': '789 Cardiac Ave, Bethesda, MD 20814',
                'phone': '301-555-0301',
                'fax': '301-555-0302',
                'takes_united_healthcare': True,
                'takes_aetna': True,
                'takes_bcbs': True,
                'takes_medicare': True
            },
            {
                'name': 'Dr. Emily Davis',
                'specialty': 'Dermatology',
                'address': '321 Skin Way, Rockville, MD 20850',
                'phone': '301-555-0401',
                'fax': '301-555-0402',
                'takes_carefirst': True,
                'takes_united_healthcare': False,
                'takes_aetna': True,
                'takes_medicaid': True
            },
            {
                'name': 'Dr. Robert Wilson',
                'specialty': 'Gastroenterology',
                'address': '654 Digestive Dr, Annapolis, MD 21401',
                'phone': '410-555-0501',
                'fax': '410-555-0502',
                'takes_carefirst': False,
                'takes_united_healthcare': True,
                'takes_cigna': True,
                'takes_bcbs': True,
                'takes_medicare': True
            },
            {
                'name': 'Dr. Lisa Anderson',
                'specialty': 'Neurology',
                'address': '987 Brain Blvd, Baltimore, MD 21201',
                'phone': '410-555-0601',
                'fax': '410-555-0602',
                'takes_carefirst': True,
                'takes_united_healthcare': True,
                'takes_aetna': False,
                'takes_medicare': True,
                'takes_medicaid': True
            }
        ]
        
        for doctor_data in sample_doctors:
            doctor = Doctor(**doctor_data)
            db.session.add(doctor)
        
        db.session.commit()
        print("Database initialized with sample data")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
