import pandas as pd


def load_civic_data(file_path: str) -> pd.DataFrame:
    """Load civic issue data from CSV."""

    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(df["date"])

    return df


def filter_civic_data(
    df: pd.DataFrame,
    category: str = "All",
    severity: str = "All",
    status: str = "All",
) -> pd.DataFrame:

    filtered = df.copy()

    if category != "All":
        filtered = filtered[
            filtered["category"] == category
        ]

    if severity != "All":
        filtered = filtered[
            filtered["severity"] == severity
        ]

    if status != "All":
        filtered = filtered[
            filtered["status"] == status
        ]

    return filtered


def calculate_metrics(df: pd.DataFrame) -> dict:

    total = len(df)

    high_priority = len(
        df[df["priority"].isin(["High", "Critical"])]
    )

    resolved = len(
        df[df["status"] == "Resolved"]
    )

    open_issues = len(
        df[df["status"] == "Open"]
    )

    resolution_rate = (
        (resolved / total) * 100
        if total > 0
        else 0
    )

    return {
        "total": total,
        "high_priority": high_priority,
        "resolved": resolved,
        "open": open_issues,
        "resolution_rate": resolution_rate,
    }