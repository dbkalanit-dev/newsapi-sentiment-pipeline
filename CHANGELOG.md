# Changelog
All notable changes to the Sentiment Auditor project are documented in this file.

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