# Product Roadmap

## Phase 1: Foundation & Auditability (Completed)
- [x] Ingestion pipeline for real-time news data.
- [x] Human-in-the-Loop (HITL) scoring overrides.
- [x] Persistent storage of manual audit trails.

## Phase 2: Data Intelligence (Immediate)
- [ ] **Data Export:** CSV/JSON export for "Gold Standard" datasets to enable future LLM fine-tuning.
- [ ] **Variance Detection:** Add a "Conflict Flag" when Human score and AI score diverge by > 0.5.
- [ ] **Test Coverage:** Implement unit testing for data parsing and score calculation scripts.

## Phase 3: Advanced Governance (Vision)
- [ ] **Automated Categorization:** Use NLP keyword-tagging to filter by "Regulation," "Ethics," or "Product Launch."
- [ ] **Alerting Service:** Implement priority thresholding for critical negative sentiment events.
- [ ] **Deployment:** Transition from local script to hosted web application (Streamlit Cloud).