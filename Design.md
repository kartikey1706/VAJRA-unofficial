# Design Document - VAJRA

## 1. Design Philosophy
VAJRA is a **Meteorological Intelligence Platform**. The UI must communicate scientific authority, operational urgency, and data transparency. It avoids "SaaS-style" aesthetics in favor of an **Operational Control Center (OCC)** look.

## 2. Visual Theme
### 2.1 Color Palette (Semantic)
- **Background:** `#0A0F1E` (Deep Navy/Midnight)
- **Panels:** `#161B2D` (Dark Blue-Grey)
- **Text (Primary):** `#E2E8F0` (Off-White/Light Grey)
- **Text (Secondary):** `#94A3B8` (Slate)
- **Accent (Analytical):** `#06B6D4` (Cyan)

**Risk-Based Semantic Colors:**
- **High Confidence (Low Bust Prob):** `#10B981` (Emerald Green)
- **Medium Confidence:** `#F59E0B` (Amber/Yellow)
- **Low Confidence (High Bust Prob):** `#EF4444` (Rose Red)

### 2.2 Typography
- **Primary Font:** `Inter` or `Geist` (Clean, modern sans-serif).
- **Data Font:** `JetBrains Mono` or `IBM Plex Mono` (For coordinates, timestamps, and probability values).

## 3. Dashboard Layout
The dashboard is a single-page operational view designed for high data density.

### 3.1 Header (Top Bar)
- **Left:** VAJRA Logo + "Forecast Bust Detection System".
- **Center:** Current Forecast Cycle (e.g., `2026-10-02 00Z`).
- **Right:** Data Status Indicator (Green: Syncing, Red: Delayed) + Last Update Timestamp.

### 3.2 Main Control Panel (Left Sidebar)
- **Lead-Time Selector:** A horizontal or vertical segmented control: `Day 1 | Day 2 | ... | Day 10`.
- **Variable Selector:** A dropdown for meteorological parameters: `Temperature`, `Precipitation`, `Wind Speed`, `Geopotential Height`.
- **Region Selector:** Search bar for cities/regions or a "High-Risk Only" toggle.
- **Data Quality Toggle:** Option to show/hide cells with missing observation data.

### 3.3 The Intelligence Map (Center)
- **Base Layer:** Dark-themed topographic map (e.g., Mapbox Dark).
- **Overlay Layer:** A high-resolution probability heatmap.
    - Color transition: Green $\to$ Yellow $\to$ Red.
    - Opacity: 60-80% to allow topographic features to be visible.
- **Interactivity:**
    - **Hover:** Tooltip showing `Bust Prob: X%`, `Confidence: LOW/MED/HIGH`.
    - **Click:** Selection of a grid cell or cluster, triggering the Bottom Detail Panel.

### 3.4 Intelligence Detail Panel (Bottom Section)
A three-column layout that appears when a region is selected:
- **Column 1: Reliability Metrics**
    - Big Number: Bust Probability (e.g., `72%`).
    - Confidence Label: `LOW` (in Red).
    - Lead Time: `Day 6`.
- **Column 2: Explainability (The "Why")**
    - List of top contributing factors:
        - `Ensemble Spread: HIGH` $\uparrow$
        - `Regime: Monsoon Active` $\to$
        - `Analogue Error: High` $\uparrow$
- **Column 3: Historical Analogues**
    - Top 3 similar cases:
        - `Case 1 (Similarity 94%): Bust occurred`.
        - `Case 2 (Similarity 88%): No bust`.
        - `Case 3 (Similarity 81%): Bust occurred`.

## 4. Interaction Design
- **Lead-Time Transition:** When switching from Day 3 to Day 4, the map should cross-fade or transition smoothly to show the evolution of risk.
- **Risk Cluster Highlighting:** High-risk cells should have a subtle "glow" or pulse to draw the operator's attention.
- **Responsive Behavior:**
    - **Desktop:** Full 3-panel view.
    - **Tablet/Mobile:** Sidebar collapses into a hamburger menu; Bottom Panel becomes a slide-up sheet.

## 5. Component Specifications
- **Probability Heatmap:** Rendered using WebGL/Canvas for performance with large grids.
- **Confidence Badge:** A pill-shaped component with semantic background colors.
- **Analogue Card:** A compact card showing similarity % and outcome.
