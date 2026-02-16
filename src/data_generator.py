"""Synthetic sales-funnel / user-event dataset generator.

Produces an event-level CSV with these columns:
- user_id, session_id, event_time, stage, channel, device, order_value

Usage:
    python src/data_generator.py --n-users 5000 --out data/synthetic_funnel.csv
"""
from __future__ import annotations
import argparse
import uuid
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

STAGES = [
    "landing",
    "signup",
    "activation",
    "add_to_cart",
    "checkout",
    "purchase",
]

CHANNELS = ["organic", "paid_search", "email", "social", "affiliate"]
DEVICES = ["desktop", "mobile", "tablet"]

BASE_PROBS = {
    ("landing", "signup"): 0.28,
    ("signup", "activation"): 0.60,
    ("activation", "add_to_cart"): 0.38,
    ("add_to_cart", "checkout"): 0.52,
    ("checkout", "purchase"): 0.62,
}

CHANNEL_MULTIPLIER = {
    "organic": 1.05,
    "paid_search": 0.95,
    "email": 1.20,
    "social": 0.85,
    "affiliate": 0.90,
}


def _next_timestamp(prev_ts, scale_minutes=60):
    """Return next timestamp by adding an exponential wait (in minutes)."""
    delta_min = max(1, np.random.exponential(scale_minutes))
    return prev_ts + timedelta(minutes=float(delta_min))


def generate_synthetic_funnel(n_users=5000, start_date: str = "2025-01-01", days=90, seed: int | None = 42) -> pd.DataFrame:
    np.random.seed(seed)
    users = []
    start_dt = datetime.fromisoformat(start_date)

    for i in range(n_users):
        user_id = str(uuid.uuid4())[:8]
        # random acquisition day within the window
        acquire_day = start_dt + timedelta(days=int(np.random.uniform(0, days)))
        channel = np.random.choice(CHANNELS, p=[0.40, 0.25, 0.15, 0.15, 0.05])
        device = np.random.choice(DEVICES, p=[0.45, 0.45, 0.10])
        # per-user price sensitivity / A-B group
        ab_group = np.random.choice(["control", "variant"], p=[0.7, 0.3])

        # simulate stage progression
        current_ts = acquire_day + timedelta(minutes=np.random.uniform(0, 60))
        session_id = str(uuid.uuid4())[:8]
        for s_idx, stage in enumerate(STAGES):
            # landing always occurs
            if stage == "landing":
                users.append({
                    "user_id": user_id,
                    "session_id": session_id,
                    "event_time": current_ts,
                    "stage": stage,
                    "channel": channel,
                    "device": device,
                    "ab_group": ab_group,
                    "order_value": np.nan,
                })
                # decide whether to move to next stage
                proceed = np.random.rand() < BASE_PROBS[("landing", "signup")] * CHANNEL_MULTIPLIER[channel]
                if not proceed:
                    break
                current_ts = _next_timestamp(current_ts, scale_minutes=30)
                continue

            # for intermediate stages, check progression probability
            prev_stage = STAGES[s_idx - 1]
            prob = BASE_PROBS[(prev_stage, stage)] * CHANNEL_MULTIPLIER[channel]
            if np.random.rand() < prob:
                # record event
                order_value = np.nan
                if stage == "purchase":
                    # simulate order value (log-normal) with AB-group effect
                    base = np.random.lognormal(mean=3.5, sigma=0.5)
                    if ab_group == "variant":
                        base *= 0.96  # e.g., price change effect
                    order_value = round(float(base), 2)

                users.append({
                    "user_id": user_id,
                    "session_id": session_id,
                    "event_time": current_ts,
                    "stage": stage,
                    "channel": channel,
                    "device": device,
                    "ab_group": ab_group,
                    "order_value": order_value,
                })
                current_ts = _next_timestamp(current_ts, scale_minutes=60)
            else:
                break

    df = pd.DataFrame(users)
    # ensure proper dtypes
    df = df.sort_values("event_time").reset_index(drop=True)
    return df


def save_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-users", type=int, default=5000)
    parser.add_argument("--out", type=str, default="data/synthetic_funnel.csv")
    parser.add_argument("--start-date", type=str, default="2025-01-01")
    parser.add_argument("--days", type=int, default=90)
    args = parser.parse_args()

    df = generate_synthetic_funnel(n_users=args.n_users, start_date=args.start_date, days=args.days)
    save_csv(df, args.out)
    print(f"Saved synthetic funnel with {df['user_id'].nunique()} users to {args.out}")
