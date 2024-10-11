from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Campaign, AdGroup, AdGroupStats
from app.schemas import UpdateCampaignRequest
from app.database import get_db
from sqlalchemy import func

router = APIRouter()

@router.get("/campaigns")
def get_campaigns(db: Session = Depends(get_db)):
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

    return result

@router.patch("/campaigns/update-name/{campaign_id}")
def update_campaign(campaign_id: int, request: UpdateCampaignRequest, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.campaign_name = request.name
    db.commit()

    return {"message": "Campaign name updated successfully"}
