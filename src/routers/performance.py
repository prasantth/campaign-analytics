from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.analytics.analytics import get_performance_data, calculate_percentage_change
from src.database.database import get_db
from datetime import datetime, timedelta
from typing import Optional, List
from src.models.models import AdGroupStats
from src.utils.log import Log  # Import the Log class for logging

router = APIRouter()

@router.get("/performance-time-series")
def performance_time_series(
    aggregate_by: str = Query(..., pattern="^(day|week|month)$"),
    campaigns: Optional[List[int]] = Query(None),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        # Parse dates if provided
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

        # Build and execute the query for time series data
        query = db.query(
            func.date_trunc(aggregate_by, AdGroupStats.date).label('period'),
            func.sum(AdGroupStats.cost).label('total_cost'),
            func.sum(AdGroupStats.clicks).label('total_clicks'),
            func.sum(AdGroupStats.conversions).label('total_conversions'),
            func.sum(AdGroupStats.impressions).label('total_impressions')
        )

        if campaigns:
            query = query.filter(AdGroupStats.ad_group_id.in_(campaigns))

        if start_date_dt:
            query = query.filter(AdGroupStats.date >= start_date_dt)
        if end_date_dt:
            query = query.filter(AdGroupStats.date <= end_date_dt)

        query = query.group_by('period').order_by(func.date_trunc(aggregate_by, AdGroupStats.date).desc())
        results = query.all()

        time_series_data = []
        for result in results:
            total_clicks = result.total_clicks
            total_conversions = result.total_conversions
            total_impressions = result.total_impressions
            total_cost = result.total_cost

            avg_cost_per_click = round(total_cost / total_clicks if total_clicks else 0, 2)
            avg_cost_per_conversion = round(total_cost / total_conversions if total_conversions else 0, 2)
            avg_ctr = round(total_clicks / total_impressions if total_impressions else 0, 2)
            avg_conversion_rate = round(total_conversions / total_clicks if total_clicks else 0, 2)

            time_series_data.append({
                "period": result.period,
                "total_cost": total_cost,
                "total_clicks": total_clicks,
                "total_conversions": total_conversions,
                "avg_cost_per_click": avg_cost_per_click,
                "avg_cost_per_conversion": avg_cost_per_conversion,
                "avg_click_through_rate": avg_ctr,
                "avg_conversion_rate": avg_conversion_rate,
            })

        Log.INFO("Performance time series data retrieved successfully.")
        return {"data": time_series_data}

    except Exception as e:
        Log.ERROR(f"Error retrieving performance time series: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/compare-performance")
def compare_performance(
    start_date: str,
    end_date: str,
    compare_mode: str = Query(..., pattern="^(preceding|previous_month)$"),
    db: Session = Depends(get_db)
):
    try:
        # Parse dates
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        current_period_days = (end_date_dt - start_date_dt).days + 1

        before_start_date_dt = None
        before_end_date_dt = None

        # Determine the 'before' period based on compare_mode
        if compare_mode == 'preceding':
            before_start_date_dt = start_date_dt - timedelta(days=current_period_days)
            before_end_date_dt = start_date_dt - timedelta(days=1)
        elif compare_mode == 'previous_month':
            before_start_date_dt = start_date_dt.replace(month=start_date_dt.month - 1)
            before_end_date_dt = end_date_dt.replace(month=end_date_dt.month - 1)

        # Fetch data for current and before periods
        current_data = get_performance_data(db, start_date_dt, end_date_dt)
        before_data = get_performance_data(db, before_start_date_dt, before_end_date_dt)

        # Calculate percentage change
        comparison_data = calculate_percentage_change(current_data, before_data)

        Log.INFO("Performance comparison data retrieved successfully.")
        return {"current_period": current_data, "before_period": before_data, "comparison": comparison_data}

    except Exception as e:
        Log.ERROR(f"Error comparing performance: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
