# MedNexus AI

MedNexus AI is an advanced biomedical data analysis system that synthesizes multi-modal biomedical data to provide precise diagnoses, treatment plans, and real-time patient monitoring.

## Features

- **Comprehensive Patient Dashboard**: View patient demographics, conditions, medications, vital signs, and lab results
- **AI-Powered Analysis**: Generate diagnoses, risk factors, treatment recommendations, and monitoring plans
- **Real-time Patient Monitoring**: Track vital signs in real-time with automatic alerts for abnormal values
- **Medical Image Analysis**: AI-powered analysis of X-rays, MRIs, and CT scans with detailed findings and recommendations
- **Disease Progression Prediction**: Forecast disease trajectories with confidence scores and personalized recommendations

## Technology Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript with Bootstrap 5
- **Data Visualization**: Chart.js
- **AI Simulation**: Simulated AI analysis for demonstration purposes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mednexus-ai.git
cd mednexus-ai
```

2. Install dependencies:
```bash
pip install flask pandas numpy scikit-learn matplotlib pillow
```

3. Run the application:
```bash
python app.py
```

4. Access the application at http://localhost:8080

## Usage

1. Select a patient from the list on the left side
2. View their basic information and vitals
3. Click "Analyze with MedNexus AI" to generate comprehensive analysis
4. Explore the different sections:
   - AI Analysis
   - Real-time Monitoring (click "Start Monitoring")
   - Medical Images (click "Analyze with AI" on any image)
   - Disease Progression (click "Generate Progression Prediction")

## Screenshots

![MedNexus AI Dashboard](screenshots/dashboard.png)
![Patient Analysis](screenshots/analysis.png)
![Medical Image Analysis](screenshots/image-analysis.png)

## License

MIT

## Disclaimer

This is a demonstration application. It does not use real patient data or provide actual medical diagnoses. The AI analysis is simulated for demonstration purposes only.