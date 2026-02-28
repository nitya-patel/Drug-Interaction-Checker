Project Title

Drug Interaction Checker with Graph-Based Conflict Detection

One-line project description:
An offline, graph-based Drug Interaction Checker that detects medication conflicts, categorizes severity levels, and visualizes risks to enhance prescription safety.

1. Problem Statement
Problem Title

Polypharmacy Drug Interaction Risk Detection

Problem Description

Patients, especially elderly individuals and those with chronic illnesses, often consume multiple medications simultaneously. Polypharmacy increases the risk of drug–drug interactions, contraindications, dosage conflicts, and adverse drug reactions. While large hospital systems may include advanced interaction checking tools, smaller clinics and individual practitioners often lack lightweight, structured, and offline-accessible systems for quick medication conflict evaluation.

Manual reference checking is time-consuming, fragmented, and prone to human error, which can compromise patient safety.

Target Users
General Physicians
Small Clinics
Rural Healthcare Providers
Pharmacists
Medical Students
Telemedicine Practitioners

Existing Gaps
Lack of lightweight offline solutions
Fragmented manual checking methods
Limited visualization of interaction severity
No structured graph-based conflict representation
Reduced accessibility in low-connectivity environments

2. Problem Understanding & Approach
Root Cause Analysis
Polypharmacy leads to exponential pairwise drug interaction possibilities.

Manual cross-referencing is inefficient.
Many tools require internet access or paid subscriptions.
Lack of visual and severity-based risk interpretation.

Solution Strategy
Use a structured local drug interaction dataset.
Implement graph-based pairwise interaction detection.
Categorize interactions by severity level.
Visualize medication conflicts as a graph network.
Ensure complete offline functionality.

3. Proposed Solution
Solution Overview
MediGraph is an offline Drug Interaction Checker that analyzes a list of medications, detects conflicts using structured pairwise matching, categorizes severity levels, and visually represents drug interactions using graph modeling.

Core Idea
Model drugs as nodes and interactions as edges in a graph. Use rule-based logic to detect conflicts and classify severity.

Key Features
Drug–Drug Interaction Detection
Contraindication Identification
Dosage Conflict Flagging
Severity Categorization (Mild / Moderate / Severe / Contraindicated)
Graph-Based Visualization
Offline Operation
Risk Score Generation
Clear Clinical Explanation Output

4. System Architecture
High-Level Flow

User → Frontend → Backend API → Interaction Engine → Local Drug Database → Graph Generator → Response

Architecture Description

User inputs medication list.
Frontend sends request to backend API.
Backend validates input.
Interaction Engine generates pairwise combinations.
Local JSON database is queried.
Conflicts are categorized by severity.
Graph model is generated.
Structured response is returned to frontend.
Results are displayed in table + graph format.

5. Database Design
ER Diagram

ER Diagram Description

Entities:

Drug
Drug_ID
Drug_Name
Max_Dosage
Category
Interaction

Interaction_ID
Drug1_ID
Drug2_ID
Severity
Description

Relationship:
Many-to-Many between Drug and Drug via Interaction

6. Dataset Selected
Dataset Name

Structured Drug Interaction Dataset (Custom Curated)

Source
DrugBank
PubChem
U.S. Food and Drug Administration
World Health Organization

Data Type
JSON structured dataset
Drug metadata
Pairwise interaction records
Severity classification

Selection Reason
Publicly accessible references
Credible medical sources
Suitable for offline structured modeling
Supports graph-based logic

Preprocessing Steps
Standardized drug names
Removed duplicates
Normalized severity levels
Converted dataset to JSON format
Indexed drugs for constant-time lookup

7. Model Selected
Model Name
Graph-Based Rule Engine (Deterministic Pairwise Conflict Detection)

Selection Reasoning
Efficient for polypharmacy pair generation
Deterministic and interpretable
Suitable for offline implementation
Low computational complexity

Alternatives Considered
Machine Learning-based DDI prediction models
Knowledge graph embeddings
Deep learning interaction predictors

Evaluation Metrics
Conflict Detection Accuracy
Severity Classification Accuracy
Response Time
Graph Completeness

8. Technology Stack
Frontend
HTML
CSS
JavaScript
Backend
Python
Flask
ML/AI
Graph modeling using NetworkX
Database
Local JSON Database
Deployment
Render (optional)
Offline local hosting supported

9. API Documentation & Testing
API Endpoints List
Endpoint 1: Check Interactions

POST /check
Input:

{
  "drugs": ["Warfarin", "Aspirin", "Metformin"]
}

Output:

{
  "conflicts": [...],
  "risk_score": 75
}
Endpoint 2: Get Drug List

GET /drugs

Endpoint 3: Get Graph Data
GET /graph
API Testing Screenshots
(Add Postman / Thunder Client screenshots here)

10. Module-wise Development & Deliverables

Checkpoint 1: Research & Planning
Deliverables:
Problem research
Dataset collection
Architecture design

Checkpoint 2: Backend Development
Deliverables:
API creation
Interaction logic
Pairwise detection engine

Checkpoint 3: Frontend Development
Deliverables:

Input form
Results dashboard
Graph display

Checkpoint 4: Model Training
Deliverables:
Rule-based engine validation
Severity mapping

Checkpoint 5: Model Integration
Deliverables:
Backend–Frontend integration
Graph rendering

Checkpoint 6: Deployment
Deliverables:
Hosted demo
GitHub repository

11. End-to-End Workflow
User enters medication list.
Input is validated.
Pairwise combinations generated.
Interaction database queried.
Conflicts categorized.
Graph model built.
Risk score calculated.
Response returned and displayed.

12. Demo & Video
Live Demo Link: (Add here)
Demo Video Link: (Add here)
GitHub Repository: (Add here)

13. Hackathon Deliverables Summary
Offline Drug Interaction Checker
Graph-based visualization
Structured JSON drug database
API documentation
Working demo
GitHub repository

14. Team Roles & Responsibilities
Member Name	Role	Responsibilities
Your Name	Backend & Architecture	Interaction logic, API, database design
Member 2	Frontend	UI development, visualization
Member 3	Data & Research	Dataset curation, validation

15. Future Scope & Scalability
Short-Term
Expand drug database
Add dosage adjustment recommendations
Export PDF reports
Long-Term
Integrate real clinical APIs
Machine learning-based DDI prediction
EMR system integration
Multi-language support
Mobile application

16. Known Limitations
Prototype-level dataset
Not clinically validated
Limited drug coverage
Rule-based detection only
Does not replace medical consultation

17. Impact
Enhances medication safety
Reduces risk of adverse drug reactions
Supports small clinics and rural healthcare
Improves clinical confidence
Promotes structured medical decision support
