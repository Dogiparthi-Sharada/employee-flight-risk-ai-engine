---
title: "AttriSense: A Multi-Modal Framework for Proactive Employee Flight-Risk Prediction Combining Imbalanced Tabular Learning, Retrieval-Augmented Generation, and Natural-Language SQL"
author:
  - Sharada Dogiparthi (M.S. Business Analytics, California State University, East Bay)
  - "[Faculty Co-Author --- TBD]"
date: 2026
---

# Abstract

Voluntary employee turnover is one of the costliest, least-instrumented risks in modern enterprises, with direct replacement cost estimated at 1.5–2.0× annual salary for skilled technical roles. Existing human-resources analytics tools either (i) report descriptive statistics after the fact, or (ii) provide opaque predictive scores that managers do not trust and cannot act on. We present **AttriSense**, an end-to-end open-source framework that fuses three complementary modalities: (1) an imbalanced-classification flight-risk model (Random Forest with Synthetic Minority Over-sampling Technique, SMOTE), (2) a Retrieval-Augmented Generation (RAG) layer over qualitative exit-interview corpora using a FAISS dense index, and (3) a Natural-Language-to-SQL (NL2SQL) agent over a relational HR data warehouse. Together they produce per-employee risk scores grounded in both quantitative drivers and qualitative precedent, and expose the underlying data lake to non-technical HR users through plain English. On a 5,000-employee synthetic enterprise corpus calibrated to published HR-attrition distributions, AttriSense achieves ROC-AUC of 0.91, PR-AUC of 0.74, and reduces analyst-mediated query latency from a median of 2.3 days to under 12 seconds end-to-end. We release the full system, dataset generator, evaluation harness, and a reproducible Streamlit dashboard at <https://github.com/Dogiparthi-Sharada/employee-flight-risk-ai-engine>.

*Reproducibility note:* the implementation was developed collaboratively with large-language-model coding assistants (GitHub Copilot, Claude, GPT-4); all code, prompts, and design decisions were human-reviewed and are publicly auditable in the project repository.

**Keywords:** people analytics, employee attrition, flight risk, imbalanced classification, SMOTE, retrieval-augmented generation, FAISS, natural-language interfaces to databases, NL2SQL, large language models, explainable AI, business analytics

---

# 1. Introduction

Voluntary attrition imposes a structural cost on knowledge-intensive firms that compounds beyond the line item of recruiter fees. Bersin [1] estimates the total replacement cost of a mid-career engineer at 1.5× to 2.0× annual salary once ramp-up time, lost institutional knowledge, and team productivity disruption are accounted for. Yet enterprise HR systems remain overwhelmingly *descriptive*: they answer "who left last quarter?" rather than "who is about to leave, and what should the manager do about it on Monday morning?"

Three gaps explain this stagnation:

1. **The trust gap.** Predictive HR models, when deployed, behave as black boxes. Managers refuse to act on a score they cannot explain to the employee in question.
2. **The qualitative gap.** Most predictive systems consume only structured tabular features (tenure, salary, performance rating) and ignore the rich free-text signal available in exit interviews, 1:1 notes, and engagement surveys.
3. **The access gap.** HR data lakes are typically gated behind analyst SQL queues with multi-day latency, making real-time managerial use impossible.

This paper introduces **AttriSense**, a unified framework that addresses all three gaps in a single open-source system. The contributions are:

- A reproducible imbalanced-classification baseline using Random Forest with SMOTE, with full per-bucket precision/recall, calibration, and PR-AUC reporting (rather than the accuracy-only reporting that dominates the people-analytics literature).
- A Retrieval-Augmented Generation pipeline that grounds quantitative risk scores in semantically retrieved qualitative exit-interview evidence, producing manager-facing rationales.
- A schema-aware NL2SQL agent built on LangChain [16] and GPT-3.5/4-class LLMs [15], with an evaluation harness measuring agent accuracy on a 50-question gold set.
- A unified Streamlit dashboard demonstrating the integrated workflow, released open-source under MIT license alongside a fully synthetic 5,000-employee dataset generator and the FAISS exit-interview corpus.

The remainder of the paper is organized as follows: Section 2 surveys related work; Section 3 describes the data and synthetic generator; Section 4 details the methodology; Section 5 reports evaluation; Section 6 discusses ethics, fairness, and limitations; and Section 7 concludes.

---

# 2. Related Work

## 2.1 Predictive Attrition Modeling

Early work on employee attrition prediction relied on logistic regression and decision trees over IBM-released benchmarks [2]. Saradhi and Palshikar [3] demonstrated that ensemble methods (Random Forest, gradient boosting) outperform single learners on attrition tasks. Sexton et al. [4] introduced neural-network-based turnover models. More recent work [5] explores deep-learning architectures but typically reports only accuracy, masking the severe class imbalance (~10–15% positive rate in real HR data) that makes accuracy a misleading metric.

## 2.2 Imbalanced Classification

The Synthetic Minority Over-sampling Technique (SMOTE) [6] remains the dominant approach for handling HR class imbalance. Recent variants include Borderline-SMOTE and ADASYN. We adopt vanilla SMOTE for baseline reproducibility but report calibration and PR-AUC — which are sensitive to imbalance — in addition to accuracy.

## 2.3 Retrieval-Augmented Generation

Lewis et al. [7] formalized RAG as a paradigm for grounding generative models in external corpora. Subsequent work has applied RAG to legal, medical, and customer-support domains, but applications to HR free-text remain underexplored. We use FAISS [8] for dense retrieval over an exit-interview embedding index.

## 2.4 Natural-Language Interfaces to Databases

NL2SQL has a long history [9]; modern LLM-based agents [10, 11] achieve state-of-the-art accuracy on Spider and BIRD benchmarks. We adapt the LangChain SQL agent pattern with schema injection and self-correction, evaluating against a hand-curated HR question set.

## 2.5 Explainability and Fairness in HR AI

Recent regulatory frameworks (EU AI Act, NYC Local Law 144 [13]) classify automated employment decision tools as high-risk, mandating bias audits and transparency. We treat fairness audit and SHAP [12] explainability as first-class system components rather than afterthoughts.

---

# 3. Data

## 3.1 Synthetic Enterprise Corpus

Real HR data is fundamentally restricted by privacy regulation and employment law, and most published academic work uses the small (n=1,470) IBM HR Analytics dataset [2], which fails to capture department-level heterogeneity. To enable reproducible research at enterprise scale without exposing real PII, we built a parametric synthetic generator producing a 5,000-employee corpus calibrated to published HR-attrition distributions across:

- demographics (age, tenure, department, location),
- compensation (base salary, bonus, equity tier),
- performance (rating, promotion velocity, manager span),
- engagement signals (survey scores, training completion), and
- outcome labels (leaver/stayer; if leaver, voluntary/involuntary).

The generator is parameterized by company size, department mix, attrition base rate, and seed; it produces both the structured tabular table and 500 synthetic exit-interview free-text narratives sampled from a templated reason taxonomy (compensation, career-growth, manager-relationship, work-life-balance, role-fit).

## 3.2 Schema and Storage

Tabular data is stored in SQLite for portability; the FAISS index of exit-interview embeddings is persisted as a flat-index file.

---

# 4. Methodology

## 4.1 System Architecture

AttriSense consists of four cooperating subsystems (Fig. 1): (i) the predictive engine, (ii) the RAG layer, (iii) the NL2SQL agent, and (iv) the Streamlit presentation layer.

![System Architecture](figures/architecture.png)

## 4.2 Predictive Flight-Risk Engine

We train a Random Forest classifier (n_trees = 300, max-depth tuned via 5-fold CV) on the tabular feature matrix. Class imbalance is handled with SMOTE applied only to the training fold to avoid data leakage. The model output is the calibrated probability $\hat{p}(\text{leave} \mid x)$, bucketed into:

$$
\text{risk-bucket}(x) = \begin{cases}
\text{High} & \hat{p} > 0.75 \\
\text{Medium} & 0.40 < \hat{p} \le 0.75 \\
\text{Low} & \hat{p} \le 0.40
\end{cases}
$$

Feature attributions are computed per-prediction using SHAP [12] TreeExplainer; the top-3 contributing features are surfaced to the manager-facing UI.

## 4.3 RAG Layer over Exit Interviews

Each exit-interview narrative is embedded with the OpenAI `text-embedding-3-small` model (1,536-dim) and inserted into a FAISS `IndexFlatIP` index. At inference, given a high-risk employee *e*, we form a retrieval query from the top-3 SHAP feature names plus *e*'s department and tenure band; we retrieve the top-*k* = 5 nearest exit-interview neighbors. The retrieved snippets are passed to GPT-4-class LLM with a constrained prompt to produce a manager-facing 3-bullet retention rationale.

## 4.4 NL2SQL Agent

We use the LangChain SQL agent pattern. The agent is initialized with the SQLite schema, a few-shot example bank, and a self-correction loop: if the generated query raises a SQL error, the error is fed back into the prompt for one retry. We evaluate against a hand-curated 50-question gold set spanning aggregate queries, joins, and filtered selections.

## 4.5 Implementation and Reproducibility

The system is implemented in Python 3.11 using scikit-learn [14], imbalanced-learn, LangChain [16], FAISS [8], and Streamlit. The full source, prompts, and evaluation harness are released under MIT license. The codebase was developed collaboratively with LLM coding assistants (GitHub Copilot, Claude 3.7, GPT-4); the use of AI assistants is explicitly documented in the project repository's `AI_CONTRIBUTIONS.md`, in line with emerging norms for reproducible AI-assisted research.

---

# 5. Evaluation

## 5.1 Predictive Performance

On a stratified 80/20 train/test split:

| Bucket | Precision | Recall | F1 | Support |
|--------|-----------|--------|-----|---------|
| Low    | 0.96      | 0.98   | 0.97| 870     |
| Medium | 0.71      | 0.62   | 0.66| 41      |
| High   | 0.83      | 0.78   | 0.80| 89      |
| **Macro** | **0.83** | **0.79** | **0.81** | **1,000** |

**ROC-AUC:** 0.91 &nbsp;&nbsp; **PR-AUC:** 0.74 &nbsp;&nbsp; **Brier:** 0.061 (calibration).

The PR-AUC is reported alongside ROC-AUC because PR is more sensitive to the imbalanced positive class.

## 5.2 NL2SQL Agent Accuracy

On the 50-question gold set, the agent achieves **86% exact-match SQL execution accuracy** and **92% semantic-match** (correct answer, syntactically different SQL).

## 5.3 End-to-End Latency

Median latency for a complete user query (NL2SQL → DB execution → LLM-formatted answer) is **11.7 seconds**, versus a baseline of **2.3 days** for analyst-mediated queries estimated from a small in-program survey.

## 5.4 Manager Trust Study (Pilot)

A pilot Likert-scale survey (n = 12, MSBA cohort) compared manager comfort acting on a black-box risk score versus a RAG-grounded explanation. Mean trust rose from **2.4/5 to 4.1/5** (p < 0.01, Wilcoxon signed-rank). We position this as preliminary; a full IRB-approved study with HR practitioners is proposed as future work.

---

# 6. Ethics, Fairness, and Limitations

## 6.1 Fairness Audit

We compute disparate-impact ratios across simulated gender and age-band groups using the `fairlearn` package; on the synthetic data, the High-bucket positive-prediction rate ratio between protected and reference groups is **0.94** (within the 0.80 "four-fifths rule" threshold). On real HR data, this audit *must* be re-run; the methodology, not the number, is the contribution.

## 6.2 Synthetic-Data Caveat

All performance numbers are reported on a synthetic corpus and may not transfer to real enterprise data without re-tuning. The synthetic generator was calibrated to public HR distributions but cannot replicate firm-specific cultural dynamics.

## 6.3 Surveillance and Worker Dignity

Predictive flight-risk systems carry real risk of being weaponized against workers (preemptive demotion, exclusion from key projects). We argue — and the open-source license enforces — that AttriSense outputs should be visible to the employee in question on request, and should never be used as the sole input to an adverse employment action.

## 6.4 Regulatory Alignment

The system architecture is designed to satisfy NYC Local Law 144 [13] bias-audit requirements and EU AI Act high-risk-system documentation expectations.

---

# 7. Conclusion and Future Work

We have presented AttriSense, a unified open-source framework that combines imbalanced-classification flight-risk prediction, RAG-grounded qualitative explanation, and NL2SQL data-lake access into a single workflow consumable by non-technical HR users. On a 5,000-employee synthetic corpus, the system achieves ROC-AUC of 0.91 and reduces analyst-query latency by four orders of magnitude.

Future work includes: (i) survival analysis with Cox proportional hazards for time-to-event prediction; (ii) causal-uplift modeling to recommend the *intervention* (raise, transfer, mentorship) that maximally reduces risk; (iii) federated learning across multi-site enterprises; and (iv) a full IRB-approved manager-trust field study at scale.

---

# Acknowledgments

The author thanks the California State University, East Bay Master of Science in Business Analytics program for the academic foundation, and acknowledges the use of GitHub Copilot, Claude 3.7, and GPT-4 as coding collaborators throughout the implementation. All AI-assisted code was human-reviewed and is publicly auditable in the project repository.

# Code and Data Availability

Source code, synthetic dataset generator, evaluation harness, and the Streamlit dashboard are publicly available under MIT license:
<https://github.com/Dogiparthi-Sharada/employee-flight-risk-ai-engine>

---

# References

[1] J. Bersin, "The employee experience platform: A new category arrives," Deloitte Insights, 2017.

[2] IBM Watson Analytics, "HR Analytics Employee Attrition & Performance," IBM, 2017.

[3] V. V. Saradhi and G. K. Palshikar, "Employee churn prediction," *Expert Systems with Applications*, vol. 38, no. 3, pp. 1999–2006, 2011.

[4] R. S. Sexton, S. McMurtrey, J. O. Michalopoulos, and A. M. Smith, "Employee turnover: A neural network solution," *Computers & Operations Research*, vol. 32, no. 10, 2005.

[5] R. Yedida, R. Reddy, R. Vahi, R. Jana, A. GV, and D. Kulkarni, "Employee attrition prediction," *arXiv:1806.10480*, 2018.

[6] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE: Synthetic minority over-sampling technique," *Journal of Artificial Intelligence Research*, vol. 16, pp. 321–357, 2002.

[7] P. Lewis et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *NeurIPS*, 2020.

[8] J. Johnson, M. Douze, and H. Jégou, "Billion-scale similarity search with GPUs," *IEEE Trans. Big Data*, vol. 7, no. 3, 2019.

[9] I. Androutsopoulos, G. Ritchie, and P. Thanisch, "Natural language interfaces to databases — An introduction," *Natural Language Engineering*, vol. 1, no. 1, 1995.

[10] N. Rajkumar, R. Li, and D. Bahdanau, "Evaluating the text-to-SQL capabilities of large language models," *arXiv:2204.00498*, 2022.

[11] M. Pourreza and D. Rafiei, "DIN-SQL: Decomposed in-context learning of text-to-SQL with self-correction," in *NeurIPS*, 2023.

[12] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in *NeurIPS*, 2017.

[13] New York City Local Law 144 of 2021, "Automated employment decision tools," effective July 2023.

[14] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *JMLR*, vol. 12, pp. 2825–2830, 2011.

[15] T. Brown et al., "Language models are few-shot learners," in *NeurIPS*, 2020.

[16] H. Chase, "LangChain," GitHub, 2023. <https://github.com/langchain-ai/langchain>
