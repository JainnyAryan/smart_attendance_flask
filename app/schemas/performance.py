from pydantic import BaseModel


class WhatIfScoreInput(BaseModel):
    active_time_pct: float  # 0-100
    hold_time_pct: float    # 0-100
    avg_transitions: float
    completed_on_time: bool