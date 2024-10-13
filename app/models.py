from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from utils.log import Log  # Import the Log class for logging

try:
    class Campaign(Base):
        __tablename__ = 'campaign'
        campaign_id = Column(Integer, primary_key=True, index=True)
        campaign_name = Column(String, index=True)
        campaign_type = Column(String)

    class AdGroup(Base):
        __tablename__ = 'ad_group'
        ad_group_id = Column(Integer, primary_key=True, index=True)
        ad_group_name = Column(String)
        campaign_id = Column(Integer, ForeignKey('campaign.campaign_id'))
        campaign = relationship('Campaign', back_populates='ad_groups')

    class AdGroupStats(Base):
        __tablename__ = 'ad_group_stats'
        stats_id = Column(Integer, primary_key=True, index=True)
        date = Column(Date)
        ad_group_id = Column(Integer, ForeignKey('ad_group.ad_group_id'))
        device = Column(String)
        impressions = Column(Float)
        clicks = Column(Integer)
        conversions = Column(Float)
        cost = Column(Float)
        ad_group = relationship('AdGroup', back_populates='stats')

    # Set up relationships
    Campaign.ad_groups = relationship('AdGroup', back_populates='campaign')
    AdGroup.stats = relationship('AdGroupStats', back_populates='ad_group')

    Log.INFO("Models Campaign, AdGroup, and AdGroupStats were successfully defined.")

except Exception as e:
    Log.ERROR(f"Error defining SQLAlchemy models: {str(e)}")
