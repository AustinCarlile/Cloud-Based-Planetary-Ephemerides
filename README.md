# 🌌 Cloud-Based Planetary Ephemerides
Cloud-Based Planetary Ephemerides is a capstone project designed to provide accurate planetary position data through a scalable, cloud-hosted API. This project integrates astronomical computation with modern web technologies to deliver real-time ephemeris data, suitable for applications in astronomy, education, and software development.

Features
● RESTful API: Access planetary positions via HTTP endpoints.
● Cloud Deployment: Hosted on cloud platforms for high availability and scalability.
● Modular Architecture: Separation of concerns between computation, API handling, and frontend presentation.
● User Interface: Web-based frontend for interactive exploration of planetary data.

Project Structure
Cloud-Based-Planetary-Ephemerides/
├── API/               # Backend API code
├── deliverable/       # Project documentation and reports
├── website/           # Frontend web application
├── LICENSE            # Project license (CC0-1.0)
└── README.md          # Project overview and setup instructions

Technologies Used
● Backend: Python, Flask, and astronomical libraries for ephemeris calculations.
● Frontend: HTML, CSS, JavaScript (possibly with frameworks like React or Vue.js).
● Cloud Services: Deployment on platforms such as AWS, Azure, or Heroku.
● Data Sources: Integration with astronomical datasets (e.g., NASA JPL ephemerides).

Getting Started
Prerequisites
● Python 3.8+
● Node.js (for frontend development)
● Docker (optional, for containerized deployment)

Backend Setup (API)
1. Navigate to the API directory:
   cd API
2. Create a virtual environment and activate it:
   python3 -m venv venv
   source venv/bin/activate
3. Install the required dependencies:
   pip install -r requirements.txt
4. Run the API server:
   python app.py
   The API will be accessible at http://localhost:5000.

Frontend Setup (Web Interface)
1. Navigate to the website directory:
   cd website
2. Install the required dependencies:
   npm install
3. Start the development server:
   npm start
   The web application will be accessible at http://localhost:3000.

Usage
● Access the web interface to visualize planetary data.
● Utilize the API endpoints to programmatically retrieve ephemeris data. Detailed API documentation is available in the API/ directory.

License
This project is licensed under the CC0-1.0 License, dedicating it to the public domain.

Acknowledgments
● Developed as a capstone project by Austin Carlile, Nicholas Gonzalez, Minuka Trikawalagoda, and Noah Schwartz.
● Inspired by existing astronomical computation tools and ephemeris data services.
