from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

COMPLAINT_FILE = (
    PROJECT_ROOT
    / "data"
    / "complaints.csv"
)


# ============================================================
# LOAD MAP COMPLAINTS
# ============================================================

def load_map_complaints():
    """Load complaints containing valid geographic coordinates."""

    if not COMPLAINT_FILE.exists():
        return pd.DataFrame()

    df = pd.read_csv(
        COMPLAINT_FILE
    )

    if df.empty:
        return df

    # Convert coordinates to numbers
    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    # Keep only complaints with valid coordinates
    df = df.dropna(
        subset=[
            "latitude",
            "longitude"
        ]
    )

    return df


# ============================================================
# FILTER MAP COMPLAINTS
# ============================================================

def filter_map_complaints(
    df,
    category="All",
    severity="All",
    status="All",
):
    """Filter complaints for map visualization."""

    filtered_df = df.copy()

    if category != "All":

        filtered_df = filtered_df[
            filtered_df["category"]
            == category
        ]

    if severity != "All":

        filtered_df = filtered_df[
            filtered_df["severity"]
            == severity
        ]

    if status != "All":

        filtered_df = filtered_df[
            filtered_df["status"]
            == status
        ]

    return filtered_df


# ============================================================
# MAP STATISTICS
# ============================================================

def get_map_statistics(df):
    """Generate location-based complaint statistics."""

    if df.empty:

        return {
            "total": 0,
            "high_priority": 0,
            "open": 0,
            "resolved": 0,
        }

    # High and Critical complaints
    high_priority = len(
        df[
            df["severity"].isin(
                [
                    "High",
                    "Critical"
                ]
            )
        ]
    )

    # Resolved complaints
    resolved = len(
        df[
            df["status"]
            == "Resolved"
        ]
    )

    # Open complaints
    open_complaints = len(
        df[
            ~df["status"].isin(
                [
                    "Resolved",
                    "Rejected"
                ]
            )
        ]
    )

    return {
        "total": len(df),
        "high_priority": high_priority,
        "open": open_complaints,
        "resolved": resolved,
    }


# ============================================================
# CIVIC LOCATION INSIGHTS
# ============================================================

def get_location_insights(df):
    """Generate useful insights from mapped civic complaints."""

    if df.empty:

        return {
            "top_category": "N/A",
            "top_location": "N/A",
            "top_location_count": 0,
            "critical_count": 0,
        }

    # --------------------------------------------------------
    # MOST REPORTED CATEGORY
    # --------------------------------------------------------

    if "category" in df.columns:

        category_counts = (
            df["category"]
            .value_counts()
        )

        if not category_counts.empty:

            top_category = (
                category_counts.index[0]
            )

        else:

            top_category = "N/A"

    else:

        top_category = "N/A"

    # --------------------------------------------------------
    # MOST AFFECTED LOCATION
    # --------------------------------------------------------

    if "location" in df.columns:

        location_counts = (
            df["location"]
            .value_counts()
        )

        if not location_counts.empty:

            top_location = (
                location_counts.index[0]
            )

            top_location_count = int(
                location_counts.iloc[0]
            )

        else:

            top_location = "N/A"
            top_location_count = 0

    else:

        top_location = "N/A"
        top_location_count = 0

    # --------------------------------------------------------
    # HIGH / CRITICAL PRIORITY
    # --------------------------------------------------------

    if "severity" in df.columns:

        critical_count = len(
            df[
                df["severity"].isin(
                    [
                        "High",
                        "Critical"
                    ]
                )
            ]
        )

    else:

        critical_count = 0

    return {
        "top_category": top_category,
        "top_location": top_location,
        "top_location_count": top_location_count,
        "critical_count": critical_count,
    }