const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "ML Engineer";
pres.title = "Loan Default Prediction — Production ML System";

// ── PALETTE ────────────────────────────────────────────────────────────────
const C = {
  navy:    "0A1628",
  blue:    "1A56DB",
  cyan:    "0EA5E9",
  teal:    "0D9488",
  light:   "F0F6FF",
  white:   "FFFFFF",
  gray:    "64748B",
  lgray:   "E2EAF8",
  red:     "DC2626",
  green:   "16A34A",
  amber:   "D97706",
  text:    "1E293B",
  accent:  "7C3AED",
};

// ── HELPERS ────────────────────────────────────────────────────────────────
function titleSlide(slide, title, sub) {
  slide.background = { color: C.navy };
  // Top accent bar
  slide.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.06, fill:{ color: C.cyan } });
  // Bottom bar
  slide.addShape(pres.shapes.RECTANGLE, { x:0, y:5.55, w:10, h:0.075, fill:{ color: C.blue } });
  // Left accent stripe
  slide.addShape(pres.shapes.RECTANGLE, { x:0, y:0.06, w:0.08, h:5.49, fill:{ color: C.teal } });

  slide.addText(title, {
    x:0.5, y:1.5, w:9, h:1.5,
    fontSize:42, bold:true, color: C.white, fontFace:"Georgia", align:"center"
  });
  slide.addText(sub, {
    x:0.5, y:3.2, w:9, h:0.8,
    fontSize:18, color: C.cyan, fontFace:"Calibri", align:"center"
  });
  slide.addText("ML Engineering | Production-Grade System Design", {
    x:0.5, y:4.8, w:9, h:0.4,
    fontSize:11, color: C.gray, fontFace:"Calibri", align:"center"
  });
}

function sectionHeader(slide, number, title, subtitle) {
  slide.background = { color: C.blue };
  slide.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:0.5, h:5.625, fill:{ color: C.navy } });
  slide.addShape(pres.shapes.RECTANGLE, { x:0, y:4.8, w:10, h:0.825, fill:{ color: C.navy } });
  slide.addText(`PHASE ${number}`, {
    x:0.7, y:1.2, w:8, h:0.6,
    fontSize:14, bold:true, color: C.cyan, fontFace:"Calibri", charSpacing:6
  });
  slide.addText(title, {
    x:0.7, y:1.9, w:8.5, h:1.4,
    fontSize:38, bold:true, color: C.white, fontFace:"Georgia"
  });
  slide.addText(subtitle, {
    x:0.7, y:3.5, w:8, h:0.7,
    fontSize:16, color: "CCE0FF", fontFace:"Calibri"
  });
}

function contentSlide(slide, title) {
  slide.background = { color: C.white };
  slide.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.85, fill:{ color: C.navy } });
  slide.addShape(pres.shapes.RECTANGLE, { x:0, y:5.25, w:10, h:0.375, fill:{ color: C.lgray } });
  slide.addText(title, {
    x:0.4, y:0.12, w:9.2, h:0.6,
    fontSize:22, bold:true, color: C.white, fontFace:"Georgia", valign:"middle"
  });
  slide.addText("Loan Default Prediction — Production ML System", {
    x:0.4, y:5.28, w:9, h:0.3,
    fontSize:9, color: C.gray, fontFace:"Calibri"
  });
}

function card(slide, x, y, w, h, header, body, color) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill:{ color: C.white },
    line:{ color: color || C.lgray, width:1.5 },
    shadow:{ type:"outer", blur:8, offset:3, angle:135, color:"000000", opacity:0.08 }
  });
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w:0.07, h,  fill:{ color: color || C.blue } });
  slide.addText(header, { x:x+0.15, y:y+0.08, w:w-0.2, h:0.3, fontSize:11, bold:true, color: C.text, fontFace:"Calibri" });
  slide.addText(body,   { x:x+0.15, y:y+0.38, w:w-0.2, h:h-0.45, fontSize:10, color: C.gray, fontFace:"Calibri", wrap:true });
}

function pill(slide, x, y, label, color) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w:1.6, h:0.35, fill:{ color }, rectRadius:0.18 });
  slide.addText(label, { x, y, w:1.6, h:0.35, fontSize:10, bold:true, color: C.white, align:"center", valign:"middle" });
}

function arrow(slide, x, y, w) {
  slide.addShape(pres.shapes.LINE, { x, y, w, h:0, line:{ color: C.cyan, width:2 } });
  // arrowhead triangle approximation
  slide.addShape(pres.shapes.RECTANGLE, { x:x+w-0.04, y:y-0.06, w:0.04, h:0.12, fill:{ color: C.cyan } });
}


// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 1 — TITLE
// ═══════════════════════════════════════════════════════════════════════════
let s = pres.addSlide();
titleSlide(s,
  "Loan Default Prediction\nML Production System",
  "End-to-End MLOps: Data → Training → Deployment → Monitoring"
);

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 2 — PROBLEM STATEMENT
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "Problem Statement & Business Context");

s.addText("Why does this matter?", { x:0.4, y:0.95, w:4, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });

const problems = [
  ["Financial Risk", "Loan defaults cause millions in losses annually for financial institutions"],
  ["Imbalanced Data", "Only ~8% of loans default → naive models predict 0% and look 92% accurate"],
  ["Complex Patterns", "Credit score + income alone miss non-linear risk signals in 40 features"],
  ["Regulatory Need", "Banks must explain decisions (GDPR / Fair Lending) — black-box won't do"],
];
problems.forEach(([h, b], i) => {
  card(s, 0.35, 1.35 + i * 0.96, 4.2, 0.88, h, b, [C.blue, C.teal, C.accent, C.red][i]);
});

s.addText("Target Metric Priority", { x:5.1, y:0.95, w:4.5, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });
const metrics = [
  ["#1  Recall (Sensitivity)", "Catch as many true defaults as possible", C.red],
  ["#2  AUC-ROC", "Rank-ordering quality across all thresholds", C.blue],
  ["#3  F1 Score", "Balance between precision and recall", C.teal],
  ["#4  Precision", "Control false alarm rate (approval noise)", C.amber],
];
metrics.forEach(([label, desc, col], i) => {
  s.addShape(pres.shapes.RECTANGLE, { x:5.1, y:1.35+i*0.94, w:4.5, h:0.85, fill:{ color: C.lgray }, line:{ color:col, width:2 } });
  s.addText(label, { x:5.25, y:1.42+i*0.94, w:4.2, h:0.28, fontSize:11, bold:true, color:col, fontFace:"Calibri" });
  s.addText(desc,  { x:5.25, y:1.70+i*0.94, w:4.2, h:0.22, fontSize:10, color:C.gray, fontFace:"Calibri" });
});

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 3 — SYSTEM ARCHITECTURE
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "System Architecture — End-to-End MLOps");

// Pipeline flow boxes
const stages = [
  { label:"Raw Data\n(CSV/DB)", color: C.navy },
  { label:"Ingest &\nValidate",  color: C.blue },
  { label:"Feature\nEngineering", color: C.teal },
  { label:"SMOTE +\nTrain Model", color: C.accent },
  { label:"Evaluate\n& Gate",    color: C.amber },
  { label:"Docker\nAPI",         color: C.green },
  { label:"Monitor\n& Alert",    color: C.red },
];

stages.forEach((st, i) => {
  const x = 0.3 + i * 1.37;
  s.addShape(pres.shapes.RECTANGLE, { x, y:1.0, w:1.25, h:0.9, fill:{ color: st.color }, line:{ color: C.white, width:1 } });
  s.addText(st.label, { x, y:1.0, w:1.25, h:0.9, fontSize:9, bold:true, color:C.white, align:"center", valign:"middle" });
  if (i < stages.length-1) {
    s.addShape(pres.shapes.LINE, { x:x+1.25, y:1.45, w:0.12, h:0, line:{ color:C.cyan, width:2.5 } });
  }
});

// Layer labels
s.addText("CI/CD Automation (GitHub Actions — triggers on push / schedule)", {
  x:0.3, y:2.1, w:9.4, h:0.3,
  fontSize:10, color:C.blue, fontFace:"Calibri", italic:true, align:"center"
});
s.addShape(pres.shapes.RECTANGLE, { x:0.3, y:2.38, w:9.4, h:0.04, fill:{ color:C.cyan } });

// Infrastructure cards
const infra = [
  ["Data Layer", "CSV → Pandas → PostgreSQL / S3", C.navy],
  ["Training Layer", "Sklearn Pipeline + SMOTE + MLflow", C.blue],
  ["Serving Layer", "FastAPI + Docker + NGINX Canary", C.teal],
  ["Monitoring", "PSI Drift + Prometheus + Grafana", C.red],
];
infra.forEach(([h, b, c], i) => {
  card(s, 0.3 + i*2.4, 2.55, 2.25, 1.4, h, b, c);
});

s.addText("Tools: Python · Scikit-learn · FastAPI · Docker · GitHub Actions · MLflow · Grafana", {
  x:0.4, y:4.15, w:9.2, h:0.4,
  fontSize:10, color:C.gray, fontFace:"Calibri", align:"center"
});


// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 4 — PHASE 1: DATA
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
sectionHeader(s, "1", "Data Ingestion &\nFeature Engineering", "Handling 121,856 rows · 40 features · Class imbalance · Missing values");

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 5 — EDA & PREPROCESSING DETAIL
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "EDA, Preprocessing & Feature Engineering");

// Left column — steps
s.addText("Preprocessing Steps", { x:0.4, y:0.95, w:4.2, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });
const steps = [
  ["1. Type Casting", "7 columns stored as strings → pd.to_numeric()"],
  ["2. Sentinel Values", "Employed_Days=365243 → NaN (means unemployed)"],
  ["3. Imputation", "Median for numeric, 'Unknown' for categorical"],
  ["4. Encoding", "OrdinalEncoder with unknown_value=-1"],
  ["5. Scaling", "StandardScaler on all numeric features"],
  ["6. SMOTE", "Synthetic minority oversampling on training set only"],
];
steps.forEach(([h, b], i) => {
  card(s, 0.4, 1.35 + i*0.65, 4.2, 0.58, h, b, C.blue);
});

// Right column — new features
s.addText("Engineered Features", { x:5.1, y:0.95, w:4.5, h:0.35, fontSize:14, bold:true, color:C.teal, fontFace:"Georgia" });
const feats = [
  ["income_annuity_ratio", "Client_Income / Loan_Annuity → affordability score", C.teal],
  ["credit_income_ratio",  "Credit_Amount / Client_Income → leverage score", C.teal],
  ["age_years",            "Age_Days / 365 → human-readable", C.blue],
  ["employment_years",     "Employed_Days / 365 → job stability", C.blue],
];
feats.forEach(([h, b, c], i) => {
  card(s, 5.1, 1.35 + i*0.95, 4.5, 0.85, h, b, c);
});

// Class imbalance callout
s.addShape(pres.shapes.RECTANGLE, { x:5.1, y:5.15, w:4.5, h:0.35, fill:{ color: C.red }, line:{ color:C.red, width:1 } });
s.addText("⚠  Class Imbalance: ~8% Default (1) vs 92% Non-Default (0) → Use SMOTE", {
  x:5.15, y:5.15, w:4.4, h:0.35,
  fontSize:10, bold:true, color:C.white, valign:"middle", fontFace:"Calibri"
});

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 6 — PHASE 2: MODEL TRAINING
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
sectionHeader(s, "2", "Model Training &\nExperiment Tracking", "Sklearn Pipelines · SMOTE · MLflow · Quality Gates");

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 7 — MODEL SELECTION & EVALUATION
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "Model Selection, Evaluation & Experiment Tracking");

s.addText("Model Comparison", { x:0.4, y:0.95, w:5, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });

// Table
const tableData = [
  [
    { text:"Model",         options:{ bold:true, color:C.white, fill:{ color:C.navy } } },
    { text:"AUC-ROC",       options:{ bold:true, color:C.white, fill:{ color:C.navy } } },
    { text:"F1",            options:{ bold:true, color:C.white, fill:{ color:C.navy } } },
    { text:"Recall",        options:{ bold:true, color:C.white, fill:{ color:C.navy } } },
    { text:"Notes",         options:{ bold:true, color:C.white, fill:{ color:C.navy } } },
  ],
  ["Logistic Regression", "0.71", "0.58", "0.61", "Baseline, interpretable"],
  ["Random Forest",       "0.74", "0.62", "0.65", "Good, parallelizable"],
  [
    { text:"Gradient Boosting ★", options:{ bold:true, color:C.green } },
    { text:"0.77",                options:{ bold:true, color:C.green } },
    { text:"0.65",                options:{ bold:true, color:C.green } },
    { text:"0.70",                options:{ bold:true, color:C.green } },
    { text:"Best — selected",     options:{ bold:true, color:C.green } },
  ],
];
s.addTable(tableData, {
  x:0.4, y:1.35, w:5.8, h:1.7,
  border:{ pt:1, color:C.lgray },
  colW:[2.0, 0.9, 0.7, 0.85, 1.35],
  fontSize:10, fontFace:"Calibri"
});

s.addText("Experiment Tracking with MLflow", { x:0.4, y:3.18, w:5, h:0.35, fontSize:14, bold:true, color:C.teal, fontFace:"Georgia" });
const mlflow_items = [
  "Every run logs: params, metrics, data hash, artifacts",
  "Data hash ensures full reproducibility of any past run",
  "MLflow UI: compare runs, visualize metrics, register models",
  "Model Registry: Staging → Production promotion workflow",
];
s.addText(mlflow_items.map(t => ({ text:t, options:{ bullet:true, breakLine:true, paraSpaceAfter:4 } })),
  { x:0.55, y:3.58, w:5.6, h:1.5, fontSize:11, color:C.text, fontFace:"Calibri" }
);

// Right side — quality gate
s.addShape(pres.shapes.RECTANGLE, {
  x:6.6, y:0.95, w:3.0, h:3.6,
  fill:{ color:C.light }, line:{ color:C.blue, width:1.5 },
  shadow:{ type:"outer", blur:8, offset:3, angle:135, color:"000000", opacity:0.10 }
});
s.addText("Quality Gate", { x:6.7, y:1.05, w:2.8, h:0.35, fontSize:13, bold:true, color:C.navy, fontFace:"Georgia" });

const gates = [
  ["AUC-ROC", "≥ 0.70", C.teal],
  ["F1 Score", "≥ 0.60", C.blue],
  ["Recall",   "≥ 0.60", C.red],
];
gates.forEach(([label, val, col], i) => {
  s.addShape(pres.shapes.RECTANGLE, { x:6.75, y:1.5+i*0.85, w:2.7, h:0.72, fill:{ color:C.white }, line:{ color:col, width:1.5 } });
  s.addText(label, { x:6.85, y:1.56+i*0.85, w:2.5, h:0.28, fontSize:11, bold:true, color:col, fontFace:"Calibri" });
  s.addText(val,   { x:6.85, y:1.84+i*0.85, w:2.5, h:0.28, fontSize:13, bold:true, color:C.navy, fontFace:"Georgia" });
});

s.addText("Pipeline exits with code 1\nif any gate fails → CI/CD blocked", {
  x:6.7, y:4.12, w:2.8, h:0.58,
  fontSize:10, color:C.gray, fontFace:"Calibri", align:"center", italic:true
});

// Imbalance handling note
s.addShape(pres.shapes.RECTANGLE, { x:0.4, y:4.75, w:9.2, h:0.42, fill:{ color:"FFF7ED" }, line:{ color:C.amber, width:1.5 } });
s.addText("Imbalance Strategy: SMOTE applied ONLY on training set (after split) to prevent data leakage. Class weights also set to 'balanced' in tree models.",
  { x:0.55, y:4.78, w:9.0, h:0.35, fontSize:10, color:C.text, fontFace:"Calibri" }
);

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 8 — PHASE 3: DEPLOYMENT
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
sectionHeader(s, "3", "Containerized Deployment\n& Canary Strategy", "Docker · FastAPI · NGINX · 90/10 Traffic Split");

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 9 — DEPLOYMENT DETAIL
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "Deployment Strategy: Canary Builds & Rolling Rollout");

// Canary diagram
const deploySteps = [
  { label:"Build &\nPush Image", x:0.35, color:C.navy },
  { label:"Deploy\nCanary (10%)", x:2.05, color:C.blue },
  { label:"15 Min\nObservation", x:3.75, color:C.amber },
  { label:"Auto\nValidation", x:5.45, color:C.teal },
  { label:"Full\nRollout", x:7.15, color:C.green },
];
deploySteps.forEach((step, i) => {
  s.addShape(pres.shapes.RECTANGLE, { x:step.x, y:1.0, w:1.55, h:0.85, fill:{ color:step.color } });
  s.addText(step.label, { x:step.x, y:1.0, w:1.55, h:0.85, fontSize:9.5, bold:true, color:C.white, align:"center", valign:"middle" });
  if (i < deploySteps.length - 1) {
    s.addShape(pres.shapes.LINE, { x:step.x+1.55, y:1.43, w:0.15, h:0, line:{ color:C.cyan, width:2 } });
  }
});

// Rollback box
s.addShape(pres.shapes.RECTANGLE, { x:7.85, y:0.9, w:1.75, h:1.05, fill:{ color: C.red } });
s.addText("Rollback\n(auto if error\nrate > 5%)", { x:7.85, y:0.9, w:1.75, h:1.05, fontSize:9.5, bold:true, color:C.white, align:"center", valign:"middle" });

// NGINX explanation
s.addText("How Canary Works", { x:0.4, y:2.1, w:5, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });
const canary_text = [
  "NGINX routes 90% traffic → stable model, 10% → canary model",
  "Both containers run in parallel; canary uses new model artifact",
  "Automated validation checks: latency P99, error rate, prediction drift",
  "If validation passes → promote canary to stable (100% traffic)",
  "If validation fails → auto-rollback to previous stable image",
];
s.addText(canary_text.map(t => ({ text:t, options:{ bullet:true, breakLine:true, paraSpaceAfter:3 } })),
  { x:0.55, y:2.5, w:5.2, h:1.8, fontSize:11, color:C.text, fontFace:"Calibri" }
);

// API security
s.addText("API Security", { x:5.8, y:2.1, w:3.8, h:0.35, fontSize:14, bold:true, color:C.teal, fontFace:"Georgia" });
const security = [
  ["API Key Auth", "X-API-Key header required on all /predict calls"],
  ["Non-root Docker", "Container runs as mluser, not root"],
  ["Read-only mounts", "Model volume mounted :ro in Docker"],
  ["Input Validation", "Pydantic validators reject malformed inputs"],
  ["HTTPS", "TLS via nginx/cert-manager in production"],
];
security.forEach(([h, b], i) => {
  card(s, 5.8, 2.5 + i*0.6, 3.8, 0.52, h, b, C.teal);
});

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 10 — PHASE 4: MONITORING
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
sectionHeader(s, "4", "Model Monitoring\n& Drift Detection", "PSI · Prometheus · Grafana · PagerDuty Alerts");

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 11 — MONITORING DETAIL
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "Monitoring Strategy: Drift, Performance & Alerting");

// PSI thresholds
s.addText("Population Stability Index (PSI) — Drift Detection", { x:0.4, y:0.95, w:9, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });

const psiLevels = [
  { range:"PSI < 0.10", label:"No Drift", color:C.green, desc:"Distribution stable — no action needed" },
  { range:"0.10 – 0.25", label:"Moderate", color:C.amber, desc:"Monitor closely — potential shift" },
  { range:"PSI > 0.25", label:"Significant", color:C.red, desc:"CRITICAL — trigger retraining pipeline" },
];
psiLevels.forEach((p, i) => {
  s.addShape(pres.shapes.RECTANGLE, { x:0.4+i*3.1, y:1.38, w:2.9, h:1.1, fill:{ color: p.color } });
  s.addText(p.range,  { x:0.4+i*3.1, y:1.43, w:2.9, h:0.35, fontSize:11, bold:true, color:C.white, align:"center" });
  s.addText(p.label,  { x:0.4+i*3.1, y:1.75, w:2.9, h:0.3, fontSize:13, bold:true, color:C.white, align:"center" });
  s.addText(p.desc,   { x:0.4+i*3.1, y:2.05, w:2.9, h:0.35, fontSize:9, color:C.white, align:"center", wrap:true });
});

// Monitoring dimensions
s.addText("What We Monitor", { x:0.4, y:2.7, w:4, h:0.35, fontSize:14, bold:true, color:C.teal, fontFace:"Georgia" });
const monDims = [
  ["Data Drift", "PSI on all numeric features vs. training reference data"],
  ["Prediction Drift", "PSI on model output score distribution"],
  ["Performance", "F1, AUC on labeled production data (sample)"],
  ["Latency", "P50/P95/P99 API response time (Prometheus)"],
  ["Error Rate", "HTTP 4xx/5xx rate — triggers PagerDuty if > 2%"],
];
monDims.forEach(([h, b], i) => {
  card(s, 0.4, 3.1 + i*0.46, 5.0, 0.4, h, b, C.teal);
});

// Alerting
s.addText("Alert Channels", { x:5.8, y:2.7, w:3.8, h:0.35, fontSize:14, bold:true, color:C.red, fontFace:"Georgia" });
const alerts = [
  ["Slack", "WARNING alerts → team channel, instant notification"],
  ["PagerDuty", "CRITICAL alerts → on-call engineer, 5-min SLA"],
  ["Email", "Weekly drift report to ML lead & business owner"],
  ["GitHub Issue", "Auto-creates issue with drift details + retrain tag"],
];
alerts.forEach(([h, b], i) => {
  card(s, 5.8, 3.1 + i*0.54, 3.8, 0.48, h, b, C.red);
});

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 12 — CI/CD PIPELINE
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
sectionHeader(s, "5", "CI/CD Pipeline\n& MLOps Automation", "GitHub Actions · 5-Phase Pipeline · Scheduled Retraining");

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 13 — CI/CD DETAIL
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "CI/CD Pipeline: From Code Push to Production");

const cicdPhases = [
  { num:"1", name:"Lint &\nUnit Tests", trigger:"Every PR / Push", detail:"flake8 + pytest\n12 tests covering data, features, monitoring", color:C.navy },
  { num:"2", name:"Train &\nEvaluate", trigger:"Weekly / [retrain] tag", detail:"Full pipeline run\nQuality gate: AUC ≥ 0.70, F1 ≥ 0.60", color:C.blue },
  { num:"3", name:"Build\nDocker Image", trigger:"Push to main", detail:"Multi-stage Dockerfile\nPush to ghcr.io registry", color:C.teal },
  { num:"4", name:"Canary\nDeploy", trigger:"After image build", detail:"10% traffic, 15 min window\nAuto-validate error rate", color:C.amber },
  { num:"5", name:"Full\nRollout", trigger:"After canary pass", detail:"100% traffic cut-over\nSlack notification to team", color:C.green },
];
cicdPhases.forEach((ph, i) => {
  const x = 0.35 + i * 1.87;
  s.addShape(pres.shapes.RECTANGLE, { x, y:1.0, w:1.72, h:0.45, fill:{ color:ph.color } });
  s.addText(`Phase ${ph.num}: ${ph.name}`, { x, y:1.0, w:1.72, h:0.45, fontSize:9, bold:true, color:C.white, align:"center", valign:"middle" });
  s.addShape(pres.shapes.RECTANGLE, { x, y:1.48, w:1.72, h:1.6, fill:{ color:C.light }, line:{ color:ph.color, width:1.5 } });
  s.addText("Trigger:\n" + ph.trigger, { x:x+0.05, y:1.52, w:1.62, h:0.55, fontSize:8.5, color:C.gray, fontFace:"Calibri", wrap:true });
  s.addText(ph.detail, { x:x+0.05, y:2.1, w:1.62, h:0.92, fontSize:8.5, color:C.text, fontFace:"Calibri", wrap:true });
  if (i < cicdPhases.length - 1) {
    s.addShape(pres.shapes.LINE, { x:x+1.72, y:1.23, w:0.15, h:0, line:{ color:C.cyan, width:2 } });
  }
});

// Governance
s.addText("Governance & Audit Trail", { x:0.4, y:3.25, w:9.2, h:0.35, fontSize:14, bold:true, color:C.navy, fontFace:"Georgia" });
const gov = [
  ["Data Lineage", "Every model stores the MD5 hash of training data for full reproducibility"],
  ["Model Registry", "MLflow tracks all versions: Staging → Production → Archived states"],
  ["Access Control", "API keys per consumer, RBAC on MLflow, Docker registry auth"],
  ["Audit Logs", "All predictions logged with timestamp, inputs, output, model version"],
];
gov.forEach(([h, b], i) => {
  card(s, 0.4 + i * 2.4, 3.65, 2.25, 1.35, h, b, C.navy);
});

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 14 — LOAD & STRESS TESTING
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "Load & Stress Testing Strategy");

s.addText("How to Validate API at Scale", { x:0.4, y:0.95, w:9, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });

const loadTests = [
  { type:"Load Test", tool:"Locust", config:"100 concurrent users · 10 min · ramp-up 20 RPS/min", target:"P95 < 200ms, error < 1%", color:C.blue },
  { type:"Stress Test", tool:"k6", config:"Ramp to 500 req/s until failure · find breaking point", target:"Identify saturation point & graceful degradation", color:C.amber },
  { type:"Spike Test", tool:"Artillery", config:"0→1000 req/s in 30 sec → back to baseline", target:"Auto-scaling triggers; no 5xx during spike", color:C.red },
  { type:"Soak Test", tool:"Locust", config:"50 concurrent users · 24 hours · memory leak check", target:"Stable latency; RSS memory flat after warmup", color:C.teal },
];
loadTests.forEach((lt, i) => {
  const x = 0.35 + i * 2.4;
  s.addShape(pres.shapes.RECTANGLE, { x, y:1.38, w:2.2, h:0.42, fill:{ color:lt.color } });
  s.addText(lt.type, { x, y:1.38, w:2.2, h:0.42, fontSize:12, bold:true, color:C.white, align:"center", valign:"middle" });
  s.addShape(pres.shapes.RECTANGLE, { x, y:1.82, w:2.2, h:2.2, fill:{ color:C.light }, line:{ color:lt.color, width:1.5 } });
  s.addText(`Tool: ${lt.tool}`, { x:x+0.1, y:1.88, w:2.0, h:0.3, fontSize:10, bold:true, color:lt.color });
  s.addText(`Config: ${lt.config}`, { x:x+0.1, y:2.2, w:2.0, h:0.6, fontSize:9, color:C.text, wrap:true });
  s.addText(`Target: ${lt.target}`, { x:x+0.1, y:2.85, w:2.0, h:0.6, fontSize:9, color:C.gray, italic:true, wrap:true });
});

// Locust snippet
s.addShape(pres.shapes.RECTANGLE, { x:0.35, y:4.22, w:9.3, h:0.95, fill:{ color:C.navy } });
s.addText(
  "# Locust example\nfrom locust import HttpUser, task\nclass LoanUser(HttpUser):\n    @task\n    def predict(self):\n        self.client.post('/predict', json={...}, headers={'X-API-Key':'key'})",
  { x:0.5, y:4.25, w:9.0, h:0.88, fontSize:8.5, color:"A8D8FF", fontFace:"Consolas" }
);

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 15 — BUSINESS INTERPRETATION
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "Business Solution & Results Interpretation");

s.addText("Translating ML Outputs to Business Decisions", { x:0.4, y:0.95, w:9, h:0.35, fontSize:14, bold:true, color:C.navy, fontFace:"Georgia" });

const tiers = [
  { range:"0 – 30%", label:"LOW RISK", action:"AUTO APPROVE", color:C.green, desc:"Fast-track loan approval. No human review needed. Offer competitive rate." },
  { range:"30 – 60%", label:"MEDIUM RISK", action:"HUMAN REVIEW", color:C.amber, desc:"Flag for credit analyst review. May approve with higher interest rate or collateral." },
  { range:"60 – 100%", label:"HIGH RISK", action:"DECLINE", color:C.red, desc:"Decline application. Provide GDPR-compliant reason. Suggest smaller loan amount." },
];
tiers.forEach((t, i) => {
  s.addShape(pres.shapes.RECTANGLE, { x:0.35+i*3.2, y:1.38, w:3.0, h:0.45, fill:{ color:t.color } });
  s.addText(`${t.range}  |  ${t.label}`, { x:0.35+i*3.2, y:1.38, w:3.0, h:0.45, fontSize:10, bold:true, color:C.white, align:"center", valign:"middle" });
  s.addShape(pres.shapes.RECTANGLE, { x:0.35+i*3.2, y:1.85, w:3.0, h:0.5, fill:{ color:t.color }, line:{ color:t.color, width:1 } });
  s.addText(t.action, { x:0.35+i*3.2, y:1.85, w:3.0, h:0.5, fontSize:14, bold:true, color:C.white, align:"center", valign:"middle" });
  s.addShape(pres.shapes.RECTANGLE, { x:0.35+i*3.2, y:2.38, w:3.0, h:1.1, fill:{ color:C.light }, line:{ color:t.color, width:1 } });
  s.addText(t.desc, { x:0.45+i*3.2, y:2.45, w:2.8, h:0.95, fontSize:10, color:C.text, fontFace:"Calibri", wrap:true });
});

// ROI frame
s.addText("Business Impact", { x:0.4, y:3.65, w:4, h:0.35, fontSize:14, bold:true, color:C.teal, fontFace:"Georgia" });
const roi = [
  ["Recall Priority", "Maximize catching true defaults even at cost of some false alarms"],
  ["Cost Matrix", "Default cost >> False-alarm cost → tune threshold toward higher recall"],
  ["Threshold Tuning", "Default: 0.5 threshold; tune to 0.35 to boost recall for high-risk loans"],
  ["Explainability", "SHAP values explain each rejection for regulatory compliance"],
];
roi.forEach(([h, b], i) => {
  card(s, 0.4, 4.05 + i * 0, 4.2, 0.42, h, b, C.teal);
  // stagger
});
// Reposition
roi.forEach(([h, b], i) => {
  card(s, i < 2 ? 0.4 : 4.8, i < 2 ? 4.05 + i * 0.52 : 4.05 + (i-2) * 0.52, 4.2, 0.46, h, b, C.teal);
});

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 16 — FOLDER STRUCTURE
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
contentSlide(s, "Project Folder Structure");

s.addShape(pres.shapes.RECTANGLE, { x:0.4, y:0.95, w:4.3, h:4.4, fill:{ color:C.navy } });
const tree = `loan_default_mlops/
├── src/
│   ├── data/
│   │   └── ingest.py          ← load, validate, split
│   ├── features/
│   │   └── feature_eng.py     ← engineer, preprocess
│   ├── models/
│   │   └── train.py           ← train, evaluate, log
│   ├── api/
│   │   └── serve.py           ← FastAPI app
│   ├── monitoring/
│   │   └── drift.py           ← PSI, alerts
│   └── tests/
│       └── test_pipeline.py   ← 12 unit tests
├── scripts/
│   └── train_pipeline.py      ← orchestrator
├── docker/
│   ├── Dockerfile             ← multi-stage
│   ├── docker-compose.yml     ← full stack
│   └── nginx.conf             ← canary routing
├── ci_cd/
│   └── ml_cicd.yml            ← GitHub Actions
├── configs/
│   └── config.yaml
├── experiments/               ← run logs (MLflow)
├── models/                    ← saved model artifacts
└── requirements.txt`;

s.addText(tree, { x:0.5, y:1.05, w:4.1, h:4.15, fontSize:8, color:"A8D8FF", fontFace:"Consolas" });

// Right: tool stack
s.addText("Technology Stack", { x:5.1, y:0.95, w:4.5, h:0.35, fontSize:14, bold:true, color:C.blue, fontFace:"Georgia" });
const stack = [
  ["Data", "Pandas, NumPy, Scikit-learn", C.blue],
  ["Imbalance", "imbalanced-learn (SMOTE)", C.teal],
  ["Serving", "FastAPI + Uvicorn", C.green],
  ["Containers", "Docker (multi-stage) + NGINX", C.navy],
  ["Orchestration", "docker-compose / Kubernetes", C.accent],
  ["Experiment Tracking", "MLflow (file → DB backend)", C.blue],
  ["Monitoring", "Custom PSI + Prometheus + Grafana", C.red],
  ["CI/CD", "GitHub Actions (5 phases)", C.amber],
  ["Testing", "pytest (12 unit tests)", C.teal],
  ["Security", "API Keys + non-root Docker", C.gray],
];
stack.forEach(([cat, val, col], i) => {
  s.addShape(pres.shapes.RECTANGLE, { x:5.1, y:1.38+i*0.38, w:4.5, h:0.35, fill:{ color:C.white }, line:{ color:col, width:1 } });
  s.addShape(pres.shapes.RECTANGLE, { x:5.1, y:1.38+i*0.38, w:0.05, h:0.35, fill:{ color:col } });
  s.addText(cat + ":", { x:5.2, y:1.41+i*0.38, w:1.5, h:0.28, fontSize:9, bold:true, color:col });
  s.addText(val,       { x:6.75, y:1.41+i*0.38, w:2.75, h:0.28, fontSize:9, color:C.text });
});

// ═══════════════════════════════════════════════════════════════════════════
//  SLIDE 17 — THANK YOU
// ═══════════════════════════════════════════════════════════════════════════
s = pres.addSlide();
s.background = { color: C.navy };
s.addShape(pres.shapes.RECTANGLE, { x:0, y:0, w:10, h:0.06, fill:{ color:C.cyan } });
s.addShape(pres.shapes.RECTANGLE, { x:0, y:5.55, w:10, h:0.075, fill:{ color:C.blue } });

s.addText("System Ready for Production", {
  x:0.5, y:1.1, w:9, h:1.2,
  fontSize:38, bold:true, color:C.white, fontFace:"Georgia", align:"center"
});
s.addText("12 Tests Passing · 5-Phase CI/CD · Canary Deployment · PSI Drift Detection", {
  x:0.5, y:2.45, w:9, h:0.5,
  fontSize:16, color:C.cyan, fontFace:"Calibri", align:"center"
});

const summary = [
  "Clean modular code → easy to extend or swap components",
  "SMOTE handles class imbalance · MLflow tracks every experiment",
  "Canary builds ensure zero-downtime deployments with auto-rollback",
  "PSI drift detection triggers automatic retraining pipeline",
  "Interview-ready: covers EDA, modeling, deployment, and monitoring",
];
s.addText(summary.map(t => ({ text:t, options:{ bullet:true, breakLine:true, paraSpaceAfter:5 } })),
  { x:1.5, y:3.1, w:7, h:2.0, fontSize:13, color:"CCE0FF", fontFace:"Calibri" }
);

// ── WRITE FILE ─────────────────────────────────────────────────────────────
pres.writeFile({ fileName: "/mnt/user-data/outputs/LoanDefault_MLOps_System.pptx" })
  .then(() => console.log("✅ Presentation saved!"))
  .catch(e => { console.error(e); process.exit(1); });
