from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Campaign, AdGroup, AdGroupStats
from app.schemas import UpdateCampaignRequest
from app.database import get_db
from sqlalchemy import func
from utils.log import Log  # Import the Log class for logging

router = APIRouter()

@router.get("/campaigns")
def get_campaigns(db: Session = Depends(get_db)):
    try:
        campaigns = db.query(Campaign).all()

        result = []
        for campaign in campaigns:
            ad_groups = db.query(AdGroup).filter(AdGroup.campaign_id == campaign.campaign_id).all()
            total_cost = 0
            total_conversions = 0

            ad_group_data = []
            for ad_group in ad_groups:
                ad_group_stats = db.query(func.avg(AdGroupStats.cost), func.avg(AdGroupStats.conversions)).filter(
                    AdGroupStats.ad_group_id == ad_group.ad_group_id
                ).all()

                avg_cost = ad_group_stats[0][0] or 0
                avg_conversions = ad_group_stats[0][1] or 0
                total_cost += avg_cost
                total_conversions += avg_conversions

                ad_group_data.append({
                    "ad_group_name": ad_group.ad_group_name,
                    "average_cost": avg_cost,
                    "average_conversions": avg_conversions
                })

            result.append({
                "campaign_name": campaign.campaign_name,
                "number_of_ad_groups": len(ad_groups),
                "ad_groups": ad_group_data,
                "average_monthly_cost": total_cost / len(ad_groups) if ad_groups else 0,
                "average_cost_per_conversion": total_cost / total_conversions if total_conversions > 0 else 0
            })

        Log.INFO("Campaigns retrieved successfully.")
        return result

    except Exception as e:
        Log.ERROR(f"Error retrieving campaigns: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.patch("/campaigns/update-name/{campaign_id}")
def update_campaign(campaign_id: int, request: UpdateCampaignRequest, db: Session = Depends(get_db)):
    try:
        campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()

        if not campaign:
            Log.ERROR(f"Campaign with ID {campaign_id} not found.")
            raise HTTPException(status_code=404, detail="Campaign not found")

        campaign.campaign_name = request.name
        db.commit()

        Log.INFO(f"Campaign name updated successfully for campaign ID {campaign_id}.")
        return {"message": "Campaign name updated successfully"}

    except HTTPException as http_err:
        # Let FastAPI handle HTTPExceptions
        raise http_err

    except Exception as e:
        Log.ERROR(f"Error updating campaign with ID {campaign_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
