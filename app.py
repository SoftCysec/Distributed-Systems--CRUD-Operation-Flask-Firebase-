from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask_mail import Mail, Message


app = Flask(__name__)

# Initialize Firebase credentials
cred = credentials.Certificate('Configs/distributed-systems-e4695-firebase-adminsdk-ixk0v-322ed17123.json')
firebase_admin.initialize_app(cred)

# Create a Firestore client
db = firestore.client()

# Configure Flask Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Replace with your email password
mail = Mail(app)

@app.route('/')
def home():
    return render_template('user_auth_modal.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username  # Set username as display name
        )

        # Create a new user document in the Firestore collection
        user_data = {
            'email': email,
            'username': username,
            'uid': user.uid
        }
        db.collection('users').document(user.uid).set(user_data)

        return redirect(url_for('home'))

    except auth.AuthError as e:
        error_message = str(e)
        return render_template('user_auth_modal.html', register_error=error_message)


@app.route('/user_auth_modal', methods=['POST'])
def user_auth_modal():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Sign in the user with Firebase Authentication
        auth.sign_in_with_email_and_password(email, password)

        return render_template('dashboard.html', email=email)

    except auth.AuthError as e:
        error_message = str(e)
        return render_template('user_auth_modal.html', login_error=error_message)


def generate_reset_link(email):
    user = auth.get_user_by_email(email)
    reset_link = auth.generate_password_reset_link(user.uid)
    return reset_link


@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')

    try:
        # Send a password reset email using Firebase Authentication
        reset_link = generate_reset_link(email)
        # Implement the logic to send the reset email
        msg = Message('Password Reset', recipients=[email])
        msg.body = f"Click the following link to reset your password: {reset_link}"
        mail.send(msg)

        return redirect(url_for('home'))

    except auth.AuthError as e:
        error_message = str(e)
        return render_template('user_auth_modal.html', reset_error=error_message)
    
    
@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('dashboard.html', username=username)
    
    
@app.route('/save_contact', methods=['POST'])
def save_contact():
    if request.method == 'POST':
        username = request.form.get('username')
        mobile_number = request.form.get('mobile_number')
        email = request.form.get('email')
        address = request.form.get('address')
        registration_number = request.form.get('registration_number')

        # Save contact details to Firestore
        contact_data = {
            'username': username,
            'mobile_number': mobile_number,
            'email': email,
            'address': address,
        }
        db.collection('contacts').document(registration_number).set(contact_data)

        # Redirect to the dashboard with a success message
        return render_template('dashboard.html', username=username, success_message='Contact saved successfully')

    # Redirect to the dashboard if the form submission fails
    return redirect(url_for('home'))



@app.route('/search_contacts', methods=['GET', 'POST'])
def search_contacts():
    if request.method == 'POST':
        registration_number = request.form.get('registration_number')

        # Query the Firestore collection for the contact with the given registration number
        contact_ref = db.collection('contacts').document(registration_number)
        contact_data = contact_ref.get().to_dict()

        if contact_data:
            # Contact found, retrieve the contact details
            return render_template('search_contacts.html', contact_data=contact_data)
        else:
            # No contact found with the given registration number
            return render_template('search_contacts.html', error_message='No contact found')

    return render_template('search_contacts.html')


if __name__ == '__main__':
    app.run(debug=True)
