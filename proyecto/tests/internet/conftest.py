"""Fixtures compartidas por los tests de internet_app."""

import pandas as pd
import pytest


@pytest.fixture
def sueno_mini():
    """DataFrame pequeño en memoria: 1 fila válida (U1) y 3 inválidas (U2, U3 y U4)."""
    return pd.DataFrame({
        "user_id": ["U1", "U2", "U3", "U4"],
        "age": [30, 12, 25, 40],                       # U2 tiene 12 años -> inválida
        "gender": ["Male", "Female", "Non-Binary", "Female"],
        "occupation_type": ["Student", "Remote Tech", "Corporate 9-to-5", "Student"],
        "chronotype": ["Night Owl", "Morning Lark", "Intermediate", "Intermediate"],
        "bedtime_phone_minutes": [90, 30, 45, 120],
        "primary_bedtime_app": ["TikTok / Reels", "YouTube", "YouTube", "TikTok / Reels"],
        "screen_brightness_pct": [60, 50, 40, 70],
        "blue_light_filter_active": [1, 0, 2, 1],      # U3 tiene un 2 (solo vale 0 o 1) -> inválida
        "caffeine_post_5pm_mg": [0, 50, 100, 0],
        "physical_activity_min": [30, 20, 40, 10],
        "sleep_latency_min": [30.0, 20.0, 25.0, 60.0],
        "total_sleep_hours": [5.0, 8.0, 7.0, 4.0],
        "deep_sleep_pct": [20.0, 22.0, 21.0, 19.0],
        "rem_sleep_pct": [20.0, 19.0, 18.0, 17.0],
        "morning_alarm_snoozes": [3, 0, 1, 5],
        "next_day_fatigue_score": [7.0, 1.5, 3.0, 9.0],
        "sleep_debt_category": ["Moderate Debt", "Optimal Recovery", "Mild Deficit", "Otra"],  # U4: "Otra" no existe -> inválida
    })
