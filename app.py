from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from model import SecurityModel
from database import db
from auth import login_required, register_user, login_user
from report_generator import generate_pdf_report
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize ML Model
print("🚀 Loading ML Model...")
security_model = SecurityModel()
print("✅ Model loaded successfully!")

# ==========================================
# PUBLIC ROUTES (No authentication required)
# ==========================================

@app.route('/')
def home():
    return jsonify({
        "message": "AI Security Dashboard API - Day 3",
        "status": "Live",
        "version": "3.0.0",
        "features": ["User Auth", "Scan History", "PDF Reports", "Database Storage"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": security_model.model is not None,
        "database": "connected",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Get global statistics from database"""
    stats_data = db.get_stats()
    return jsonify({
        **stats_data,
        "last_updated": datetime.now().isoformat()
    })

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    result = register_user(
        data['username'],
        data.get('email', ''),
        data['password']
    )
    
    if result['success']:
        return jsonify({
            'message': 'User registered successfully',
            'user_id': result['user_id']
        }), 201
    else:
        return jsonify({'error': result['error']}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    result = login_user(data['username'], data['password'])
    
    if result['success']:
        return jsonify({
            'message': 'Login successful',
            'token': result['token'],
            'user': result['user']
        })
    else:
        return jsonify({'error': result['error']}), 401

# ==========================================
# PROTECTED ROUTES (Authentication required)
# ==========================================

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                "error": "Please provide 'features' array with 10 numerical values (0-1)"
            }), 400
        
        features = data['features']
        
        if not isinstance(features, list) or len(features) != 10:
            return jsonify({
                "error": f"Features must be array of exactly 10 values"
            }), 400
        
        try:
            features = [float(f) for f in features]
        except:
            return jsonify({"error": "All features must be numbers"}), 400
        
        # Prediction
        result = security_model.predict(features)
        
        # Save to database
        scan_id = db.save_scan(
            user_id=request.user_id,
            features=features,
            prediction=result['prediction'],
            confidence=result['confidence'],
            risk_score=result['risk_score'],
            model_version="3.0.0"
        )
        
        # Add metadata
        result['scan_id'] = scan_id
        result['timestamp'] = datetime.now().isoformat()
        result['input_features'] = features
        result['model_version'] = "3.0.0"
        result['status'] = "success"
        result['saved_to_history'] = True
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/history', methods=['GET'])
@login_required
def history():
    """Get user's scan history"""
    scans = db.get_user_scans(request.user_id)
    return jsonify({
        "scans": scans,
        "total": len(scans),
        "user": request.username
    })

@app.route('/api/report/<int:scan_id>', methods=['GET'])
@login_required
def download_report(scan_id):
    """Download PDF report for a scan"""
    # Get scan from database
    scans = db.get_user_scans(request.user_id)
    scan = next((s for s in scans if s['id'] == scan_id), None)
    
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
    
    # Generate PDF
    user_info = {'username': request.username}
    pdf_buffer = generate_pdf_report(scan, user_info)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'security_report_{scan_id}.pdf'
    )

@app.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Get complete dashboard data for user"""
    scans = db.get_user_scans(request.user_id, limit=10)
    stats_data = db.get_stats()
    
    # Calculate user-specific stats
    user_high_risk = sum(1 for s in scans if s['prediction'] == 1)
    user_low_risk = sum(1 for s in scans if s['prediction'] == 0)
    
    return jsonify({
        "user": request.username,
        "recent_scans": scans,
        "global_stats": stats_data,
        "user_stats": {
            "total_scans": len(scans),
            "high_risk": user_high_risk,
            "low_risk": user_low_risk
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Starting Day 3 Server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)






  