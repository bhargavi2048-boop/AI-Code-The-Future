# AI Code The Future.py - Complete Fixed Version
import os
import re
import fitz  # PyMuPDF
import spacy
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import json
from datetime import timedelta
import nltk
from nltk.tokenize import sent_tokenize
import secrets
import random

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = {
    'technical': ['python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb', 
                  'aws', 'docker', 'kubernetes', 'machine learning', 'data analysis',
                  'html', 'css', 'git', 'agile', 'scrum', 'rest api', 'graphql',
                  'typescript', 'angular', 'vue', 'django', 'flask', 'spring',
                  'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'rust', 'go'],
    'soft': ['leadership', 'communication', 'teamwork', 'problem solving', 'time management',
             'critical thinking', 'adaptability', 'creativity', 'emotional intelligence',
             'conflict resolution', 'negotiation', 'presentation', 'mentoring'],
    'tools': ['jira', 'confluence', 'slack', 'microsoft office', 'excel', 'tableau',
              'power bi', 'photoshop', 'figma', 'sketch', 'jenkins', 'gitlab',
              'github', 'bitbucket', 'trello', 'asana', 'notion']
}

# HTML Templates as strings
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Analyzer Pro - AI-Powered Resume Analysis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --teal-blue: #008080;
            --teal-light: #20b2aa;
            --teal-dark: #006666;
            --teal-soft: #e0f2f1;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .navbar {
            background-color: var(--teal-blue) !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: bold;
            color: white !important;
            font-size: 1.5rem;
        }
        
        .nav-link {
            color: rgba(255,255,255,0.9) !important;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .nav-link:hover {
            color: white !important;
            transform: translateY(-2px);
        }
        
        .btn-teal {
            background-color: var(--teal-blue);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-teal:hover {
            background-color: var(--teal-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,128,128,0.3);
            color: white;
        }
        
        .btn-outline-teal {
            background-color: transparent;
            color: var(--teal-blue);
            border: 2px solid var(--teal-blue);
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-outline-teal:hover {
            background-color: var(--teal-blue);
            color: white;
            transform: translateY(-2px);
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--teal-blue), var(--teal-light));
            color: white;
            font-weight: bold;
            padding: 15px 20px;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            color: var(--teal-blue);
            margin-bottom: 15px;
        }
        
        .score-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--teal-blue), var(--teal-light));
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            color: white;
            font-size: 2.5rem;
            font-weight: bold;
            box-shadow: 0 10px 20px rgba(0,128,128,0.3);
        }
        
        .section-title {
            color: var(--teal-dark);
            font-weight: bold;
            margin-bottom: 20px;
            position: relative;
            padding-bottom: 10px;
        }
        
        .section-title:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 50px;
            height: 3px;
            background: var(--teal-blue);
        }
        
        .badge-skill {
            background-color: var(--teal-soft);
            color: var(--teal-dark);
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 500;
            margin: 5px;
            display: inline-block;
            border: 1px solid var(--teal-light);
        }
        
        .progress-teal {
            background-color: var(--teal-soft);
            height: 10px;
            border-radius: 5px;
        }
        
        .progress-bar-teal {
            background: linear-gradient(90deg, var(--teal-blue), var(--teal-light));
            border-radius: 5px;
        }
        
        .footer {
            background-color: var(--teal-dark);
            color: white;
            padding: 20px 0;
            margin-top: 50px;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-fadeInUp {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .min-vh-75 {
            min-height: 75vh;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-file-alt me-2"></i>Resume Analyzer Pro
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/get-started">Get Started</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main>
        <div class="container mt-5">
            <div class="row align-items-center min-vh-75">
                <div class="col-lg-6 animate-fadeInUp">
                    <h1 class="display-4 fw-bold mb-4" style="color: var(--teal-dark);">
                        Transform Your Resume with AI Power
                    </h1>
                    <p class="lead mb-4 text-secondary">
                        Get instant, AI-powered analysis of your resume. Identify gaps, improve impact, 
                        and align with your dream job in minutes.
                    </p>
                    <div class="mb-4">
                        <div class="d-flex align-items-center mb-3">
                            <i class="fas fa-check-circle me-3" style="color: var(--teal-blue); font-size: 1.5rem;"></i>
                            <span class="fs-5">Extract key skills and projects automatically</span>
                        </div>
                        <div class="d-flex align-items-center mb-3">
                            <i class="fas fa-check-circle me-3" style="color: var(--teal-blue); font-size: 1.5rem;"></i>
                            <span class="fs-5">Get a detailed resume score out of 10</span>
                        </div>
                        <div class="d-flex align-items-center mb-3">
                            <i class="fas fa-check-circle me-3" style="color: var(--teal-blue); font-size: 1.5rem;"></i>
                            <span class="fs-5">Receive AI-generated professional summary</span>
                        </div>
                        <div class="d-flex align-items-center mb-3">
                            <i class="fas fa-check-circle me-3" style="color: var(--teal-blue); font-size: 1.5rem;"></i>
                            <span class="fs-5">Compare with job descriptions for better alignment</span>
                        </div>
                    </div>
                    <a href="/get-started" class="btn btn-teal btn-lg px-5 py-3">
                        Get Started <i class="fas fa-arrow-right ms-2"></i>
                    </a>
                </div>
                <div class="col-lg-6 animate-fadeInUp" style="animation-delay: 0.2s;">
                    <div class="card p-4">
                        <div class="text-center p-5">
                            <i class="fas fa-chart-pie fa-6x" style="color: var(--teal-blue);"></i>
                            <h3 class="mt-4">AI-Powered Analysis Dashboard</h3>
                            <p class="text-secondary">Comprehensive insights in seconds</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-5 pt-5">
                <h2 class="text-center section-title mb-5">Why Choose Resume Analyzer Pro?</h2>
                
                <div class="col-md-4 mb-4">
                    <div class="card h-100 text-center p-4">
                        <div class="feature-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <h4 class="fw-bold mb-3">AI-Powered Analysis</h4>
                        <p class="text-secondary">Advanced AI algorithms analyze your resume against industry standards and job requirements.</p>
                    </div>
                </div>
                
                <div class="col-md-4 mb-4">
                    <div class="card h-100 text-center p-4">
                        <div class="feature-icon">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <h4 class="fw-bold mb-3">Real-time Scoring</h4>
                        <p class="text-secondary">Get instant feedback with a comprehensive score out of 10 for clarity and impact.</p>
                    </div>
                </div>
                
                <div class="col-md-4 mb-4">
                    <div class="card h-100 text-center p-4">
                        <div class="feature-icon">
                            <i class="fas fa-magic"></i>
                        </div>
                        <h4 class="fw-bold mb-3">Smart Suggestions</h4>
                        <p class="text-secondary">Receive actionable recommendations to improve each section of your resume.</p>
                    </div>
                </div>
            </div>

            <div class="row mt-5">
                <div class="col-12">
                    <div class="card p-5 text-center" style="background: linear-gradient(135deg, var(--teal-blue), var(--teal-light));">
                        <h2 class="text-white mb-4">Ready to Transform Your Resume?</h2>
                        <p class="text-white mb-4 fs-5">Join thousands of professionals who have improved their resumes with our AI-powered analysis.</p>
                        <div>
                            <a href="/get-started" class="btn btn-light btn-lg px-5 py-3" style="color: var(--teal-blue); font-weight: bold;">
                                Start Analysis Now <i class="fas fa-arrow-right ms-2"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container text-center">
            <p class="mb-0">&copy; 2026 Resume Analyzer Pro. All rights reserved. | www.unsaidtalks.com</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

GET_STARTED_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Started - Resume Analyzer Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --teal-blue: #008080;
            --teal-light: #20b2aa;
            --teal-dark: #006666;
            --teal-soft: #e0f2f1;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .navbar {
            background-color: var(--teal-blue) !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: bold;
            color: white !important;
            font-size: 1.5rem;
        }
        
        .nav-link {
            color: rgba(255,255,255,0.9) !important;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .nav-link:hover {
            color: white !important;
            transform: translateY(-2px);
        }
        
        .btn-teal {
            background-color: var(--teal-blue);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-teal:hover {
            background-color: var(--teal-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,128,128,0.3);
            color: white;
        }
        
        .btn-outline-teal {
            background-color: transparent;
            color: var(--teal-blue);
            border: 2px solid var(--teal-blue);
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-outline-teal:hover {
            background-color: var(--teal-blue);
            color: white;
            transform: translateY(-2px);
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--teal-blue), var(--teal-light));
            color: white;
            font-weight: bold;
            padding: 15px 20px;
        }
        
        .score-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--teal-blue), var(--teal-light));
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            box-shadow: 0 10px 20px rgba(0,128,128,0.3);
        }
        
        .footer {
            background-color: var(--teal-dark);
            color: white;
            padding: 20px 0;
            margin-top: 50px;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animate-fadeInUp {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .upload-area {
            transition: all 0.3s;
            cursor: pointer;
            border: 3px dashed var(--teal-blue) !important;
            background-color: var(--teal-soft);
        }
        
        .upload-area:hover {
            background-color: #c8e6e3 !important;
            border-color: var(--teal-dark) !important;
        }
        
        .loading-spinner {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.9);
            z-index: 9999;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        
        .spinner-teal {
            width: 60px;
            height: 60px;
            border: 5px solid var(--teal-soft);
            border-top: 5px solid var(--teal-blue);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-file-alt me-2"></i>Resume Analyzer Pro
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/get-started">Get Started</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="loading-spinner" id="loadingSpinner">
        <div class="spinner-teal mb-3"></div>
        <h4 class="text-teal">Analyzing your resume...</h4>
        <p class="text-muted">This may take a few moments</p>
    </div>

    <main>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-lg-8 animate-fadeInUp">
                    <div class="card">
                        <div class="card-header">
                            <h3 class="mb-0"><i class="fas fa-rocket me-2"></i>Get Started with Resume Analysis</h3>
                        </div>
                        <div class="card-body p-5">
                            <div class="text-center mb-5">
                                <div class="score-circle mb-4">
                                    <i class="fas fa-file-pdf"></i>
                                </div>
                                <h4 class="fw-bold">Upload Your Resume</h4>
                                <p class="text-secondary">We support PDF format only. Maximum file size: 16MB</p>
                            </div>

                            <form action="/analyze" method="post" enctype="multipart/form-data" id="uploadForm">
                                <div class="upload-area mb-4 p-5 text-center border rounded-3" id="dropArea">
                                    <i class="fas fa-cloud-upload-alt fa-4x mb-3" style="color: var(--teal-blue);"></i>
                                    <h5 class="mb-2">Drag & Drop your resume here</h5>
                                    <p class="text-muted mb-3">or</p>
                                    <button type="button" class="btn btn-outline-teal" onclick="document.getElementById('fileInput').click()">
                                        Browse Files
                                    </button>
                                    <input type="file" id="fileInput" name="resume" accept=".pdf" style="display: none;" required>
                                    <div id="fileName" class="mt-3 text-success fw-bold"></div>
                                </div>

                                <div class="mb-4">
                                    <h5 class="fw-bold mb-3">Job Details (Optional)</h5>
                                    <p class="text-muted small mb-3">Adding a job description helps us provide better alignment analysis</p>
                                    
                                    <div class="mb-3">
                                        <label class="form-label fw-bold">Target Job Title</label>
                                        <input type="text" class="form-control form-control-lg" name="job_title" 
                                               placeholder="e.g., Senior Software Engineer">
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label class="form-label fw-bold">Job Description</label>
                                        <textarea class="form-control" name="job_description" rows="5" 
                                                  placeholder="Paste the job description here..."></textarea>
                                    </div>
                                </div>

                                <div class="d-grid gap-2">
                                    <button type="submit" class="btn btn-teal btn-lg" id="submitBtn">
                                        <i class="fas fa-search me-2"></i>Analyze Resume
                                    </button>
                                </div>
                            </form>

                            <div class="mt-5">
                                <h5 class="fw-bold mb-3">What you'll get:</h5>
                                <div class="row">
                                    <div class="col-md-6">
                                        <ul class="list-unstyled">
                                            <li class="mb-2"><i class="fas fa-check-circle me-2" style="color: var(--teal-blue);"></i>Skills extraction</li>
                                            <li class="mb-2"><i class="fas fa-check-circle me-2" style="color: var(--teal-blue);"></i>Project analysis</li>
                                            <li class="mb-2"><i class="fas fa-check-circle me-2" style="color: var(--teal-blue);"></i>Resume score (out of 10)</li>
                                        </ul>
                                    </div>
                                    <div class="col-md-6">
                                        <ul class="list-unstyled">
                                            <li class="mb-2"><i class="fas fa-check-circle me-2" style="color: var(--teal-blue);"></i>Improvement suggestions</li>
                                            <li class="mb-2"><i class="fas fa-check-circle me-2" style="color: var(--teal-blue);"></i>Professional summary</li>
                                            <li class="mb-2"><i class="fas fa-check-circle me-2" style="color: var(--teal-blue);"></i>Job alignment analysis</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container text-center">
            <p class="mb-0">&copy; 2026 Resume Analyzer Pro. All rights reserved. | www.unsaidtalks.com</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                document.getElementById('fileName').textContent = 'Selected: ' + fileName;
            }
        });

        document.getElementById('dropArea').addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.backgroundColor = '#c8e6e3';
        });

        document.getElementById('dropArea').addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.backgroundColor = 'var(--teal-soft)';
        });

        document.getElementById('dropArea').addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.backgroundColor = 'var(--teal-soft)';
            
            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].type === 'application/pdf') {
                document.getElementById('fileInput').files = files;
                document.getElementById('fileName').textContent = 'Selected: ' + files[0].name;
            } else {
                alert('Please drop a PDF file');
            }
        });

        document.getElementById('uploadForm').addEventListener('submit', function() {
            document.getElementById('loadingSpinner').style.display = 'flex';
        });
    </script>
</body>
</html>
'''

# Fixed RESULTS_TEMPLATE - Removed all 'min' function calls
RESULTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Results - Resume Analyzer Pro</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --teal-blue: #008080;
            --teal-light: #20b2aa;
            --teal-dark: #006666;
            --teal-soft: #e0f2f1;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .navbar {
            background-color: var(--teal-blue) !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: bold;
            color: white !important;
            font-size: 1.5rem;
        }
        
        .nav-link {
            color: rgba(255,255,255,0.9) !important;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .nav-link:hover {
            color: white !important;
            transform: translateY(-2px);
        }
        
        .btn-teal {
            background-color: var(--teal-blue);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-teal:hover {
            background-color: var(--teal-dark);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,128,128,0.3);
            color: white;
        }
        
        .btn-outline-teal {
            background-color: transparent;
            color: var(--teal-blue);
            border: 2px solid var(--teal-blue);
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .btn-outline-teal:hover {
            background-color: var(--teal-blue);
            color: white;
            transform: translateY(-2px);
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            overflow: hidden;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--teal-blue), var(--teal-light));
            color: white;
            font-weight: bold;
            padding: 15px 20px;
        }
        
        .score-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--teal-blue), var(--teal-light));
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            color: white;
            font-size: 3rem;
            font-weight: bold;
            box-shadow: 0 10px 20px rgba(0,128,128,0.3);
        }
        
        .section-title {
            color: var(--teal-dark);
            font-weight: bold;
            margin-bottom: 20px;
            position: relative;
            padding-bottom: 10px;
        }
        
        .section-title:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 50px;
            height: 3px;
            background: var(--teal-blue);
        }
        
        .badge-skill {
            background-color: var(--teal-soft);
            color: var(--teal-dark);
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 500;
            margin: 5px;
            display: inline-block;
            border: 1px solid var(--teal-light);
        }
        
        .footer {
            background-color: var(--teal-dark);
            color: white;
            padding: 20px 0;
            margin-top: 50px;
        }
        
        .suggestion-item {
            background-color: #f8f9fa;
            border-left: 4px solid var(--teal-blue);
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
        }
        
        .priority-high {
            border-left-color: #dc3545;
        }
        
        .priority-medium {
            border-left-color: #ffc107;
        }
        
        .skill-tag {
            background-color: var(--teal-soft);
            color: var(--teal-dark);
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin: 3px;
            display: inline-block;
            border: 1px solid var(--teal-light);
        }
        
        .missing-skill {
            background-color: #f8d7da;
            color: #721c24;
            border-color: #f5c6cb;
        }
        
        .aligned-skill {
            background-color: #d4edda;
            color: #155724;
            border-color: #c3e6cb;
        }
        
        .progress {
            height: 20px;
            border-radius: 10px;
        }
        
        .progress-bar {
            background: linear-gradient(90deg, var(--teal-blue), var(--teal-light));
            border-radius: 10px;
        }
        
        .summary-card {
            background-color: var(--teal-soft);
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid var(--teal-blue);
        }
        
        .improvement-task {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }
        
        .quality-badge {
            background-color: #17a2b8;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-file-alt me-2"></i>Resume Analyzer Pro
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/get-started">New Analysis</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main>
        <div class="container mt-5">
            <!-- Score Overview -->
            <div class="row mb-5">
                <div class="col-md-4">
                    <div class="card text-center p-4">
                        <div class="score-circle mb-3">
                            {{ analysis.score }}/10
                        </div>
                        <h4>Overall Score</h4>
                        <p class="text-muted">Resume Clarity & Impact</p>
                        {% if analysis.score < 5 %}
                            <span class="badge bg-danger">Needs Improvement</span>
                        {% elif analysis.score < 7 %}
                            <span class="badge bg-warning">Good</span>
                        {% elif analysis.score < 9 %}
                            <span class="badge bg-success">Very Good</span>
                        {% else %}
                            <span class="badge bg-primary">Excellent</span>
                        {% endif %}
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card p-4">
                        <h4 class="mb-3">Score Breakdown</h4>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between mb-2">
                                <span>Skills Coverage</span>
                                <span>{{ analysis.skills|length }}/10+ skills</span>
                            </div>
                            <div class="progress">
                                {% set skills_width = analysis.skills|length * 10 %}
                                {% if skills_width > 100 %}{% set skills_width = 100 %}{% endif %}
                                <div class="progress-bar" style="width: {{ skills_width }}%"></div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between mb-2">
                                <span>Project Quality</span>
                                <span>
                                    {% set quality_projects = [] %}
                                    {% for project in analysis.projects %}
                                        {% if project.quality_score >= 7 %}
                                            {% set quality_projects = quality_projects.append(project) %}
                                        {% endif %}
                                    {% endfor %}
                                    {{ quality_projects|length }}/3+ quality projects
                                </span>
                            </div>
                            <div class="progress">
                                {% set project_width = quality_projects|length * 33 %}
                                {% if project_width > 100 %}{% set project_width = 100 %}{% endif %}
                                <div class="progress-bar" style="width: {{ project_width }}%"></div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="d-flex justify-content-between mb-2">
                                <span>Format & Clarity</span>
                                <span>{% if analysis.score > 7 %}Good{% else %}Needs Work{% endif %}</span>
                            </div>
                            <div class="progress">
                                <div class="progress-bar" style="width: {{ analysis.score * 10 }}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Professional Summary -->
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="mb-0"><i class="fas fa-user-tie me-2"></i>Professional Summary</h4>
                        </div>
                        <div class="card-body">
                            <div class="summary-card">
                                <p class="fs-5 mb-0">{{ analysis.professional_summary }}</p>
                            </div>
                            <div class="mt-3">
                                <button class="btn btn-outline-teal btn-sm me-2" onclick="regenerateSummary()">
                                    <i class="fas fa-sync-alt me-1"></i>Regenerate
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Skills Section -->
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="mb-0"><i class="fas fa-code me-2"></i>Extracted Skills</h4>
                        </div>
                        <div class="card-body">
                            {% if analysis.skills %}
                                {% for skill in analysis.skills %}
                                    <span class="badge-skill">
                                        {{ skill.name }}
                                        <small class="text-muted">({{ skill.category }})</small>
                                    </span>
                                {% endfor %}
                            {% else %}
                                <p class="text-muted">No skills detected. Consider adding more technical skills to your resume.</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Projects Analysis -->
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="mb-0"><i class="fas fa-project-diagram me-2"></i>Projects Analysis</h4>
                        </div>
                        <div class="card-body">
                            {% if analysis.projects %}
                                {% for project in analysis.projects %}
                                    <div class="mb-4 pb-3 border-bottom">
                                        <p class="fw-bold mb-2">Project {{ loop.index }}</p>
                                        <p>{{ project.description }}</p>
                                        <div class="row">
                                            <div class="col-md-3">
                                                <span class="badge {% if project.has_action_words %}bg-success{% else %}bg-warning{% endif %} me-2">
                                                    Action Words: {{ '✓' if project.has_action_words else '✗' }}
                                                </span>
                                            </div>
                                            <div class="col-md-3">
                                                <span class="badge {% if project.has_technologies %}bg-success{% else %}bg-warning{% endif %} me-2">
                                                    Technologies: {{ '✓' if project.has_technologies else '✗' }}
                                                </span>
                                            </div>
                                            <div class="col-md-3">
                                                <span class="badge {% if project.has_impact %}bg-success{% else %}bg-warning{% endif %} me-2">
                                                    Impact: {{ '✓' if project.has_impact else '✗' }}
                                                </span>
                                            </div>
                                            <div class="col-md-3">
                                                <span class="badge bg-info">Quality: {{ project.quality_score }}/10</span>
                                            </div>
                                        </div>
                                    </div>
                                {% endfor %}
                            {% else %}
                                <p class="text-muted">No projects detected. Consider adding project descriptions to your resume.</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Job Description Comparison -->
            {% if analysis.jd_comparison %}
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="mb-0"><i class="fas fa-briefcase me-2"></i>Job Alignment Analysis</h4>
                        </div>
                        <div class="card-body">
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <h5>Target Job: {{ analysis.job_title or 'Not Specified' }}</h5>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex align-items-center">
                                        <span class="fw-bold me-3">Alignment Score:</span>
                                        <div class="progress flex-grow-1" style="height: 25px;">
                                            {% set align_width = analysis.jd_comparison.alignment_score * 10 %}
                                            {% if align_width > 100 %}{% set align_width = 100 %}{% endif %}
                                            <div class="progress-bar" style="width: {{ align_width }}%">
                                                {{ analysis.jd_comparison.alignment_score }}/10
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-md-6">
                                    <h6 class="fw-bold mb-3">Aligned Skills ({{ analysis.jd_comparison.aligned_skills|length }})</h6>
                                    {% for skill in analysis.jd_comparison.aligned_skills %}
                                        <span class="skill-tag aligned-skill">{{ skill }}</span>
                                    {% endfor %}
                                </div>
                                <div class="col-md-6">
                                    <h6 class="fw-bold mb-3">Missing Skills ({{ analysis.jd_comparison.missing_skills|length }})</h6>
                                    {% for skill in analysis.jd_comparison.missing_skills %}
                                        <span class="skill-tag missing-skill">{{ skill }}</span>
                                    {% endfor %}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            {% endif %}

            <!-- Improvement Suggestions -->
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="mb-0"><i class="fas fa-lightbulb me-2"></i>Improvement Suggestions</h4>
                        </div>
                        <div class="card-body">
                            {% if analysis.suggestions %}
                                {% for suggestion in analysis.suggestions %}
                                    <div class="suggestion-item priority-{{ suggestion.priority }}">
                                        <div class="d-flex justify-content-between align-items-start">
                                            <div>
                                                <h5 class="fw-bold">{{ suggestion.section }}</h5>
                                                <p class="mb-2"><strong>Issue:</strong> {{ suggestion.issue }}</p>
                                                <p class="mb-0"><strong>Suggestion:</strong> {{ suggestion.suggestion }}</p>
                                            </div>
                                            <span class="badge {% if suggestion.priority == 'high' %}bg-danger{% elif suggestion.priority == 'medium' %}bg-warning{% else %}bg-success{% endif %}">
                                                {{ suggestion.priority|upper }} PRIORITY
                                            </span>
                                        </div>
                                    </div>
                                {% endfor %}
                            {% else %}
                                <p class="text-muted">No suggestions available.</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Improvement Tasks -->
            <div class="row mb-5">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h4 class="mb-0"><i class="fas fa-tasks me-2"></i>Improvement Tasks</h4>
                        </div>
                        <div class="card-body">
                            <div class="improvement-task">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="task1" onchange="updateScore(2)">
                                    <label class="form-check-label" for="task1">
                                        <strong>Add missing skills:</strong> Include at least 5 of the missing skills identified in the job comparison.
                                    </label>
                                </div>
                            </div>
                            <div class="improvement-task">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="task2" onchange="updateScore(3)">
                                    <label class="form-check-label" for="task2">
                                        <strong>Improve project descriptions:</strong> Add action verbs and quantify impact for each project.
                                    </label>
                                </div>
                            </div>
                            <div class="improvement-task">
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="task3" onchange="updateScore(2)">
                                    <label class="form-check-label" for="task3">
                                        <strong>Add professional summary:</strong> Include a compelling 2-line summary at the top of your resume.
                                    </label>
                                </div>
                            </div>
                            <div class="mt-4">
                                <button class="btn btn-teal" onclick="reEvaluate()">
                                    <i class="fas fa-sync-alt me-2"></i>Re-evaluate Resume
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container text-center">
            <p class="mb-0">&copy; 2026 Resume Analyzer Pro. All rights reserved. | www.unsaidtalks.com</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentScore = {{ analysis.score }};
        let appliedImprovements = [];

        function updateScore(points) {
            currentScore = Math.min(currentScore + points, 10);
            document.querySelector('.score-circle').innerHTML = currentScore + '/10';
        }

        function regenerateSummary() {
            fetch('/improve', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    regenerate_summary: true,
                    applied: appliedImprovements,
                    improvement_points: 0
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector('.summary-card p').textContent = data.professional_summary;
                }
            });
        }

        function reEvaluate() {
            const improvements = {
                applied: appliedImprovements,
                improvement_points: currentScore - {{ analysis.score }}
            };
            
            fetch('/improve', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(improvements)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.new_score >= 8) {
                    alert('Congratulations! Your resume has improved to ' + data.new_score + '/10!');
                } else if (data.success) {
                    alert('Resume score updated to ' + data.new_score + '/10. Keep working to reach 8+!');
                }
            });
        }

        // Track checkbox changes
        document.querySelectorAll('.form-check-input').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    appliedImprovements.push(this.nextElementSibling.textContent.trim());
                }
            });
        });
    </script>
</body>
</html>
'''

class ResumeAnalyzer:
    def __init__(self):
        self.skills_found = []
        self.projects = []
        self.experience = []
        self.education = []
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        text = ""
        try:
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        seen_skills = set()
        
        # Check for common skills
        for category, skills in COMMON_SKILLS.items():
            for skill in skills:
                if skill.lower() in text_lower and skill.lower() not in seen_skills:
                    seen_skills.add(skill.lower())
                    found_skills.append({
                        'name': skill.title(),
                        'category': category,
                        'context': self.get_skill_context(text, skill)
                    })
        
        # Use NLP to find potential skills
        doc = nlp(text[:5000])
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
                if token.text.lower() not in seen_skills and token.text[0].isupper():
                    seen_skills.add(token.text.lower())
                    found_skills.append({
                        'name': token.text,
                        'category': 'technical',
                        'context': self.get_skill_context(text, token.text)
                    })
        
        return found_skills[:20]
    
    def get_skill_context(self, text, skill, window=100):
        """Get context around where skill appears"""
        skill_index = text.lower().find(skill.lower())
        if skill_index != -1:
            start = max(0, skill_index - window)
            end = min(len(text), skill_index + len(skill) + window)
            return text[start:end].replace('\n', ' ').strip()
        return ""
    
    def extract_projects(self, text):
        """Extract project information"""
        projects = []
        project_patterns = [
            r'project[s]?:?\s*(.+?)(?=\n\n|\n[A-Z]|$)',
            r'(?:developed|created|built|implemented)\s+(.+?)(?=\.|\n)',
            r'(?:project|work)\s+experience[s]?\s*(.+?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in project_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                project_text = match.group(1).strip()
                if len(project_text) > 30:
                    analysis = self.analyze_project_description(project_text)
                    projects.append({
                        'description': project_text[:200] + '...' if len(project_text) > 200 else project_text,
                        'has_action_words': analysis['has_action_words'],
                        'has_technologies': analysis['has_technologies'],
                        'has_impact': analysis['has_impact'],
                        'quality_score': analysis['quality_score']
                    })
        
        return projects[:5]
    
    def analyze_project_description(self, description):
        """Analyze quality of project description"""
        action_words = ['developed', 'created', 'implemented', 'designed', 'built',
                       'led', 'managed', 'achieved', 'improved', 'increased',
                       'decreased', 'reduced', 'launched', 'delivered', 'engineered']
        
        tech_indicators = ['using', 'with', 'in', 'on', 'technology', 'framework',
                          'language', 'platform', 'tool', 'stack', 'built with']
        
        impact_indicators = ['increased', 'decreased', 'improved', 'reduced',
                            'saved', 'generated', 'achieved', 'delivered',
                            'by', 'resulted in', 'leading to']
        
        description_lower = description.lower()
        
        has_action_words = any(word in description_lower for word in action_words)
        has_technologies = any(ind in description_lower for ind in tech_indicators)
        has_impact = any(ind in description_lower for ind in impact_indicators)
        
        quality_score = 0
        if has_action_words:
            quality_score += 3
        if has_technologies:
            quality_score += 3
        if has_impact:
            quality_score += 3
        if len(description.split()) > 15:
            quality_score += 1
            
        return {
            'has_action_words': has_action_words,
            'has_technologies': has_technologies,
            'has_impact': has_impact,
            'quality_score': min(quality_score, 10)
        }
    
    def calculate_resume_score(self, text, skills, projects):
        """Calculate overall resume score out of 10"""
        score = 0
        
        # Skills assessment
        if len(skills) >= 10:
            score += 3
        elif len(skills) >= 5:
            score += 2
        elif len(skills) >= 3:
            score += 1
            
        # Projects assessment
        quality_projects = [p for p in projects if p['quality_score'] >= 7]
        if len(quality_projects) >= 3:
            score += 3
        elif len(quality_projects) >= 2:
            score += 2
        elif len(quality_projects) >= 1:
            score += 1
            
        # Length and completeness
        word_count = len(text.split())
        if word_count > 500:
            score += 2
        elif word_count > 300:
            score += 1
            
        # Formatting and clarity
        if '•' in text or '-' in text or '*' in text:
            score += 1
        if re.search(r'EXPERIENCE|EDUCATION|SKILLS', text, re.IGNORECASE):
            score += 1
            
        return min(score, 10)
    
    def generate_improvement_suggestions(self, resume_data):
        """Generate suggestions for resume improvement"""
        suggestions = []
        
        if len(resume_data['skills']) < 10:
            suggestions.append({
                'section': 'Skills',
                'issue': 'Limited skills listed',
                'suggestion': 'Add more relevant technical and soft skills. Include both hard skills (programming languages, tools) and soft skills (communication, leadership).',
                'priority': 'high'
            })
        
        weak_projects = [p for p in resume_data['projects'] if p['quality_score'] < 7]
        if weak_projects:
            suggestions.append({
                'section': 'Projects',
                'issue': 'Weak project descriptions',
                'suggestion': 'Use action verbs (developed, created, implemented) and quantify your impact. Include technologies used and specific outcomes.',
                'priority': 'high'
            })
        
        if not re.search(r'summary|objective|profile', resume_data['text'][:1000], re.IGNORECASE):
            suggestions.append({
                'section': 'Professional Summary',
                'issue': 'Missing professional summary',
                'suggestion': 'Add a 2-3 line professional summary at the top highlighting your key skills and career goals.',
                'priority': 'medium'
            })
        
        return suggestions
    
    def generate_professional_summary(self, skills, projects):
        """Generate a professional summary"""
        skill_names = [s['name'] for s in skills[:3]]
        skills_text = ', '.join(skill_names) if skill_names else 'various technical and soft skills'
        
        templates = [
            f"Results-driven professional with expertise in {skills_text}. Passionate about leveraging technical skills to solve complex problems and deliver impactful results.",
            f"Dedicated professional with strong background in {skills_text}. Committed to continuous learning and applying best practices to drive project success.",
            f"Experienced practitioner skilled in {skills_text}. Focused on delivering high-quality solutions and collaborating effectively with cross-functional teams."
        ]
        
        return random.choice(templates)
    
    def compare_with_job_description(self, resume_skills, job_description):
        """Compare resume skills with job description requirements"""
        missing_skills = []
        aligned_skills = []
        
        jd_lower = job_description.lower()
        
        jd_skills = []
        for category, skills in COMMON_SKILLS.items():
            for skill in skills:
                if skill.lower() in jd_lower:
                    jd_skills.append(skill.lower())
        
        resume_skill_names = [s['name'].lower() for s in resume_skills]
        
        for required_skill in jd_skills:
            if required_skill in resume_skill_names:
                aligned_skills.append(required_skill.title())
            else:
                missing_skills.append(required_skill.title())
        
        if jd_skills:
            alignment_score = (len(aligned_skills) / len(jd_skills)) * 10
        else:
            alignment_score = 5
        
        return {
            'aligned_skills': aligned_skills[:10],
            'missing_skills': missing_skills[:10],
            'alignment_score': round(alignment_score, 1)
        }

analyzer = ResumeAnalyzer()

@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)

@app.route('/get-started')
def get_started():
    return render_template_string(GET_STARTED_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return redirect(url_for('get_started'))
    
    file = request.files['resume']
    job_title = request.form.get('job_title', '')
    job_description = request.form.get('job_description', '')
    
    if file.filename == '' or not file.filename.endswith('.pdf'):
        return redirect(url_for('get_started'))
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    text = analyzer.extract_text_from_pdf(filepath)
    
    skills = analyzer.extract_skills(text)
    projects = analyzer.extract_projects(text)
    score = analyzer.calculate_resume_score(text, skills, projects)
    suggestions = analyzer.generate_improvement_suggestions({
        'text': text,
        'skills': skills,
        'projects': projects
    })
    
    professional_summary = analyzer.generate_professional_summary(skills, projects)
    
    jd_comparison = None
    if job_description:
        jd_comparison = analyzer.compare_with_job_description(skills, job_description)
    
    session['analysis'] = {
        'skills': skills,
        'projects': projects,
        'score': score,
        'suggestions': suggestions,
        'professional_summary': professional_summary,
        'jd_comparison': jd_comparison,
        'job_title': job_title
    }
    
    os.remove(filepath)
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    analysis = session.get('analysis', {})
    if not analysis:
        return redirect(url_for('get_started'))
    return render_template_string(RESULTS_TEMPLATE, analysis=analysis)

@app.route('/improve', methods=['POST'])
def improve():
    analysis = session.get('analysis', {})
    improvements = request.json
    
    if improvements.get('regenerate_summary'):
        analysis['professional_summary'] = analyzer.generate_professional_summary(
            analysis.get('skills', []),
            analysis.get('projects', [])
        )
    
    current_score = analysis.get('score', 0)
    new_score = min(current_score + improvements.get('improvement_points', 0), 10)
    analysis['score'] = new_score
    session['analysis'] = analysis
    
    return jsonify({
        'success': True,
        'new_score': new_score,
        'professional_summary': analysis.get('professional_summary')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)