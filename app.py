from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
import json
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='/static')

# Configure static folder
app.static_folder = 'static'

# Sample patient data
patients = {
    "P001": {
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "conditions": ["Hypertension", "Type 2 Diabetes"],
        "vitals": {
            "heart_rate": [75, 78, 72, 76, 74],
            "blood_pressure": ["120/80", "125/82", "118/79", "122/81", "120/78"],
            "temperature": [98.6, 98.7, 98.5, 98.6, 98.6],
            "oxygen_saturation": [98, 97, 98, 99, 98]
        },
        "medications": ["Lisinopril", "Metformin"],
        "lab_results": {
            "glucose": [142, 138, 145],
            "hba1c": [6.8],
            "cholesterol": [210]
        }
    },
    "P002": {
        "name": "Jane Smith",
        "age": 38,
        "gender": "Female",
        "conditions": ["Asthma", "Allergic Rhinitis"],
        "vitals": {
            "heart_rate": [68, 70, 67, 69, 71],
            "blood_pressure": ["118/75", "120/76", "117/74", "119/75", "121/77"],
            "temperature": [98.4, 98.5, 98.3, 98.4, 98.5],
            "oxygen_saturation": [97, 96, 97, 98, 97]
        },
        "medications": ["Albuterol", "Fluticasone"],
        "lab_results": {
            "ige": [245],
            "eosinophils": [420]
        }
    },
    "P003": {
        "name": "Robert Johnson",
        "age": 62,
        "gender": "Male",
        "conditions": ["Coronary Artery Disease", "Hyperlipidemia"],
        "vitals": {
            "heart_rate": [65, 68, 64, 67, 66],
            "blood_pressure": ["135/85", "138/87", "132/84", "136/86", "134/85"],
            "temperature": [98.5, 98.6, 98.4, 98.5, 98.5],
            "oxygen_saturation": [96, 95, 96, 97, 96]
        },
        "medications": ["Atorvastatin", "Aspirin", "Metoprolol"],
        "lab_results": {
            "cholesterol": [185],
            "ldl": [110],
            "hdl": [45],
            "triglycerides": [150]
        }
    }
}

# Sample medical knowledge base
knowledge_base = {
    "Hypertension": {
        "description": "High blood pressure condition that can lead to heart disease and stroke.",
        "symptoms": ["Headaches", "Shortness of breath", "Nosebleeds"],
        "treatments": ["ACE inhibitors", "Diuretics", "Beta-blockers"],
        "risk_factors": ["Age", "Family history", "High sodium diet", "Obesity"]
    },
    "Type 2 Diabetes": {
        "description": "Chronic condition affecting how the body metabolizes glucose.",
        "symptoms": ["Increased thirst", "Frequent urination", "Fatigue", "Blurred vision"],
        "treatments": ["Metformin", "Lifestyle changes", "Insulin therapy"],
        "risk_factors": ["Obesity", "Family history", "Age", "Sedentary lifestyle"]
    },
    "Asthma": {
        "description": "Chronic condition affecting the airways in the lungs.",
        "symptoms": ["Wheezing", "Shortness of breath", "Chest tightness", "Coughing"],
        "treatments": ["Bronchodilators", "Inhaled corticosteroids", "Leukotriene modifiers"],
        "risk_factors": ["Allergies", "Family history", "Respiratory infections", "Air pollution"]
    },
    "Coronary Artery Disease": {
        "description": "Narrowing or blockage of the coronary arteries.",
        "symptoms": ["Chest pain", "Shortness of breath", "Fatigue", "Nausea"],
        "treatments": ["Statins", "Antiplatelet agents", "Beta-blockers", "Lifestyle changes"],
        "risk_factors": ["High cholesterol", "Hypertension", "Smoking", "Diabetes", "Age"]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients', methods=['GET'])
def get_patients():
    patient_list = []
    for id, data in patients.items():
        patient_list.append({
            "id": id,
            "name": data["name"],
            "age": data["age"],
            "gender": data["gender"]
        })
    return jsonify(patient_list)

@app.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    if patient_id in patients:
        return jsonify(patients[patient_id])
    return jsonify({"error": "Patient not found"}), 404

@app.route('/api/knowledge/<condition>', methods=['GET'])
def get_condition_info(condition):
    if condition in knowledge_base:
        return jsonify(knowledge_base[condition])
    return jsonify({"error": "Condition not found"}), 404

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    data = request.json
    patient_id = data.get('patient_id')
    
    if patient_id not in patients:
        return jsonify({"error": "Patient not found"}), 404
    
    patient = patients[patient_id]
    conditions = patient.get('conditions', [])
    
    # Simple analysis based on conditions
    analysis = {
        "patient_name": patient["name"],
        "diagnosis": conditions,
        "risk_factors": [],
        "treatment_recommendations": [],
        "monitoring_recommendations": [],
        "confidence_score": random.uniform(0.85, 0.98),
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add risk factors and treatments based on conditions
    for condition in conditions:
        if condition in knowledge_base:
            analysis["risk_factors"].extend(knowledge_base[condition]["risk_factors"])
            analysis["treatment_recommendations"].extend(knowledge_base[condition]["treatments"])
    
    # Remove duplicates
    analysis["risk_factors"] = list(set(analysis["risk_factors"]))
    analysis["treatment_recommendations"] = list(set(analysis["treatment_recommendations"]))
    
    # Add monitoring recommendations based on conditions
    if "Hypertension" in conditions:
        analysis["monitoring_recommendations"].append("Monitor blood pressure daily")
    if "Type 2 Diabetes" in conditions:
        analysis["monitoring_recommendations"].append("Check blood glucose levels regularly")
    if "Asthma" in conditions:
        analysis["monitoring_recommendations"].append("Track peak flow measurements")
    if "Coronary Artery Disease" in conditions:
        analysis["monitoring_recommendations"].append("Regular ECG monitoring")
    
    # Add AI-generated insights
    analysis["ai_insights"] = generate_ai_insights(patient)
    
    return jsonify(analysis)

@app.route('/api/realtime/<patient_id>', methods=['GET'])
def get_realtime_data(patient_id):
    """Generate simulated real-time patient data"""
    if patient_id not in patients:
        return jsonify({"error": "Patient not found"}), 404
    
    patient = patients[patient_id]
    conditions = patient.get('conditions', [])
    
    # Get the last recorded vitals
    last_hr = patient['vitals']['heart_rate'][-1]
    last_bp = patient['vitals']['blood_pressure'][-1]
    last_temp = patient['vitals']['temperature'][-1]
    last_o2 = patient['vitals']['oxygen_saturation'][-1]
    
    # Simulate small changes in vitals
    new_hr = max(40, min(180, last_hr + random.uniform(-5, 5)))
    
    # Parse last BP
    systolic, diastolic = map(int, last_bp.split('/'))
    new_systolic = max(80, min(200, systolic + random.uniform(-5, 5)))
    new_diastolic = max(40, min(120, diastolic + random.uniform(-3, 3)))
    new_bp = f"{int(new_systolic)}/{int(new_diastolic)}"
    
    new_temp = max(95, min(104, last_temp + random.uniform(-0.3, 0.3)))
    new_o2 = max(80, min(100, last_o2 + random.uniform(-2, 2)))
    
    # Add anomalies based on conditions
    if "Hypertension" in conditions and random.random() < 0.2:
        new_systolic += random.uniform(5, 15)
        new_bp = f"{int(new_systolic)}/{int(new_diastolic)}"
    
    if "Coronary Artery Disease" in conditions and random.random() < 0.15:
        new_hr += random.uniform(10, 20)
    
    if "Asthma" in conditions and random.random() < 0.1:
        new_o2 -= random.uniform(3, 8)
    
    # Create real-time data object
    realtime_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "heart_rate": round(new_hr, 1),
        "blood_pressure": new_bp,
        "temperature": round(new_temp, 1),
        "oxygen_saturation": round(new_o2, 1),
        "alerts": []
    }
    
    # Generate alerts based on abnormal values
    if new_hr > 100:
        realtime_data["alerts"].append({
            "type": "warning",
            "message": "Elevated heart rate detected"
        })
    elif new_hr < 60:
        realtime_data["alerts"].append({
            "type": "warning",
            "message": "Low heart rate detected"
        })
    
    if new_systolic > 140 or new_diastolic > 90:
        realtime_data["alerts"].append({
            "type": "warning",
            "message": "Elevated blood pressure detected"
        })
    
    if new_temp > 99.5:
        realtime_data["alerts"].append({
            "type": "warning",
            "message": "Elevated temperature detected"
        })
    
    if new_o2 < 95:
        realtime_data["alerts"].append({
            "type": "danger",
            "message": "Low oxygen saturation detected"
        })
    
    return jsonify(realtime_data)

def generate_ai_insights(patient):
    """Generate AI-based insights for the patient"""
    insights = []
    
    # Check for patterns in vitals
    hr_values = patient['vitals']['heart_rate']
    if len(hr_values) >= 3:
        if all(hr > 85 for hr in hr_values[-3:]):
            insights.append({
                "type": "pattern",
                "message": "Consistently elevated heart rate detected over multiple readings",
                "confidence": 0.92
            })
    
    # Check lab results
    if 'lab_results' in patient:
        if 'glucose' in patient['lab_results']:
            glucose_values = patient['lab_results']['glucose']
            if any(g > 125 for g in glucose_values):
                insights.append({
                    "type": "lab",
                    "message": "Elevated glucose levels may indicate poor glycemic control",
                    "confidence": 0.89
                })
        
        if 'cholesterol' in patient['lab_results']:
            chol_values = patient['lab_results']['cholesterol']
            if any(c > 200 for c in chol_values):
                insights.append({
                    "type": "lab",
                    "message": "Elevated cholesterol levels detected; consider lipid management therapy",
                    "confidence": 0.94
                })
    
    # Check for medication interactions
    medications = patient.get('medications', [])
    if len(medications) >= 2:
        insights.append({
            "type": "medication",
            "message": f"Multiple medications detected ({', '.join(medications)}). Monitor for potential interactions.",
            "confidence": 0.87
        })
    
    # Add a random insight based on conditions
    conditions = patient.get('conditions', [])
    if conditions:
        condition = random.choice(conditions)
        if condition == "Hypertension":
            insights.append({
                "type": "lifestyle",
                "message": "Consider DASH diet to help manage hypertension",
                "confidence": 0.91
            })
        elif condition == "Type 2 Diabetes":
            insights.append({
                "type": "lifestyle",
                "message": "Regular physical activity may improve insulin sensitivity",
                "confidence": 0.93
            })
        elif condition == "Asthma":
            insights.append({
                "type": "environmental",
                "message": "Monitor air quality index to prevent asthma exacerbations",
                "confidence": 0.88
            })
        elif condition == "Coronary Artery Disease":
            insights.append({
                "type": "risk",
                "message": "Stress management techniques may reduce cardiovascular risk",
                "confidence": 0.85
            })
    
    return insights

# Sample medical images data
medical_images = {
    "P001": [
        {
            "id": "IMG001",
            "type": "X-Ray",
            "body_part": "Chest",
            "date": "2025-04-10",
            "findings": "No significant abnormalities detected",
            "url": "/static/images/chest_xray.jpg"
        }
    ],
    "P002": [
        {
            "id": "IMG002",
            "type": "MRI",
            "body_part": "Brain",
            "date": "2025-03-22",
            "findings": "Normal brain structure, no lesions detected",
            "url": "/static/images/brain_mri.jpg"
        }
    ],
    "P003": [
        {
            "id": "IMG003",
            "type": "CT Scan",
            "body_part": "Chest",
            "date": "2025-05-01",
            "findings": "Mild coronary calcification consistent with CAD diagnosis",
            "url": "/static/images/chest_ct.jpg"
        }
    ]
}

@app.route('/api/images/<patient_id>', methods=['GET'])
def get_patient_images(patient_id):
    """Get medical images for a patient"""
    if patient_id not in medical_images:
        return jsonify([])
    return jsonify(medical_images[patient_id])

@app.route('/api/analyze/image', methods=['POST'])
def analyze_medical_image():
    """Simulate AI analysis of a medical image"""
    data = request.json
    image_id = data.get('image_id')
    
    # Find the image
    image_data = None
    for patient_id, images in medical_images.items():
        for image in images:
            if image['id'] == image_id:
                image_data = image
                break
        if image_data:
            break
    
    if not image_data:
        return jsonify({"error": "Image not found"}), 404
    
    # Simulate AI analysis based on image type
    analysis_result = {
        "image_id": image_id,
        "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confidence_score": random.uniform(0.82, 0.97),
        "findings": [],
        "recommendations": []
    }
    
    if image_data['type'] == 'X-Ray' and image_data['body_part'] == 'Chest':
        analysis_result['findings'] = [
            {
                "description": "Lung fields appear clear",
                "confidence": 0.95,
                "location": "Bilateral lung fields"
            },
            {
                "description": "No evidence of consolidation or effusion",
                "confidence": 0.93,
                "location": "Bilateral lung fields"
            },
            {
                "description": "Heart size within normal limits",
                "confidence": 0.97,
                "location": "Cardiac silhouette"
            }
        ]
        analysis_result['recommendations'] = [
            "No further imaging required at this time",
            "Recommend follow-up X-ray in 12 months"
        ]
    
    elif image_data['type'] == 'MRI' and image_data['body_part'] == 'Brain':
        analysis_result['findings'] = [
            {
                "description": "No evidence of acute infarction",
                "confidence": 0.94,
                "location": "Entire brain"
            },
            {
                "description": "No mass effect or midline shift",
                "confidence": 0.96,
                "location": "Entire brain"
            },
            {
                "description": "Ventricles normal in size and configuration",
                "confidence": 0.95,
                "location": "Ventricular system"
            }
        ]
        analysis_result['recommendations'] = [
            "No further imaging required at this time",
            "Clinical correlation recommended"
        ]
    
    elif image_data['type'] == 'CT Scan' and image_data['body_part'] == 'Chest':
        analysis_result['findings'] = [
            {
                "description": "Mild coronary artery calcification",
                "confidence": 0.91,
                "location": "Coronary arteries"
            },
            {
                "description": "No pulmonary nodules or masses",
                "confidence": 0.89,
                "location": "Lung parenchyma"
            },
            {
                "description": "No pleural effusion",
                "confidence": 0.94,
                "location": "Pleural space"
            }
        ]
        analysis_result['recommendations'] = [
            "Consider cardiac risk assessment",
            "Follow-up with cardiologist recommended"
        ]
    
    return jsonify(analysis_result)

@app.route('/api/predict/progression/<patient_id>', methods=['GET'])
def predict_disease_progression(patient_id):
    """Predict disease progression for a patient"""
    if patient_id not in patients:
        return jsonify({"error": "Patient not found"}), 404
    
    patient = patients[patient_id]
    conditions = patient.get('conditions', [])
    
    if not conditions:
        return jsonify({"error": "No conditions to predict progression for"}), 400
    
    # Generate predictions for each condition
    predictions = []
    
    for condition in conditions:
        prediction = {
            "condition": condition,
            "time_horizon": "6 months",
            "prediction_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "confidence": random.uniform(0.75, 0.92),
            "trajectory": random.choice(["stable", "improving", "worsening"]),
            "risk_factors": [],
            "recommendations": []
        }
        
        # Add condition-specific predictions
        if condition == "Hypertension":
            prediction["risk_factors"] = ["Sodium intake", "Stress levels", "Medication adherence"]
            prediction["key_metrics"] = {
                "current_bp": patient['vitals']['blood_pressure'][-1],
                "target_bp": "120/80",
                "probability_of_reaching_target": random.uniform(0.6, 0.8)
            }
            prediction["recommendations"] = [
                "Continue current medication regimen",
                "Reduce sodium intake to <2g per day",
                "Implement stress reduction techniques"
            ]
        
        elif condition == "Type 2 Diabetes":
            prediction["risk_factors"] = ["Dietary habits", "Physical activity", "Weight management"]
            prediction["key_metrics"] = {
                "current_hba1c": patient['lab_results'].get('hba1c', [6.8])[-1],
                "target_hba1c": "<6.5%",
                "probability_of_reaching_target": random.uniform(0.5, 0.75)
            }
            prediction["recommendations"] = [
                "Maintain carbohydrate-controlled diet",
                "Increase physical activity to 150 minutes per week",
                "Monitor blood glucose levels daily"
            ]
        
        elif condition == "Asthma":
            prediction["risk_factors"] = ["Environmental triggers", "Seasonal allergies", "Medication adherence"]
            prediction["key_metrics"] = {
                "current_o2": patient['vitals']['oxygen_saturation'][-1],
                "exacerbation_risk": random.choice(["low", "moderate", "high"]),
                "probability_of_exacerbation": random.uniform(0.1, 0.4)
            }
            prediction["recommendations"] = [
                "Continue current inhaler regimen",
                "Avoid known triggers",
                "Consider allergy testing"
            ]
        
        elif condition == "Coronary Artery Disease":
            prediction["risk_factors"] = ["Lipid levels", "Blood pressure control", "Physical activity"]
            prediction["key_metrics"] = {
                "current_cholesterol": patient['lab_results'].get('cholesterol', [185])[-1],
                "target_ldl": "<100 mg/dL",
                "probability_of_cardiac_event": random.uniform(0.05, 0.2)
            }
            prediction["recommendations"] = [
                "Continue statin therapy",
                "Maintain blood pressure control",
                "Cardiac rehabilitation program"
            ]
        
        predictions.append(prediction)
    
    return jsonify(predictions)

if __name__ == '__main__':
    # Create directories if they don't exist
    for directory in ['templates', 'static/images']:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Create placeholder images for demo
    placeholder_images = {
        'chest_xray.jpg': (300, 250),
        'brain_mri.jpg': (300, 250),
        'chest_ct.jpg': (300, 250)
    }
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        for img_name, size in placeholder_images.items():
            img_path = os.path.join('static/images', img_name)
            if not os.path.exists(img_path):
                # Create a placeholder image with text
                img = Image.new('RGB', size, color=(240, 240, 240))
                d = ImageDraw.Draw(img)
                d.rectangle([0, 0, size[0]-1, size[1]-1], outline=(200, 200, 200))
                d.text((size[0]//2-50, size[1]//2), f"MedNexus AI\n{img_name}", fill=(100, 100, 100))
                img.save(img_path)
                print(f"Created placeholder image: {img_path}")
    except ImportError:
        print("PIL not available, skipping image creation")
    
    app.run(host='0.0.0.0', port=8080, debug=True)