from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime # Import datetime for setting default date

# --- Flask App Configuration ---
app = Flask(__name__)

# Configure database path (SQLite database will be in the 'instance' folder)
# The 'instance' folder is typically outside of version control for security/flexibility
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppress a warning
app.config['SECRET_KEY'] = 'YOUR_SUPER_SECRET_KEY_HERE' # <<< IMPORTANT: CHANGE THIS!

# Initialize the database
db = SQLAlchemy(app)

# --- Database Models (Define your tables) ---

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Use datetime.utcnow

    def __repr__(self):
        return f'<ContactMessage {self.name} - {self.subject}>'

class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    event_name = db.Column(db.String(200), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Use datetime.utcnow
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='Pending') # e.g., 'Pending', 'Confirmed', 'Attended'

    def __repr__(self):
        return f'<EventRegistration {self.name} - {self.event_name}>'

# --- Routes (Your Website's Pages) ---

@app.route('/')
def index():
    # You can add a success message for contact form here if needed
    return render_template('index.html')

@app.route('/contact-us') # This is your Event Registration page
def event_registration_page():
    return render_template('contact-us.html')

@app.route('/event-admin')
def event_admin_page():
    # Fetch all event registrations from the database to display
    registrations = EventRegistration.query.order_by(EventRegistration.registration_date.desc()).all()
    return render_template('event-admin.html', registrations=registrations)

@app.route('/contact-admin')
def contact_admin_page():
    # Fetch all contact messages from the database to display
    messages = ContactMessage.query.order_by(ContactMessage.date_submitted.desc()).all()
    return render_template('contact-admin.html', messages=messages)

# --- Form Submission Handlers ---

# Handler for general Contact Us form submission (if you add one on index.html)
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form.get('subject')
        message = request.form['message']

        new_message = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success') # Flash message for user feedback
        return redirect(url_for('index')) # Redirect to home page
    flash('Invalid request method for contact form.', 'error')
    return redirect(url_for('index'))

# Handler for Event Registration form submission (from contact-us.html)
@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        event_name = request.form['event'] # Ensure your form field has name="event"
        phone = request.form.get('phone')
        company = request.form.get('company')

        new_registration = EventRegistration(
            name=name,
            email=email,
            event_name=event_name,
            phone=phone,
            company=company
        )
        db.session.add(new_registration)
        db.session.commit()
        flash('Your event registration was successful!', 'success') # Flash message
        return redirect(url_for('event_registration_page')) # Redirect back to the registration page
    flash('Invalid request method for registration form.', 'error')
    return redirect(url_for('event_registration_page'))

# --- Database Creation/Management Command ---
# This function will create the database file and tables when run
@app.cli.command('create-db')
def create_db():
    """Creates the database tables."""
    with app.app_context(): # Essential for working with Flask app context
        # Ensure the 'instance' folder exists
        os.makedirs(app.instance_path, exist_ok=True)
        db.create_all()
    print("Database tables created!")

# --- Run the App ---
if __name__ == '__main__':
    # This line is usually handled by 'flask create-db' or 'flask run'
    # but ensures instance path exists if app.run() is called directly.
    os.makedirs(app.instance_path, exist_ok=True)
    app.run(debug=True)