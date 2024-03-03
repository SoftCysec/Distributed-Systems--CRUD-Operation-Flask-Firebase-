# User Authentication and Dashboard

This project implements user authentication and a user dashboard using Flask, Firebase, and Bootstrap.

## Features

- **User Authentication:** Allows users to register, login, and reset their passwords securely.

- **User Dashboard:** Displays a personalized dashboard for authenticated users.

- **Contact Management:** Users can save and search for contacts in the dashboard.

## Technologies Used

- **Flask:** A lightweight web application framework for Python.

- **Firebase:** A cloud-based platform for building web and mobile apps.

- **Bootstrap:** A popular front-end framework for designing responsive and stylish web pages.

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up Firebase project:

    - Create a new Firebase project at [https://console.firebase.google.com](https://console.firebase.google.com).
    - Enable the Authentication and Firestore services.
    - Generate a new private key for your Firebase project and save it as `serviceAccountKey.json` in the project root directory.

4. Configure the Flask app:

    - Rename the `config.example.py` file to `config.py`.
    - Update the `config.py` file with your Firebase project credentials.

5. Run the application:

    ```bash
    python app.py
    ```

6. Open your web browser and visit [http://localhost:5000](http://localhost:5000) to access the application.

7. Enjoy using the User Authentication and Dashboard application!
