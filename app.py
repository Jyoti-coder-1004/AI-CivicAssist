import streamlit as st
import pandas as pd
import plotly.express as px

from modules.analytics import (
    load_civic_data,
    filter_civic_data,
    calculate_metrics,
)

from modules.ai_engine import (
    analyze_issue,
    analyze_severity,
    generate_recommendation,
) 

from modules.voice_analyzer import (
    analyze_voice_report
)    


from modules.vision_analyzer import(
    analyze_civic_image,    
)


from modules.complaint_manager import (
    create_complaint,
    load_complaints,
    update_complaint_status,
)
from modules.map_manager import (
    load_map_complaints,
    filter_map_complaints,
    get_map_statistics,
    get_location_insights,
)

from utils.session import initialize_session_state


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI CivicAssist",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

initialize_session_state()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .hero-card {
        padding: 40px;
        border-radius: 24px;
        margin-bottom: 30px;

        background:
            linear-gradient(
                135deg,
                rgba(40, 60, 110, 0.95),
                rgba(25, 35, 75, 0.95)
            );

        border: 1px solid rgba(255, 255, 255, 0.12);

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.25);
    }


    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 12px;
        color: white;
    }


    .hero-subtitle {
        font-size: 24px;
        font-weight: 600;
        color: #dbe7ff;
        margin-bottom: 15px;
    }


    .hero-description {
        font-size: 16px;
        line-height: 1.7;
        color: #c8d2e8;
        max-width: 800px;
        margin-bottom: 25px;
    }


    .hero-features {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }


    .hero-features span {
        padding: 10px 16px;
        border-radius: 12px;

        background: rgba(255, 255, 255, 0.08);

        border: 1px solid rgba(
            255,
            255,
            255,
            0.12
        );

        color: white;
        font-size: 14px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "data/civic_issues.csv"

try:
    df = load_civic_data(DATA_PATH)

except FileNotFoundError:
    st.error(
        "Civic dataset not found. "
        "Please check data/civic_issues.csv"
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌍 AI CivicAssist")

    st.caption(
        "AI-powered civic issue intelligence platform"
    )

    st.divider()

    st.markdown("### 🔎 Filters")

    categories = ["All"] + sorted(
        df["category"].unique().tolist()
    )

    severities = ["All"] + sorted(
        df["severity"].unique().tolist()
    )

    statuses = ["All"] + sorted(
        df["status"].unique().tolist()
    )

    category = st.selectbox(
        "Issue Category",
        categories,
        key="selected_category",
    )

    severity = st.selectbox(
        "Severity",
        severities,
        key="selected_severity",
    )

    status = st.selectbox(
        "Status",
        statuses,
        key="selected_status",
    )

    st.divider()

    st.info(
        "AI analysis, image recognition, voice reporting "
        "and smart recommendations will be added in later stages."
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = filter_civic_data(
    df,
    category,
    severity,
    status,
)

metrics = calculate_metrics(filtered_df)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero-card">

        <div class="hero-title">
            🔵 AI CivicAssist
        </div>

        <div class="hero-subtitle">
            Intelligent Civic Issue Detection,
            Reporting & Community Management
        </div>

        <div class="hero-description">
            AI-powered civic intelligence platform that helps
            citizens identify, analyze and prioritize real-world
            community problems.
        </div>

        <div class="hero-features">
            <span>🤖 AI Analysis</span>
            <span>📸 Vision AI</span>
            <span>🎤 Voice AI</span>
            <span>📊 Smart Analytics</span>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Civic Overview</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Issues",
        metrics["total"],
        "+12%",
    )

with col2:
    st.metric(
        "High Priority",
        metrics["high_priority"],
        "+5%",
    )

with col3:
    st.metric(
        "Open Issues",
        metrics["open"],
        "-3%",
    )

with col4:
    st.metric(
        "Resolution Rate",
        f"{metrics['resolution_rate']:.1f}%",
        "+8%",
    )


# ============================================================
# ANALYTICS
# ============================================================

st.markdown(
    '<div class="section-title">📈 Issue Analytics</div>',
    unsafe_allow_html=True,
)

chart_col1, chart_col2 = st.columns(2)


# -------------------- CATEGORY CHART -------------------------

with chart_col1:

    category_counts = (
        filtered_df["category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "category",
        "count",
    ]

    fig_category = px.bar(
        category_counts,
        x="category",
        y="count",
        title="Issues by Category",
        labels={
            "category": "Category",
            "count": "Issues",
        },
    )

    fig_category.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True,
    )


# -------------------- SEVERITY CHART -------------------------

with chart_col2:

    severity_counts = (
        filtered_df["severity"]
        .value_counts()
        .reset_index()
    )

    severity_counts.columns = [
        "severity",
        "count",
    ]

    fig_severity = px.pie(
        severity_counts,
        names="severity",
        values="count",
        title="Severity Distribution",
        hole=0.45,
    )

    fig_severity.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    st.plotly_chart(
        fig_severity,
        use_container_width=True,
    )


# ============================================================
# STATUS CHART
# ============================================================

status_counts = (
    filtered_df["status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "status",
    "count",
]

fig_status = px.bar(
    status_counts,
    x="status",
    y="count",
    title="Issue Resolution Status",
    labels={
        "status": "Status",
        "count": "Number of Issues",
    },
)

fig_status.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=50, b=20),
)

st.plotly_chart(
    fig_status,
    use_container_width=True,
)


# ============================================================
# SMART CIVIC MAP
# ============================================================

st.markdown("---")

st.header("🗺️ Smart Civic Issue Map")

st.write(
    "Explore civic complaints by location, "
    "severity, category and resolution status."
)

map_df = load_map_complaints()

if map_df.empty:

    st.info(
        "No complaints with valid coordinates "
        "are available for the map yet."
    )

else:

    # --------------------------------------------------------
    # MAP FILTERS
    # --------------------------------------------------------

    st.markdown(
        "### 🔎 Map Filters"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        category_options = [
            "All"
        ] + sorted(
            map_df["category"]
            .dropna()
            .unique()
            .tolist()
        )

        map_category = st.selectbox(
            "🏷️ Category",
            category_options,
            key="map_category_filter"
        )

    with col2:

        severity_options = [
            "All",
            "Low",
            "Medium",
            "High",
            "Critical",
        ]

        map_severity = st.selectbox(
            "🚨 Severity",
            severity_options,
            key="map_severity_filter"
        )

    with col3:

        status_options = [
            "All"
        ] + sorted(
            map_df["status"]
            .dropna()
            .unique()
            .tolist()
        )

        map_status = st.selectbox(
            "🚦 Status",
            status_options,
            key="map_status_filter"
        )

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    filtered_map_df = filter_map_complaints(
        map_df,
        category=map_category,
        severity=map_severity,
        status=map_status,
    )

    

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    st.markdown(
        "### 🗺️ Issue Locations"
    )

    if filtered_map_df.empty:

        st.warning(
            "No complaints match the selected filters."
        )

    else:

        st.map(
            filtered_map_df[
                [
                    "latitude",
                    "longitude",
                ]
            ],
            use_container_width=True,
        )

        # ----------------------------------------------------
        # MAP DATA
        # ----------------------------------------------------

        st.markdown(
            "### 📋 Mapped Issues"
        )

        st.dataframe(
            filtered_map_df[
                [
                    "complaint_id",
                    "category",
                    "severity",
                    "location",
                    "status",
                    "latitude",
                    "longitude",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

# ============================================================
# AI CIVIC ISSUE ANALYZER
# ============================================================

st.markdown(
    '<div class="section-title">🤖 AI Civic Issue Analyzer</div>',
    unsafe_allow_html=True,
)

st.write(
    "Describe a local civic problem and let Gemini analyze it."
)


with st.form("civic_analysis_form"):

    description = st.text_area(
        "Describe the civic issue",
        placeholder=(
            "Example: There is a large pothole near "
            "the main road. Vehicles are having difficulty "
            "passing through this area."
        ),
        height=150,
    )

    location = st.text_input(
        "Location Context",
        placeholder="Example: Near the community park",
    )

    submitted = st.form_submit_button(
        "🤖 Analyze Civic Issue"
    )



# ============================================================
# MULTIMODAL VISION ANALYZER
# ============================================================

st.markdown(
    '<div class="section-title">📸 AI Vision Civic Detector</div>',
    unsafe_allow_html=True,
)

st.write(
    "Upload or capture an image of a civic issue. "
    "Gemini Vision will analyze the visible problem."
)


vision_col1, vision_col2 = st.columns(2)


# ============================================================
# CAMERA INPUT
# ============================================================

with vision_col1:

    st.markdown("### 📷 Capture Image")

    camera_image = st.camera_input(
        "Take a photo of the civic issue"
    )


# ============================================================
# FILE UPLOAD
# ============================================================

with vision_col2:

    st.markdown("### 🖼️ Upload Image")

    uploaded_image = st.file_uploader(
        "Upload a civic issue image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
        ],
    )

# ============================================================
# VOICE CIVIC REPORTER
# ============================================================

st.markdown(
    "---"
)

st.header("🎤 Voice Civic Reporter")

st.write(
    "Record your civic complaint using your voice. "
    "CivicAssist will transcribe and analyze it using AI."
)

audio_value = st.audio_input(
    "Record your civic issue"
)

if audio_value is not None:

    st.audio(
        audio_value
    )

    if st.button(
        "🎤 Analyze Voice Report",
        key="analyze_voice_button"
    ):

        try:

            with st.spinner(
                "Analyzing your voice report with Gemini..."
            ):

                audio_bytes = audio_value.getvalue()

                mime_type = (
                    audio_value.type
                    or "audio/wav"
                )

                voice_result = analyze_voice_report(
                    audio_bytes=audio_bytes,
                    mime_type=mime_type,
                )

            st.success(
                "Voice report analyzed successfully!"
            )

            st.markdown(
                "### 🧠 AI Voice Analysis"
            )

            st.markdown(
                voice_result
            )

        except Exception as e:

            st.error(
                "Unable to analyze the voice report."
            )

            st.caption(
                f"Technical details: {str(e)}"
            )



# ============================================================
# SMART CIVIC COMPLAINT SUBMISSION
# ============================================================

st.markdown("---")

st.header("📝 Submit a Civic Complaint")

st.write(
    "Create and submit a structured civic complaint "
    "for tracking and resolution."
)

with st.form("civic_complaint_form"):

    category = st.selectbox(
        "Issue Category",
        [
            "Garbage",
            "Road Damage",
            "Streetlight",
            "Water Leakage",
            "Public Facility",
            "Accessibility",
            "Traffic",
            "Pollution",
            "Drainage",
            "Other",
        ],
    )

    severity = st.selectbox(
        "Severity",
        [
            "Low",
            "Medium",
            "High",
            "Critical",
        ],
    )

    description = st.text_area(
        "Issue Description",
        placeholder=(
            "Describe the civic issue..."
        ),
    )

    location = st.text_input(
        "Location",
        placeholder=(
            "Enter area, city or landmark..."
        ),
    )

    latitude = st.text_input(
        "Latitude (optional)"
    )

    longitude = st.text_input(
        "Longitude (optional)"
    )

    submitted = st.form_submit_button(
        "🚀 Submit Complaint"
    )


    if submitted:

        if not description.strip():

            st.warning(
                "Please enter an issue description."
            )

        else:

            try:

                complaint = create_complaint(
                    category=category,
                    severity=severity,
                    description=description,
                    location=location,
                    latitude=latitude,
                    longitude=longitude,
                )

                st.success(
                    "Civic complaint submitted successfully!"
                )

                st.info(
                    f"Complaint ID: "
                    f"{complaint['complaint_id']}"
                )

                st.write(
                    f"**Status:** "
                    f"{complaint['status']}"
                )

            except Exception as e:

                st.error(
                    "Unable to submit complaint."
                )

                st.caption(
                    f"Technical details: {str(e)}"
                )


# ============================================================
# MY COMPLAINTS / COMPLAINT TRACKING
# ============================================================

st.markdown("---")

st.header("📋 Complaint Tracking")

st.write(
    "View and track submitted civic complaints."
)

complaints_df = load_complaints()

if complaints_df.empty:

    st.info(
        "No complaints have been submitted yet."
    )

else:

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search_id = st.text_input(
        "🔎 Search Complaint ID",
        placeholder="Example: CA-2026-0001"
    )

    filtered_complaints = complaints_df.copy()

    if search_id.strip():

        filtered_complaints = filtered_complaints[
            filtered_complaints[
                "complaint_id"
            ]
            .astype(str)
            .str.contains(
                search_id.strip(),
                case=False,
                na=False
            )
        ]

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        categories = [
            "All"
        ] + sorted(
            complaints_df["category"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Category",
            categories,
            key="tracking_category"
        )

    with col2:

        severities = [
            "All"
        ] + sorted(
            complaints_df["severity"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_severity = st.selectbox(
            "Severity",
            severities,
            key="tracking_severity"
        )

    with col3:

        statuses = [
            "All"
        ] + sorted(
            complaints_df["status"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_status = st.selectbox(
            "Status",
            statuses,
            key="tracking_status"
        )

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    if selected_category != "All":

        filtered_complaints = filtered_complaints[
            filtered_complaints["category"]
            == selected_category
        ]

    if selected_severity != "All":

        filtered_complaints = filtered_complaints[
            filtered_complaints["severity"]
            == selected_severity
        ]

    if selected_status != "All":

        filtered_complaints = filtered_complaints[
            filtered_complaints["status"]
            == selected_status
        ]

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    total = len(filtered_complaints)

    submitted_count = len(
        filtered_complaints[
            filtered_complaints["status"]
            == "Submitted"
        ]
    )

    resolved_count = len(
        filtered_complaints[
            filtered_complaints["status"]
            == "Resolved"
        ]
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Complaints",
            total
        )

    with col2:

        st.metric(
            "Submitted",
            submitted_count
        )

    with col3:

        st.metric(
            "Resolved",
            resolved_count
        )

    # --------------------------------------------------------
    # COMPLAINT TABLE
    # --------------------------------------------------------

    st.markdown(
        "### 📊 Complaint Records"
    )

    if filtered_complaints.empty:

        st.warning(
            "No complaints match your filters."
        )

    else:

        display_columns = [
            "complaint_id",
            "created_at",
            "category",
            "severity",
            "description",
            "location",
            "status",
        ]

        st.dataframe(
            filtered_complaints[
                display_columns
            ],
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    if st.button(
        "🔄 Refresh Complaints",
        key="refresh_complaints"
    ):

        st.rerun()



# ============================================================
# ADMIN / AUTHORITY STATUS MANAGEMENT
# ============================================================

st.markdown("---")

st.header("🛠️ Complaint Status Management")

st.write(
    "Update the current status of a submitted civic complaint."
)

management_df = load_complaints()

if management_df.empty:

    st.info(
        "No complaints are available for status management."
    )

else:

    complaint_ids = (
        management_df[
            "complaint_id"
        ]
        .astype(str)
        .tolist()
    )

    selected_complaint = st.selectbox(
        "Select Complaint",
        complaint_ids,
        key="status_complaint_id"
    )

    selected_row = management_df[
        management_df["complaint_id"].astype(str)
        == selected_complaint
    ]

    if not selected_row.empty:

        row = selected_row.iloc[0]

        st.markdown("### Complaint Details")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Category:** {row['category']}"
            )

            st.write(
                f"**Severity:** {row['severity']}"
            )

            st.write(
                f"**Status:** {row['status']}"
            )

        with col2:

            st.write(
                f"**Location:** {row['location']}"
            )

            st.write(
                f"**Created:** {row['created_at']}"
            )

        st.write(
            f"**Description:** {row['description']}"
        )

        new_status = st.selectbox(
            "Update Status",
            [
                "Submitted",
                "Under Review",
                "In Progress",
                "Resolved",
                "Rejected",
            ],
            index=[
                "Submitted",
                "Under Review",
                "In Progress",
                "Resolved",
                "Rejected",
            ].index(
                row["status"]
            ),
            key="new_complaint_status"
        )

        if st.button(
            "🔄 Update Complaint Status",
            key="update_complaint_status"
        ):

            success = update_complaint_status(
                selected_complaint,
                new_status
            )

            if success:

                st.success(
                    f"Complaint {selected_complaint} "
                    f"updated to '{new_status}'."
                )

                st.rerun()

            else:

                st.error(
                    "Unable to update complaint status."
                )


# ============================================================
# CIVIC MAP
# ============================================================

st.markdown("---")

st.header("🗺️ Civic Issue Map")

st.write(
    "Explore reported civic issues by geographic location."
)

map_df = load_map_complaints()

if map_df.empty:

    st.info(
        "No complaints with valid coordinates "
        "are available for the map yet."
    )

else:

    st.markdown("### 🔎 Map Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        category_options = [
            "All"
        ] + sorted(
            map_df["category"]
            .dropna()
            .unique()
            .tolist()
        )

        map_category = st.selectbox(
            "🏷️ Category",
            category_options,
            key="map_category_filter"
        )

    with col2:
        severity_options = [
            "All",
            "Low",
            "Medium",
            "High",
            "Critical",
        ]

        map_severity = st.selectbox(
            "🚨 Severity",
            severity_options,
            key="map_severity_filter"
        )

    with col3:
        status_options = [
            "All"
        ] + sorted(
            map_df["status"]
            .dropna()
            .unique()
            .tolist()
        )

        map_status = st.selectbox(
            "🚦 Status",
            status_options,
            key="map_status_filter"
        )

    # CREATE filtered data FIRST
    filtered_map_df = filter_map_complaints(
        map_df,
        category=map_category,
        severity=map_severity,
        status=map_status,
    )

    # NOW statistics can use it
    stats = get_map_statistics(
        filtered_map_df
    )

    # NOW insights can use it
    insights = get_location_insights(
        filtered_map_df
    )



    # --------------------------------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------------------------------

    with col1:

        st.markdown(
            "#### 🏷️ Complaints by Category"
        )

        category_counts = (
            filtered_map_df["category"]
            .value_counts()
        )

        st.bar_chart(
            category_counts
        )

    # --------------------------------------------------------
    # SEVERITY ANALYSIS
    # --------------------------------------------------------

    with col2:

        st.markdown(
            "#### 🚨 Complaints by Severity"
        )

        severity_counts = (
            filtered_map_df["severity"]
            .value_counts()
        )

        st.bar_chart(
            severity_counts
        )

    # --------------------------------------------------------
    # STATUS ANALYSIS
    # --------------------------------------------------------

    st.markdown(
        "#### 🚦 Complaint Status Distribution"
    )

    status_counts = (
        filtered_map_df["status"]
        .value_counts()
    )

    st.bar_chart(
        status_counts
    )
    
# ============================================================
# DESCRIPTION
# ============================================================

vision_description = st.text_area(
    "Optional additional description",
    placeholder=(
        "Example: This pothole is located near "
        "the community park."
    ),
    height=100,
    key="vision_description",
)


# ============================================================
# SELECT IMAGE
# ============================================================

selected_image = (
    camera_image
    if camera_image is not None
    else uploaded_image
)


# ============================================================
# ANALYZE IMAGE
# ============================================================

if selected_image is not None:

    st.markdown(
        "### 🔎 Selected Image"
    )

    st.image(
        selected_image,
        caption="Civic issue image",
        use_container_width=True,
    )


    analyze_button = st.button(
        "🤖 Analyze Image with Gemini",
        type="primary",
    )


    if analyze_button:

        with st.spinner(
            "Gemini Vision is analyzing the image..."
        ):

            try:

                image_bytes = selected_image.getvalue()

                mime_type = (
                    selected_image.type
                    or "image/jpeg"
                )

                vision_result = analyze_civic_image(
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    description=vision_description,
                )

                st.markdown(
                    "### 🧠 AI Vision Analysis"
                )

                st.success(
                    "Image analysis completed."
                )

                st.markdown(
                    vision_result
                )


            except Exception as e:

                st.error(
                    "Unable to analyze the image."
                )

                st.caption(
                    f"Technical details: {str(e)}"
                )

else:

    st.info(
        "📷 Capture an image or 🖼️ upload an image "
        "to start the AI vision analysis."
    )


# ============================================================
# AI PROCESSING
# ============================================================

if submitted:

    if not description.strip():

        st.warning(
            "Please describe the civic issue first."
        )

    else:

        try:

            # ------------------------------------------------
            # ISSUE ANALYSIS
            # ------------------------------------------------

            with st.spinner(
                "Gemini is analyzing the civic issue..."
            ):

                issue_analysis = analyze_issue(
                    description
                )

            st.markdown(
                "### 🔍 AI Issue Analysis"
            )

            st.info(
                issue_analysis
            )


            # ------------------------------------------------
            # SEVERITY ANALYSIS
            # ------------------------------------------------

            with st.spinner(
                "Assessing issue severity..."
            ):

                severity_analysis = analyze_severity(
                    issue=description,
                    category="Civic Issue",
                    location=location or "Not specified",
                )

            st.markdown(
                "### 🚨 Severity Assessment"
            )

            st.warning(
                severity_analysis
            )


            # ------------------------------------------------
            # RECOMMENDATION
            # ------------------------------------------------

            with st.spinner(
                "Generating recommendation..."
            ):

                recommendation = generate_recommendation(
                    issue=description,
                    category="Civic Issue",
                    severity=severity_analysis,
                )

            st.markdown(
                "### 💡 AI Recommendation"
            )

            st.success(
                recommendation
            )


        except Exception as e:

            st.error(
                "Unable to complete AI analysis."
            )

            st.caption(
                f"Technical details: {str(e)}"
            )



# ============================================================
# ISSUE TABLE
# ============================================================

st.markdown(
    '<div class="section-title">📋 Civic Issue Registry</div>',
    unsafe_allow_html=True,
)

display_df = filtered_df[
    [
        "issue_id",
        "date",
        "category",
        "severity",
        "status",
        "priority",
        "description",
    ]
].copy()

display_df["date"] = display_df["date"].dt.strftime(
    "%Y-%m-%d"
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# EXPANDER
# ============================================================

with st.expander("ℹ️ About AI CivicAssist"):

    st.write(
        """
        AI CivicAssist is a multimodal civic intelligence
        platform designed to transform community observations
        into structured, actionable civic reports.

        Future versions will integrate Gemini AI for:

        • Image-based civic issue detection
        • Voice-to-report conversion
        • Severity analysis
        • Smart recommendations
        • AI-generated reports
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI CivicAssist • MirAI Capstone Project • final"
)