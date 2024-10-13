from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from src.models.models import AdGroupStats
from src.utils.log import Log  # Import the Log class for logging


def get_performance_data(db: Session, start_date: datetime, end_date: datetime):
    try:
        query = db.query(
            func.sum(AdGroupStats.cost).label("total_cost"),
            func.sum(AdGroupStats.clicks).label("total_clicks"),
            func.sum(AdGroupStats.conversions).label("total_conversions"),
            func.sum(AdGroupStats.impressions).label("total_impressions")
        ).filter(
            AdGroupStats.date >= start_date,
            AdGroupStats.date <= end_date
        )
        result = query.one()

        total_clicks = result.total_clicks or 0
        total_conversions = result.total_conversions or 0
        total_impressions = result.total_impressions or 0
        total_cost = result.total_cost or 0

        avg_cost_per_click = round(total_cost / total_clicks if total_clicks else 0, 2)
        avg_cost_per_conversion = round(total_cost / total_conversions if total_conversions else 0, 2)
        avg_ctr = round((total_clicks / total_impressions if total_impressions else 0) * 100, 2)
        avg_conversion_rate = round(total_conversions / total_clicks if total_clicks else 0, 2)
        cost_per_mille = round((total_cost / total_impressions * 1000) if total_impressions else 0, 2)

        return {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "cost_per_click": avg_cost_per_click,
            "cost_per_conversion": avg_cost_per_conversion,
            "cost_per_mille_impression": cost_per_mille,
            "conversion_rate": avg_conversion_rate * 100,
            "click_through_rate": avg_ctr,
            "total_conversions": total_conversions,
            "total_cost": total_cost,
            "total_clicks": total_clicks
        }

    except Exception as e:
        Log.ERROR(f"Error in get_performance_data: {str(e)}")
        return {"error": "Failed to retrieve performance data"}


def calculate_percentage_change(current, before):
    try:
        comparison = {}
        exclude_keys = {'start_date', 'end_date'}
        for key in current:
            if key in exclude_keys:
                continue
            current_value = current.get(key, 0)
            before_value = before.get(key, 0)

            # Calculate percentage change
            if before_value != 0:
                change = round((((current_value - before_value) / before_value) * 100), 2)
            else:
                change = None  # Use None instead of float('inf') for JSON compatibility

            comparison[key] = {
                "current": current_value,
                "before": before_value,
                "percent_change": change
            }
        return comparison

    except Exception as e:
        Log.ERROR(f"Error in calculate_percentage_change: {str(e)}")
        return {"error": "Failed to calculate percentage change"}
