from pathlib import Path
from datetime import datetime
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

COMPLAINT_FILE = (
    PROJECT_ROOT
    / "data"
    / "complaints.csv"
)


COLUMNS = [
    "complaint_id",
    "created_at",
    "category",
    "severity",
    "description",
    "location",
    "latitude",
    "longitude",
    "status",
]


def initialize_complaints_file():

    COMPLAINT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not COMPLAINT_FILE.exists():

        df = pd.DataFrame(
            columns=COLUMNS
        )

        df.to_csv(
            COMPLAINT_FILE,
            index=False
        )


def generate_complaint_id():

    initialize_complaints_file()

    df = pd.read_csv(
        COMPLAINT_FILE
    )

    year = datetime.now().year

    next_number = len(df) + 1

    return f"CA-{year}-{next_number:04d}"


def create_complaint(
    category,
    severity,
    description,
    location="",
    latitude="",
    longitude="",
):
    initialize_complaints_file()

    complaint_id = generate_complaint_id()

    complaint = {
        "complaint_id": complaint_id,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "category": category,
        "severity": severity,
        "description": description,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "status": "Submitted",
    }

    df = pd.DataFrame(
        [complaint]
    )

    df.to_csv(
        COMPLAINT_FILE,
        mode="a",
        header=False,
        index=False
    )

    return complaint


def load_complaints():

    initialize_complaints_file()

    df = pd.read_csv(COMPLAINT_FILE)

    # Ensure all required columns exist
    for column in COLUMNS:

        if column not in df.columns:

            if column == "status":
                df[column] = "Submitted"

            else:
                df[column] = ""

    # Keep columns in the correct order
    df = df[COLUMNS]

    df.to_csv(
        COMPLAINT_FILE,
        index=False
    )

    return df

def update_complaint_status(
    complaint_id,
    new_status
):
    """Update the status of an existing complaint."""

    initialize_complaints_file()

    df = pd.read_csv(
        COMPLAINT_FILE
    )

    if df.empty:
        return False

    if complaint_id not in df[
        "complaint_id"
    ].astype(str).values:

        return False

    allowed_statuses = [
        "Submitted",
        "Under Review",
        "In Progress",
        "Resolved",
        "Rejected",
    ]

    if new_status not in allowed_statuses:
        return False

    df.loc[
        df["complaint_id"].astype(str)
        == str(complaint_id),
        "status"
    ] = new_status

    df.to_csv(
        COMPLAINT_FILE,
        index=False
    )

    return True

    initialize_complaints_file()

    df = pd.read_csv(
        COMPLAINT_FILE
    )

    if complaint_id not in df[
        "complaint_id"
    ].values:

        return False

    df.loc[
        df["complaint_id"] == complaint_id,
        "status"
    ] = new_status

    df.to_csv(
        COMPLAINT_FILE,
        index=False
    )

    return True

def get_location_insights(df):
    """Generate useful insights from mapped civic complaints."""

    if df.empty:
        return {
            "top_category": "N/A",
            "top_location": "N/A",
            "top_location_count": 0,
            "critical_count": 0,
        }

    # Most reported category
    if "category" in df.columns:
        category_counts = df["category"].value_counts()

        top_category = (
            category_counts.index[0]
            if not category_counts.empty
            else "N/A"
        )
    else:
        top_category = "N/A"

    # Most affected location
    if "location" in df.columns:
        location_counts = df["location"].value_counts()

        if not location_counts.empty:
            top_location = location_counts.index[0]
            top_location_count = int(
                location_counts.iloc[0]
            )
        else:
            top_location = "N/A"
            top_location_count = 0

    else:
        top_location = "N/A"
        top_location_count = 0

    # Critical/high-priority complaints
    critical_count = len(
        df[
            df["severity"].isin(
                ["High", "Critical"]
            )
        ]
    )

    return {
        "top_category": top_category,
        "top_location": top_location,
        "top_location_count": top_location_count,
        "critical_count": critical_count,
    }