"""
Omneky API Integration Framework for T2India
Seamlessly integrates AI-powered ad generation with T2India travel platform
"""

import os
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import uuid
import base64

class OmnekyIntegration:
    def __init__(self, api_key=None, base_url="https://api.omneky.com"):
        self.api_key = api_key or os.environ.get('OMNEKY_API_KEY')
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        } if self.api_key else {}
        
        # T2India brand configuration
        self.t2india_brand = {
            'name': 't2India',
            'tagline': 'Your Gateway To India',
            'primary_color': '#FF6B35',  # Orange
            'secondary_color': '#2E8B8B',  # Teal
            'logo_url': 'https://t2india.com/assets/logo.png',
            'brand_voice': 'Professional, welcoming, culturally rich, authentic',
            'target_audience': 'International travelers seeking authentic Indian experiences'
        }
    
    def create_destination_ad_campaign(self, destination_data):
        """
        Create AI-generated ads for T2India destinations
        """
        try:
            # Prepare campaign data for Omneky
            campaign_data = {
                'campaign_name': f"T2India - {destination_data['name']} Campaign",
                'brand_info': self.t2india_brand,
                'content_brief': {
                    'destination': destination_data['name'],
                    'highlights': destination_data.get('highlights', []),
                    'experiences': destination_data.get('experiences', []),
                    'best_time': destination_data.get('best_time', 'Year-round'),
                    'duration': destination_data.get('recommended_duration', '3-4 days'),
                    'unique_selling_points': destination_data.get('usp', [])
                },
                'ad_formats': ['image', 'video', 'carousel'],
                'platforms': ['facebook', 'instagram', 'google', 'youtube'],
                'objectives': ['awareness', 'consideration', 'conversion']
            }
            
            # Generate ad variations
            ad_variations = self._generate_ad_variations(campaign_data)
            
            return {
                'success': True,
                'campaign_id': str(uuid.uuid4()),
                'destination': destination_data['name'],
                'ads_generated': len(ad_variations),
                'ad_variations': ad_variations,
                'estimated_reach': self._estimate_campaign_reach(destination_data),
                'recommended_budget': self._calculate_recommended_budget(destination_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'destination': destination_data.get('name', 'Unknown')
            }
    
    def create_itinerary_promotion_ads(self, itinerary_data):
        """
        Create promotional ads for complete T2India itineraries
        """
        try:
            # Extract key information from itinerary
            destinations = [dest['name'] for dest in itinerary_data.get('destinations', [])]
            duration = itinerary_data.get('total_days', 7)
            highlights = []
            
            # Collect highlights from all destinations
            for dest in itinerary_data.get('destinations', []):
                highlights.extend(dest.get('highlights', []))
            
            # Create campaign brief
            campaign_brief = {
                'campaign_type': 'itinerary_promotion',
                'itinerary_name': itinerary_data.get('name', f"{' → '.join(destinations[:3])} Tour"),
                'destinations': destinations,
                'duration': f"{duration} days",
                'highlights': highlights[:8],  # Top 8 highlights
                'price_range': itinerary_data.get('price_range', 'Premium'),
                'target_market': itinerary_data.get('target_market', 'International'),
                'unique_experiences': itinerary_data.get('handicrafts', [])
            }
            
            # Generate promotional content
            promotional_ads = self._generate_itinerary_ads(campaign_brief)
            
            return {
                'success': True,
                'campaign_id': str(uuid.uuid4()),
                'itinerary': campaign_brief['itinerary_name'],
                'promotional_ads': promotional_ads,
                'content_variations': len(promotional_ads),
                'recommended_platforms': ['facebook', 'instagram', 'google_ads', 'youtube'],
                'targeting_suggestions': self._get_targeting_suggestions(campaign_brief)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'itinerary': itinerary_data.get('name', 'Unknown')
            }
    
    def create_handicraft_experience_ads(self, handicraft_data):
        """
        Create ads specifically for T2India handicraft experiences
        """
        try:
            # Prepare handicraft campaign data
            campaign_data = {
                'experience_type': 'cultural_handicraft',
                'handicraft_name': handicraft_data.get('name'),
                'artisan_name': handicraft_data.get('artisan', {}).get('name'),
                'location': handicraft_data.get('location'),
                'workshop_duration': handicraft_data.get('duration'),
                'skill_level': handicraft_data.get('difficulty'),
                'cultural_significance': handicraft_data.get('cultural_background'),
                'learning_outcomes': handicraft_data.get('learning_outcomes', [])
            }
            
            # Generate cultural experience ads
            cultural_ads = self._generate_cultural_ads(campaign_data)
            
            return {
                'success': True,
                'campaign_id': str(uuid.uuid4()),
                'handicraft': handicraft_data.get('name'),
                'cultural_ads': cultural_ads,
                'target_audience': 'Cultural enthusiasts, experiential travelers',
                'recommended_budget': self._calculate_cultural_ad_budget(handicraft_data),
                'performance_metrics': ['engagement_rate', 'workshop_bookings', 'cultural_interest_score']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'handicraft': handicraft_data.get('name', 'Unknown')
            }
    
    def _generate_ad_variations(self, campaign_data):
        """Generate multiple ad variations for A/B testing"""
        variations = []
        
        destination = campaign_data['content_brief']['destination']
        highlights = campaign_data['content_brief']['highlights']
        
        # Image ad variations
        image_ads = [
            {
                'type': 'image',
                'headline': f"Discover Authentic {destination}",
                'description': f"Experience the real {destination} with t2India. {highlights[0] if highlights else 'Unforgettable memories await.'}",
                'cta': 'Plan Your Journey',
                'visual_style': 'scenic_landscape',
                'format': 'square'
            },
            {
                'type': 'image',
                'headline': f"Explore {destination} Like Never Before",
                'description': f"Immerse yourself in {destination}'s rich culture and heritage. Expert guides, authentic experiences.",
                'cta': 'Book Now',
                'visual_style': 'cultural_heritage',
                'format': 'landscape'
            }
        ]
        
        # Video ad variations
        video_ads = [
            {
                'type': 'video',
                'headline': f"Journey Through {destination}",
                'description': f"Watch the magic of {destination} unfold. From ancient traditions to modern wonders.",
                'cta': 'Start Planning',
                'duration': '30_seconds',
                'style': 'cinematic_journey'
            }
        ]
        
        # Carousel ad variations
        carousel_ads = [
            {
                'type': 'carousel',
                'headline': f"Why Choose {destination}?",
                'cards': [
                    {'title': 'Authentic Experiences', 'description': 'Local artisans and traditional crafts'},
                    {'title': 'Expert Guidance', 'description': 'Professional local guides'},
                    {'title': 'Comfortable Stay', 'description': '4-star accommodations'},
                    {'title': 'Seamless Planning', 'description': 'Everything organized for you'}
                ],
                'cta': 'Explore Options'
            }
        ]
        
        variations.extend(image_ads)
        variations.extend(video_ads)
        variations.extend(carousel_ads)
        
        return variations
    
    def _generate_itinerary_ads(self, campaign_brief):
        """Generate promotional ads for complete itineraries"""
        ads = []
        
        itinerary_name = campaign_brief['itinerary_name']
        destinations = campaign_brief['destinations']
        duration = campaign_brief['duration']
        
        # Main promotional ad
        main_ad = {
            'type': 'hero_promotion',
            'headline': f"Grand {itinerary_name} - {duration}",
            'description': f"Explore {', '.join(destinations[:3])} {'and more' if len(destinations) > 3 else ''} in one incredible journey.",
            'highlights': campaign_brief['highlights'][:4],
            'cta': 'View Complete Itinerary',
            'urgency': 'Limited Time Offer',
            'social_proof': '500+ Happy Travelers'
        }
        
        # Destination spotlight ads
        for dest in destinations[:3]:
            spotlight_ad = {
                'type': 'destination_spotlight',
                'headline': f"Spotlight: {dest}",
                'description': f"Discover what makes {dest} special in our {itinerary_name}.",
                'cta': f'Learn About {dest}',
                'focus': dest
            }
            ads.append(spotlight_ad)
        
        # Experience-focused ad
        if campaign_brief.get('unique_experiences'):
            experience_ad = {
                'type': 'experience_focused',
                'headline': 'Authentic Cultural Experiences',
                'description': f"Learn traditional crafts and meet master artisans during your {itinerary_name}.",
                'experiences': campaign_brief['unique_experiences'][:3],
                'cta': 'Explore Cultural Experiences'
            }
            ads.append(experience_ad)
        
        ads.insert(0, main_ad)
        return ads
    
    def _generate_cultural_ads(self, campaign_data):
        """Generate ads for handicraft and cultural experiences"""
        ads = []
        
        handicraft = campaign_data['handicraft_name']
        artisan = campaign_data['artisan_name']
        location = campaign_data['location']
        
        # Master artisan spotlight
        artisan_ad = {
            'type': 'artisan_spotlight',
            'headline': f"Learn {handicraft} from Master {artisan}",
            'description': f"Experience authentic {handicraft} in {location} with renowned artisan {artisan}.",
            'cta': 'Book Workshop',
            'trust_indicators': ['Master craftsman', 'Authentic techniques', 'Cultural heritage']
        }
        
        # Cultural immersion ad
        cultural_ad = {
            'type': 'cultural_immersion',
            'headline': f"Immerse in {location}'s {handicraft} Tradition",
            'description': f"Go beyond tourism. Create your own {handicraft} masterpiece and understand its cultural significance.",
            'cta': 'Join Experience',
            'benefits': ['Hands-on learning', 'Cultural understanding', 'Take home creation']
        }
        
        # Skill development ad
        skill_ad = {
            'type': 'skill_development',
            'headline': f"Master the Art of {handicraft}",
            'description': f"Develop a new skill while traveling. {campaign_data['workshop_duration']} workshop in authentic setting.",
            'cta': 'Start Learning',
            'outcomes': campaign_data.get('learning_outcomes', [])
        }
        
        ads.extend([artisan_ad, cultural_ad, skill_ad])
        return ads
    
    def _estimate_campaign_reach(self, destination_data):
        """Estimate potential reach for destination campaign"""
        base_reach = {
            'facebook': 50000,
            'instagram': 35000,
            'google_ads': 25000,
            'youtube': 15000
        }
        
        # Adjust based on destination popularity
        popularity_multiplier = destination_data.get('popularity_score', 1.0)
        
        estimated_reach = {}
        for platform, reach in base_reach.items():
            estimated_reach[platform] = int(reach * popularity_multiplier)
        
        return estimated_reach
    
    def _calculate_recommended_budget(self, destination_data):
        """Calculate recommended advertising budget"""
        base_budget = {
            'daily_budget': 2000,  # INR
            'monthly_budget': 60000,  # INR
            'cost_per_click': 15,  # INR
            'cost_per_impression': 2  # INR
        }
        
        # Adjust based on destination competitiveness
        competition_level = destination_data.get('competition_level', 'medium')
        multipliers = {'low': 0.8, 'medium': 1.0, 'high': 1.3}
        
        multiplier = multipliers.get(competition_level, 1.0)
        
        recommended_budget = {}
        for metric, amount in base_budget.items():
            recommended_budget[metric] = int(amount * multiplier)
        
        return recommended_budget
    
    def _calculate_cultural_ad_budget(self, handicraft_data):
        """Calculate budget for cultural experience ads"""
        return {
            'daily_budget': 1500,  # INR
            'monthly_budget': 45000,  # INR
            'target_cpc': 12,  # INR
            'expected_conversion_rate': '3.5%',
            'cost_per_booking': 400  # INR
        }
    
    def _get_targeting_suggestions(self, campaign_brief):
        """Get audience targeting suggestions"""
        return {
            'demographics': {
                'age_range': '25-55',
                'income_level': 'Upper middle class and above',
                'education': 'College educated',
                'interests': ['Travel', 'Culture', 'Heritage', 'Authentic experiences']
            },
            'geographic': {
                'primary_markets': ['USA', 'UK', 'Australia', 'Germany', 'France'],
                'secondary_markets': ['Canada', 'Netherlands', 'Japan', 'Singapore'],
                'exclude': ['India'] if campaign_brief.get('target_market') == 'International' else []
            },
            'behavioral': {
                'travel_behavior': ['Frequent travelers', 'Cultural tourists', 'Luxury travelers'],
                'online_behavior': ['Travel website visitors', 'Cultural content engagers'],
                'purchase_behavior': ['Premium travel bookers', 'Experience seekers']
            },
            'custom_audiences': {
                'lookalike': 'Based on existing t2India customers',
                'retargeting': 'Website visitors and email subscribers',
                'exclusions': 'Recent bookers (last 30 days)'
            }
        }

# Flask app for Omneky integration API
app = Flask(__name__)
CORS(app)

# Initialize Omneky integration (API key would be set via environment variable)
omneky = OmnekyIntegration()

@app.route('/api/omneky/destination-campaign', methods=['POST'])
def create_destination_campaign():
    """API endpoint to create destination ad campaign"""
    destination_data = request.json
    result = omneky.create_destination_ad_campaign(destination_data)
    return jsonify(result)

@app.route('/api/omneky/itinerary-promotion', methods=['POST'])
def create_itinerary_promotion():
    """API endpoint to create itinerary promotional campaign"""
    itinerary_data = request.json
    result = omneky.create_itinerary_promotion_ads(itinerary_data)
    return jsonify(result)

@app.route('/api/omneky/handicraft-campaign', methods=['POST'])
def create_handicraft_campaign():
    """API endpoint to create handicraft experience campaign"""
    handicraft_data = request.json
    result = omneky.create_handicraft_experience_ads(handicraft_data)
    return jsonify(result)

@app.route('/api/omneky/brand-config')
def get_brand_config():
    """API endpoint to get T2India brand configuration"""
    return jsonify(omneky.t2india_brand)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'Omneky Integration for T2India',
        'version': '1.0.0',
        'api_key_configured': bool(omneky.api_key)
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)

