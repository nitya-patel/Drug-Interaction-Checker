🩺 Drug Interaction Checker

Offline Clinical Decision-Support Prototype — Hackathon Project

A lightweight system designed to detect drug–drug interactions, contraindications, and dosage conflicts using a structured local database and graph-based logic to improve medication safety.

📚 Table of Contents

Problem Statement • Solution Overview • Key Features • Architecture • Usage • Database Structure • Graph Visualization • Severity Classification • Safety Disclaimer • Limitations & Future Work • Testing

🚨 Problem Statement
Polypharmacy significantly increases the risk of medication errors, adverse drug reactions, and delayed prescription decisions. While large hospitals may use integrated electronic systems, smaller clinics and individual practitioners often lack fast, structured interaction-checking tools. Manual reference lookup across fragmented sources reduces efficiency, clinical confidence, and patient safety outcomes.

💡 Solution Overview
The system operates fully offline using the workflow:

Medication Input → Local Database → Rule Engine
→ Severity Classification → Graph Visualization → Results Dashboard


It evaluates medication combinations through rule-based conflict detection, identifies risks, and communicates results using structured explanations and visual graphs for quick clinical interpretation.

⭐ Key Features
Medication list input system.
Drug–drug interaction detection.
Contraindication identification.
Dosage conflict alerts.
Severity classification (Mild → Contraindicated).
Graph-based visualization of medication conflicts.
Human-readable clinical risk explanations.
Fully offline accessibility.

🏗 Architecture
1.⁠ ⁠Local Drug Database
Stores structured medication rules including drug names, maximum dosage limits, interaction partners, severity levels, and clinical explanations.

2.⁠ ⁠Pairwise Interaction Engine
Generates all medication combinations for evaluation.

Example:

Input:
[Aspirin, Warfarin, Ibuprofen]

Generated Pairs:
(Aspirin,Warfarin)
(Aspirin,Ibuprofen)
(Warfarin,Ibuprofen)


Each pair is matched against stored interaction rules.

3.⁠ ⁠Dosage Validator
Compares user-entered dosage values with defined maximum limits and flags overdose risks.

4.⁠ ⁠Severity Classifier
Categorizes detected conflicts into standardized clinical risk levels.

5.⁠ ⁠Visualization Engine
Represents medications as a graph:

Nodes → Drugs
Edges → Interactions

▶️ Usage

Enter medications separated by commas:
Warfarin, Aspirin, Paracetamol


System output includes:

Conflict table.
Severity warnings.
Clinical explanations.
Medication interaction graph.

🗄 Database Structure

Example dataset entry:

{
  "Warfarin": {
    "max_dose": 10,
    "interactions": {
      "Aspirin": {
        "severity": "Severe",
        "reason": "High bleeding risk"
      }
    }
  }
}


Stored information includes:

Drug name.

Maximum recommended dosage.
Interaction partners.
Severity classification.
Clinical explanation text.

📊 Graph Visualization
Medication conflicts are displayed visually to enable rapid understanding.

Concept:

Node → Drug
Edge → Interaction

Severity representation:

Yellow → Mild
Orange → Moderate
Red → Severe

This allows quick identification of high-risk medication combinations.

⚠ Severity Classification

Mild: Minimal clinical concern.
Moderate: Monitoring recommended.
Severe: High probability of adverse effects.

Contraindicated: Combination should be avoided.

⚠️ Safety Disclaimer (IMPORTANT)
This application is an educational hackathon prototype and is not a certified medical device. It is not approved for diagnosis, prescribing, or treatment decisions. The dataset is limited and may not include comprehensive clinical information. Healthcare professionals must consult validated clinical references and exercise independent judgment. This tool is intended only as a decision-support aid and does not replace clinical expertise.

🚧 Limitations & Future Work
Current Limitations

Limited drug dataset.
Rule-based detection only.
No patient allergy or medical history integration.
Future Improvements
Expanded medical databases.
AI-assisted prediction models.
Electronic prescription integration.
Patient-specific risk scoring.

🧪 Testing

Testing scenarios included:
No-interaction validation cases.
Severe interaction detection.
Invalid medication inputs.
Dosage overdose validation.
Manual verification ensured backend stability, correct rule matching, and accurate graph visualization.
