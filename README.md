# JackpotHaven

JackpotHaven is a Django-based web application designed for betting enthusiasts. This platform allows users to place bets on various events, 
making it the ultimate destination for betting lovers.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [Contact](#contact)

## Features
- **User Authentication**: Secure login and registration system.
- **Betting System**: Users can place bets on various events.
- **Payment Integration**: Supports payment methods like Stripe and PayPal.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Admin Dashboard**: Manage users, events, and bets from a user-friendly interface.


## Installation


### Steps to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kamranzaman0/jackpothaven.git
   cd jackpothaven
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database:**
   - Update the `settings.py` file with your database credentials.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**
   - Visit `http://127.0.0.1:8000/` in your browser.

## Usage

- **Creating an Account**: Users can sign up with their email and password.
- **Placing Bets**: Browse available events and place bets.
- **Admin Panel**: Access the admin panel at `/admin/` to manage the app.
## Technologies Used
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Payment Integration**: Stripe, PayPal
- **Version Control**: Git, GitHub

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.


## Contact
For any inquiries, feel free to reach out:

- **Kamran Zaman** - [kamranzaman0@gmail.com](mailto:kamranzaman0@gmail.com)
