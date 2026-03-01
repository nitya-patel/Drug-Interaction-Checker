# 🩺 Drug Interaction Checker with Graph-Based Conflict Detection

## 👥 Team Name
**Codecrew**

---

## 🔗 Live Links

- **Deployed App:**  
  https://drug-interaction-checkergit-fcajbg3co6q2sau8yzvmar.streamlit.app  

- **Demo Video:**  
  https://drive.google.com/file/d/1nckD_cEFyZoki-L4pGuo__5lWj-zNgxk/view  

---

## 📌 One-Line Project Description

An **offline, graph-based Drug Interaction Checker** that detects medication conflicts, categorizes severity levels, calculates risk scores, and visualizes drug interactions to enhance prescription safety.

---

# 1️⃣ Problem Statement

## 🏷 Problem Title
**Polypharmacy Drug Interaction Risk Detection**

## 📖 Problem Description

Patients—especially elderly individuals and those with chronic illnesses—often consume multiple medications simultaneously. This practice, known as **polypharmacy**, significantly increases the risk of:

- Drug–Drug Interactions  
- Contraindications  
- Dosage Conflicts  
- Adverse Drug Reactions  

While large hospital systems may include advanced interaction-checking tools, smaller clinics and rural healthcare providers often lack lightweight, structured, and offline-accessible systems for quick medication conflict evaluation.

Manual reference checking is time-consuming, fragmented, and prone to human error, compromising patient safety.

---

## 🎯 Target Users

- General Physicians  
- Small Clinics  
- Rural Healthcare Providers  
- Pharmacists  
- Medical Students  
- Telemedicine Practitioners  

---

## 🚫 Existing Gaps

- Lack of lightweight offline solutions  
- Fragmented manual checking methods  
- Limited visualization of interaction severity  
- No structured graph-based conflict representation  
- Reduced accessibility in low-connectivity environments  

---

# 2️⃣ Problem Understanding & Approach

## 🔍 Root Cause Analysis

- Polypharmacy leads to exponential pairwise drug interaction possibilities  
- Manual cross-referencing is inefficient and error-prone  
- Many tools require internet access or paid subscriptions  
- Lack of visual and severity-based risk interpretation  

## 💡 Solution Strategy

- Use a structured local drug interaction dataset  
- Implement graph-based pairwise interaction detection  
- Categorize interactions by severity level  
- Visualize medication conflicts as a graph network  
- Ensure complete offline functionality  

---

# 3️⃣ Proposed Solution

## 🧠 Solution Overview

**MediGraph** is an offline Drug Interaction Checker that:

- Analyzes a list of medications  
- Detects conflicts using structured pairwise matching  
- Categorizes severity levels  
- Visually represents drug interactions using graph modeling  

## 🔗 Core Idea

- **Drugs → Nodes**
- **Interactions → Edges**
- Rule-based logic detects conflicts and classifies severity

## ⭐ Key Features

- Drug–Drug Interaction Detection  
- Contraindication Identification  
- Dosage Conflict Flagging  
- Severity Categorization (Mild / Moderate / Severe / Contraindicated)  
- Graph-Based Visualization  
- Offline Operation  
- Risk Score Generation  
- Clear Clinical Explanation Output  

---

# 4️⃣ System Architecture

## 🔄 High-Level Flow

User → Frontend → Backend API → Interaction Engine
→ Local Drug Database → Graph Generator → Response


## 🏗 Architecture Description

1. User inputs medication list  
2. Frontend sends request to backend API  
3. Backend validates input  
4. Interaction engine generates pairwise combinations  
5. Local JSON database is queried  
6. Conflicts are categorized by severity  
7. Graph model is generated  
8. Structured response is returned  
9. Results are displayed in table and graph format  

---

# 5️⃣ Database Design

## 🗂 ER Diagram Description

### 📌 Entities

### Drug
- Drug_ID  
- Drug_Name  
- Max_Dosage  
- Category  

### Interaction
- Interaction_ID  
- Drug1_ID  
- Drug2_ID  
- Severity  
- Description  

### 🔁 Relationship

- Many-to-Many relationship between Drug entities via Interaction  

---

# 6️⃣ Dataset Selected

## 📚 Dataset Name
**Structured Drug Interaction Dataset (Custom Curated)**

## 🌍 Sources
- DrugBank  
- PubChem  
- U.S. Food and Drug Administration (FDA)  
- World Health Organization (WHO)  

## 📦 Data Type
- JSON structured dataset  
- Drug metadata  
- Pairwise interaction records  
- Severity classification  

## ✅ Selection Reason
- Publicly accessible references  
- Credible medical sources  
- Suitable for offline structured modeling  
- Supports graph-based logic  

## ⚙ Preprocessing Steps
- Standardized drug names  
- Removed duplicates  
- Normalized severity levels  
- Converted dataset to JSON format  
- Indexed drugs for constant-time lookup  

---

# 7️⃣ Model Selected

## 🧩 Model Name
**Graph-Based Rule Engine (Deterministic Pairwise Conflict Detection)**

## 📌 Selection Reasoning
- Efficient for polypharmacy pair generation  
- Deterministic and interpretable  
- Suitable for offline implementation  
- Low computational complexity  

## 🔄 Alternatives Considered
- Machine Learning-based DDI prediction models  
- Knowledge graph embeddings  
- Deep learning interaction predictors  

## 📊 Evaluation Metrics
- Conflict Detection Accuracy  
- Severity Classification Accuracy  
- Response Time  
- Graph Completeness  

---

# 8️⃣ Technology Stack

## 🎨 Frontend
- HTML  
- CSS  
- JavaScript  

## 🖥 Backend
- Python  
- Flask  

## 📈 Graph Modeling
- NetworkX  

## 🗄 Database
- Local JSON Database  

## 🚀 Deployment
- Streamlit / Render  
- Offline local hosting supported  

---

# 9️⃣ API Documentation

## 📌 Endpoint 1: Check Interactions

**POST /check**

### Input
```json
{
  "drugs": ["Warfarin", "Aspirin", "Metformin"]
}
```
Output
```
{
  "conflicts": [...],
  "risk_score": 75
}
```
## 📌 API Endpoints

### Endpoint 2: Get Drug List
**GET /drugs**

---

### Endpoint 3: Get Graph Data
**GET /graph**

---

## 🔟 Module-wise Development

### ✅ Checkpoint 1: Research & Planning
- Problem research  
- Dataset collection  
- Architecture design  

### ✅ Checkpoint 2: Backend Development
- API creation  
- Interaction logic  
- Pairwise detection engine  

### ✅ Checkpoint 3: Frontend Development
- Input form  
- Results dashboard  
- Graph display  

### ✅ Checkpoint 4: Model Validation
- Rule-based engine validation  
- Severity mapping  

### ✅ Checkpoint 5: Integration
- Backend–Frontend integration  
- Graph rendering  

### ✅ Checkpoint 6: Deployment
- Hosted demo  
- GitHub repository  

---

## 🔁 End-to-End Workflow
1. User enters medication list  
2. Input is validated  
3. Pairwise combinations are generated  
4. Interaction database is queried  
5. Conflicts are categorized  
6. Graph model is built  
7. Risk score is calculated  
8. Response is returned and displayed  

---

## 📦 Hackathon Deliverables
- Offline Drug Interaction Checker  
- Graph-based visualization  
- Structured JSON drug database  
- API documentation  
- Working demo  
- GitHub repository  

---

## 👨‍💻 Team Roles & Responsibilities

| Name | Role | Responsibilities |
|------|------|------------------|
| **Nitya Patel** | Frontend Developer & UI/UX Designer | Responsive UI, dashboard design, API integration, interactive color-coded graph 
| **Aryan Kesarkar** | Backend & Core Logic Developer | Flask backend, REST APIs, interaction logic, severity & risk scoring, graph generation |visualizations |
| **Shreya Singh** | Data Engineer, Research & QA | Dataset curation, JSON structuring, testing, validation, documentation |

---

## 🚀 Future Scope & Scalability

### 🔹 Short-Term
- Expand drug database  
- Add dosage adjustment recommendations  
- Export PDF reports  

### 🔹 Long-Term
- Integrate real clinical APIs  
- Machine learning-based DDI prediction  
- EMR system integration  
- Multi-language support  
- Mobile application  

---

## ⚠ Known Limitations
- Prototype-level dataset  
- Not clinically validated  
- Limited drug coverage  
- Rule-based detection only  
- Does not replace professional medical consultation  

---

## 🌍 Impact
- Enhances medication safety  
- Reduces risk of adverse drug reactions  
- Supports small clinics and rural healthcare  
- Improves clinical confidence  
- Promotes structured medical decision support  
