# Changelog
All notable changes to the Sentiment Auditor project are documented in this file.

# [3.2.0] - 2026-03-11
### Added
- **Governance Visualization:** Introduced a "Verification Rate" donut chart to visualize the ratio of AI-generated vs. Human-verified data points.
- **Sample Data Fallback:** Implemented a smart-loading sequence that provides a `sample_data.csv` for new users to explore dashboard capabilities immediately without an API key.
- **Operational UX:** Integrated an interactive row-selection trigger that automatically links the Audit Log to the Sidebar Editor for faster expert overrides.

### Fixed
- **Selection State Persistence:** Corrected `st.dataframe` configuration to use the proper hyphenated `single-row` selection mode, restoring the ability to challenge AI scores.
- **Data Pipeline Resiliency:** Added `fillna()` logic to the date processing pipeline to ensure articles with missing publication timestamps do not crash the global date filters.
- **Sequential Item Numbering:** Default ordering to ascending by index number. 

# [3.1.0] - 2026-03-11
### Added
- Global Search & Filter: Replaced local table search with a global dashboard search (Title, Description, Publisher) and Date Range picker for deep investigative analysis.

- Improved Data Resiliency: Implemented robust ISO8601 date parsing with error handling to ensure pipeline stability across varying API formats.

- Enhanced Audit Log: Restored date_published to the Audit Log and enabled interactive LinkColumn rendering for seamless access to source articles.

- Actionable UI Hierarchy: Reordered audit log columns to prioritize operational metrics (Status, Sentiment, Score) before content, creating a more intuitive "Action-to-Context" workflow.

### Fixed
- State Management: Resolved NameError in table rendering by correcting the order of operations for data manipulation and display.

- Filtering Logic: Refactored global filter logic to ensure UI components dynamically re-render based on search inputs, eliminating "hidden result" bugs.

- Data Integrity: Added data coercion for missing values (NaN/NaT) to prevent runtime crashes during dashboard ingestion.

## [3.0.0] - 2026-03-06
### Added
- Longitudinal Sentiment Drift: Integrated time-series line charting to visualize sentiment trends.
- Publisher Bias Reporting: Added categorical horizontal bar charts to analyze sentiment variance by news source.
- Governance Documentation: Drafted official PRD, Roadmap, and Changelog to formalize the product lifecycle.
- Empty-State UX: Added intelligent "PM Notes" for users to guide data collection requirements.
- Technical Integrity: Implemented datetime casting and de-duplication logic to ensure chronological accuracy.

## [2.0.0] - 2026-02-25
### Added
- Auditor Toolbox: Built Human-in-the-Loop (HITL) sidebar for real-time sentiment overrides.
- Data Provenance: Introduced 'Status' tagging (🤖 Auto vs 👤 Manual) to distinguish AI vs. expert records.
- Persistence Layer: Added "Permanent Save" functionality to commit manual overrides to the master CSV.
- UX Optimization: Implemented session state management to handle data persistence during UI reruns.

## [1.0.0] - 2026-02-10
### Added
- Base Ingestion Pipeline: Established connection to NewsAPI for real-time data collection.
- Inference Engine: Implemented VADER for initial polarity scoring.
- Dashboard Foundation: Built high-density table view with Streamlit for executive visibility.