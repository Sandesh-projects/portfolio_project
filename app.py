import csv  # Import the CSV module to handle reading and writing CSV files
from flask import Flask, render_template, request, redirect, url_for  # Import Flask and related modules for web app functionality

app = Flask(__name__)  # Create a Flask application instance

# Sample projects data for the Portfolio page
projects = [
    {
        "title": "Myntra Clone",  # Title of the project
        "description": (  # Description of the project
            "An e-commerce platform clone featuring user registration"
            "product listings, a shopping cart, secure checkout, and "
            "responsive design."
        ),
        "image": "Myntra Clone.png",  # Image file for the project
        "link": "https://sandesh-projects.github.io/IP-lab-work/Practice%20Myntra%20Clone/myntra.html"  # Link to the project
    },
    {
        "title": "Mentorlink App",  # Title of the project
        "description": (  # Description of the project
            "A mentorship platform connecting students and professionals. "
            "Key features will include messaging, scheduling, and progress "
            "tracking for mentorship sessions. (Under development)"
        ),
        "image": "quiz.jpg",  # Image file for the project
        "link": "#"  # Placeholder link for the project
    },
    {
        "title": "Bat Ball and Stump",  # Title of the project
        "description": (  # Description of the project
            "A fun twist on Rock-Paper-Scissors with a cricket theme. "
            "Bat beats Ball, Ball beats Stump, and Stump beats Bat. "
            "Features interactive gameplay, simple UI, and scoreboard tracking."
        ),
        "image": "batballstump.png",  # Image file for the project
        "link": "https://sandesh-projects.github.io/IP-lab-work/Bat%20Ball%20Stump%20optimize/batBallStump.html"  # Link to the project
    }
]

# 1. Read all contacts from CSV
def read_contacts():
    contacts = []  # Initialize an empty list to store contacts
    try:
        with open('contact.csv', 'r', newline='', encoding='utf-8') as csvfile:  # Open the CSV file in read mode
            reader = csv.DictReader(csvfile)  # Create a DictReader to read rows as dictionaries
            for row in reader:  # Iterate through each row in the CSV
                contacts.append(row)  # Append the row (contact) to the list
    except FileNotFoundError:  # Handle the case where the file does not exist
        pass  # Do nothing and return an empty list
    return contacts  # Return the list of contacts

# 2. Write the entire contacts list to CSV
def write_contacts(contacts):
    with open('contact.csv', 'w', newline='', encoding='utf-8') as csvfile:  # Open the CSV file in write mode
        fieldnames = ['id', 'name', 'email', 'subject', 'message']  # Define the column headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)  # Create a DictWriter to write dictionaries
        writer.writeheader()  # Write the header row
        for contact in contacts:  # Iterate through the list of contacts
            writer.writerow(contact)  # Write each contact as a row in the CSV

# 3. Get the next ID for a new contact
def get_next_id(contacts):
    if not contacts:  # If the contacts list is empty
        return 1  # Return 1 as the first ID
    max_id = max(int(contact['id']) for contact in contacts)  # Find the maximum ID in the list
    return max_id + 1  # Return the next ID by incrementing the maximum ID

@app.route('/')  # Define the route for the home page
def home():
    return render_template('home.html')  # Render the home.html template

@app.route('/portfolio')  # Define the route for the portfolio page
def portfolio():
    # Pass the projects list to the template
    return render_template('portfolio.html', projects=projects)  # Render the portfolio.html template with projects data

@app.route('/contact', methods=['GET', 'POST'])  # Define the route for the contact page with GET and POST methods
def contact():
    if request.method == 'POST':  # If the request method is POST (form submission)
        # Retrieve form data
        name = request.form.get('name')  # Get the 'name' field from the form
        email = request.form.get('email')  # Get the 'email' field from the form
        subject = request.form.get('subject')  # Get the 'subject' field from the form
        message = request.form.get('message')  # Get the 'message' field from the form

        # Read existing contacts
        contacts = read_contacts()  # Read the existing contacts from the CSV file

        # Prepare new entry with a unique ID
        new_id = get_next_id(contacts)  # Get the next unique ID
        new_contact = {  # Create a dictionary for the new contact
            'id': str(new_id),  # Convert the ID to a string
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }

        # Append and write back to CSV
        contacts.append(new_contact)  # Add the new contact to the list
        write_contacts(contacts)  # Write the updated list back to the CSV file

        # Redirect to the success page, passing data via query parameters
        return redirect(url_for('success', name=name, email=email, subject=subject, message=message))  # Redirect to the success page
    
    return render_template('contact.html')  # Render the contact.html template for GET requests

@app.route('/success')  # Define the route for the success page
def success():
    # Retrieve data from query parameters
    name = request.args.get('name')  # Get the 'name' parameter from the URL
    email = request.args.get('email')  # Get the 'email' parameter from the URL
    subject = request.args.get('subject')  # Get the 'subject' parameter from the URL
    message = request.args.get('message')  # Get the 'message' parameter from the URL
    return render_template('success.html', name=name, email=email, subject=subject, message=message)  # Render the success.html template with the data

# 4. New route to list all contact requests
@app.route('/requests')  # Define the route for the requests page
def list_requests():
    contacts = read_contacts()  # Read all contacts from the CSV file
    return render_template('requests.html', contacts=contacts)  # Render the requests.html template with the contacts data

# 5. Route to delete a contact by ID
@app.route('/delete/<int:contact_id>')  # Define the route to delete a contact by its ID
def delete_contact(contact_id):
    contacts = read_contacts()  # Read all contacts from the CSV file
    # Filter out the contact with matching ID
    updated_contacts = [c for c in contacts if int(c['id']) != contact_id]  # Create a new list excluding the contact with the given ID
    write_contacts(updated_contacts)  # Write the updated list back to the CSV file
    return redirect(url_for('list_requests'))  # Redirect to the requests page

if __name__ == '__main__':  # Check if the script is run directly
    app.run(debug=True)  # Run the Flask app in debug mode