"""
Enhanced TravMechanix Backend API for Intelligent Search
Supports ambiguity detection and "Suggest & Select" interface
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Ambiguous terms with multiple destination options
AMBIGUOUS_TERMS = {
    'spirituality': {
        'label': 'Spiritual Destination',
        'suggested': 'varanasi',
        'suggested_label': 'Varanasi (Most Popular)',
        'options': [
            {
                'value': 'varanasi',
                'label': 'Varanasi',
                'description': 'Oldest living city, Ganges ghats, spiritual capital of India'
            },
            {
                'value': 'rishikesh',
                'label': 'Rishikesh',
                'description': 'Yoga capital, Himalayan foothills, adventure + spirituality'
            },
            {
                'value': 'ajmer',
                'label': 'Ajmer',
                'description': 'Sufi shrine of Khwaja Moinuddin Chishti, Islamic spirituality'
            },
            {
                'value': 'haridwar',
                'label': 'Haridwar',
                'description': 'Gateway to Gods, Ganga Aarti, Char Dham starting point'
            },
            {
                'value': 'amritsar',
                'label': 'Amritsar',
                'description': 'Golden Temple, Sikh spirituality, Punjab culture'
            }
        ],
        'example': 'Bodh Gaya, Shirdi, Tirupati'
    },
    'desert palaces': {
        'label': 'Desert Palace Destination',
        'suggested': 'jaisalmer',
        'suggested_label': 'Jaisalmer (Golden City)',
        'options': [
            {
                'value': 'jaisalmer',
                'label': 'Jaisalmer',
                'description': 'Golden City, Thar Desert, magnificent havelis and fort'
            },
            {
                'value': 'jodhpur',
                'label': 'Jodhpur',
                'description': 'Blue City, Mehrangarh Fort, gateway to Thar Desert'
            },
            {
                'value': 'bikaner',
                'label': 'Bikaner',
                'description': 'Camel country, Junagarh Fort, desert safaris'
            },
            {
                'value': 'udaipur',
                'label': 'Udaipur',
                'description': 'City of Lakes, Lake Palace, romantic desert city'
            }
        ],
        'example': 'Pushkar, Mandawa, Shekhawati'
    },
    'golden triangle': {
        'label': 'Golden Triangle Route',
        'suggested': 'delhi_agra_jaipur',
        'suggested_label': 'Delhi → Agra → Jaipur (Classic Route)',
        'options': [
            {
                'value': 'delhi_agra_jaipur',
                'label': 'Delhi → Agra → Jaipur',
                'description': 'Classic route: Capital → Taj Mahal → Pink City'
            },
            {
                'value': 'delhi_jaipur_agra',
                'label': 'Delhi → Jaipur → Agra',
                'description': 'Alternative route: Capital → Pink City → Taj Mahal'
            },
            {
                'value': 'agra_delhi_jaipur',
                'label': 'Agra → Delhi → Jaipur',
                'description': 'Taj first route: Taj Mahal → Capital → Pink City'
            }
        ],
        'example': 'Mathura, Fatehpur Sikri, Bharatpur'
    },
    'honeymoon': {
        'label': 'Honeymoon Destination',
        'suggested': 'kashmir',
        'suggested_label': 'Kashmir (Paradise on Earth)',
        'options': [
            {
                'value': 'kashmir',
                'label': 'Kashmir',
                'description': 'Paradise on Earth, Dal Lake, houseboats, snow-capped mountains'
            },
            {
                'value': 'kerala',
                'label': 'Kerala',
                'description': 'God\'s Own Country, backwaters, hill stations, beaches'
            },
            {
                'value': 'goa',
                'label': 'Goa',
                'description': 'Beach paradise, Portuguese heritage, luxury resorts'
            },
            {
                'value': 'udaipur',
                'label': 'Udaipur',
                'description': 'City of Lakes, Lake Palace, romantic royal heritage'
            },
            {
                'value': 'andaman',
                'label': 'Andaman Islands',
                'description': 'Pristine beaches, crystal clear waters, tropical paradise'
            }
        ],
        'example': 'Shimla, Manali, Coorg'
    },
    'adventure': {
        'label': 'Adventure Destination',
        'suggested': 'himachal',
        'suggested_label': 'Himachal Pradesh (Adventure Hub)',
        'options': [
            {
                'value': 'himachal',
                'label': 'Himachal Pradesh',
                'description': 'Trekking, paragliding, river rafting, mountain adventures'
            },
            {
                'value': 'uttarakhand',
                'label': 'Uttarakhand',
                'description': 'Char Dham trek, Valley of Flowers, Kedarnath, adventure + spirituality'
            },
            {
                'value': 'ladakh',
                'label': 'Ladakh',
                'description': 'High altitude desert, bike tours, extreme adventures'
            },
            {
                'value': 'rishikesh',
                'label': 'Rishikesh',
                'description': 'White water rafting, bungee jumping, yoga + adventure'
            }
        ],
        'example': 'Spiti Valley, Zanskar, Auli'
    }
}

# Destination details for itinerary generation
DESTINATION_DETAILS = {
    'varanasi': {
        'name': 'Varanasi',
        'region': 'Uttar Pradesh',
        'type': 'Spiritual',
        'duration': '2-3 days',
        'highlights': ['Ganges Ghats', 'Kashi Vishwanath Temple', 'Sarnath', 'Evening Aarti'],
        'hotels': ['Taj Ganges', 'Radisson Hotel Varanasi', 'Hotel Surya'],
        'artisans': [
            {'name': 'Banarasi Silk Weavers', 'specialty': 'Traditional silk sarees', 'location': 'Peeli Kothi'},
            {'name': 'Brass Craftsmen', 'specialty': 'Religious artifacts and utensils', 'location': 'Thatheri Bazaar'}
        ]
    },
    'rishikesh': {
        'name': 'Rishikesh',
        'region': 'Uttarakhand',
        'type': 'Spiritual & Adventure',
        'duration': '2-3 days',
        'highlights': ['Laxman Jhula', 'Ram Jhula', 'Triveni Ghat', 'Beatles Ashram', 'River Rafting'],
        'hotels': ['Ananda in the Himalayas', 'Ganga Kinare Hotel', 'Hotel Ganga Beach Resort'],
        'artisans': [
            {'name': 'Rudraksha Craftsmen', 'specialty': 'Sacred bead jewelry', 'location': 'Laxman Jhula Market'},
            {'name': 'Ayurvedic Herb Specialists', 'specialty': 'Traditional medicines', 'location': 'Swarg Ashram'}
        ]
    },
    'jaisalmer': {
        'name': 'Jaisalmer',
        'region': 'Rajasthan',
        'type': 'Desert & Heritage',
        'duration': '2-3 days',
        'highlights': ['Jaisalmer Fort', 'Sam Sand Dunes', 'Patwon Ki Haveli', 'Camel Safari'],
        'hotels': ['Suryagarh Jaisalmer', 'Hotel Fort Rajwada', 'Hotel Rang Mahal'],
        'artisans': [
            {'name': 'Stone Carvers', 'specialty': 'Intricate sandstone sculptures', 'location': 'Fort area'},
            {'name': 'Mirror Work Artists', 'specialty': 'Traditional Rajasthani textiles', 'location': 'Sadar Bazaar'}
        ]
    },
    'delhi': {
        'name': 'Delhi',
        'region': 'National Capital Territory',
        'type': 'Heritage & Culture',
        'duration': '2-3 days',
        'highlights': ['Red Fort', 'India Gate', 'Qutub Minar', 'Lotus Temple', 'Chandni Chowk'],
        'hotels': ['The Imperial New Delhi', 'Taj Palace Hotel', 'The Leela Palace New Delhi'],
        'artisans': [
            {'name': 'Chandni Chowk Craftsmen', 'specialty': 'Traditional jewelry and textiles', 'location': 'Old Delhi'},
            {'name': 'Dilli Haat Artists', 'specialty': 'Handicrafts from all over India', 'location': 'INA Market'}
        ]
    },
    'agra': {
        'name': 'Agra',
        'region': 'Uttar Pradesh',
        'type': 'Heritage & Monuments',
        'duration': '1-2 days',
        'highlights': ['Taj Mahal', 'Agra Fort', 'Fatehpur Sikri', 'Mehtab Bagh'],
        'hotels': ['The Oberoi Amarvilas', 'ITC Mughal Agra', 'Taj Hotel & Convention Centre'],
        'artisans': [
            {'name': 'Marble Inlay Artists', 'specialty': 'Pietra Dura work like Taj Mahal', 'location': 'Taj Ganj'},
            {'name': 'Leather Craftsmen', 'specialty': 'Traditional footwear and bags', 'location': 'Sadar Bazaar'}
        ]
    },
    'jaipur': {
        'name': 'Jaipur',
        'region': 'Rajasthan',
        'type': 'Heritage & Royal',
        'duration': '2-3 days',
        'highlights': ['Amber Fort', 'City Palace', 'Hawa Mahal', 'Jantar Mantar'],
        'hotels': ['Rambagh Palace', 'Taj Jai Mahal Palace', 'The Oberoi Rajvilas'],
        'artisans': [
            {'name': 'Blue Pottery Artists', 'specialty': 'Traditional ceramic art', 'location': 'Sanganer'},
            {'name': 'Gem Cutters', 'specialty': 'Precious and semi-precious stones', 'location': 'Johari Bazaar'}
        ]
    }
}

def parse_travel_query(query):
    """Parse travel query and extract components"""
    components = []
    
    # Extract duration
    duration_match = re.search(r'(\d+)\s*days?', query.lower())
    if duration_match:
        days = int(duration_match.group(1))
        components.append({
            'key': 'duration',
            'label': 'Trip Duration',
            'original': duration_match.group(0),
            'understanding': f'{days} days total trip',
            'ambiguous': False,
            'value': days
        })
    
    # Extract specific day allocations
    day_allocations = re.findall(r'(\d+)\s*days?\s*in\s*([^,\d]+?)(?=\s*\d+\s*days?|$|,)', query.lower())
    for days, activity in day_allocations:
        activity = activity.strip()
        
        # Check if activity is ambiguous
        ambiguous_key = None
        for key, data in AMBIGUOUS_TERMS.items():
            if any(keyword in activity for keyword in key.split()):
                ambiguous_key = key
                break
        
        if ambiguous_key:
            components.append({
                'key': f'activity_{activity.replace(" ", "_")}',
                'label': AMBIGUOUS_TERMS[ambiguous_key]['label'],
                'original': f'{days} days in {activity}',
                'ambiguous': True,
                'suggested': AMBIGUOUS_TERMS[ambiguous_key]['suggested'],
                'suggested_label': AMBIGUOUS_TERMS[ambiguous_key]['suggested_label'],
                'options': AMBIGUOUS_TERMS[ambiguous_key]['options'],
                'example': AMBIGUOUS_TERMS[ambiguous_key]['example'],
                'days': int(days)
            })
        else:
            components.append({
                'key': f'activity_{activity.replace(" ", "_")}',
                'label': f'{activity.title()} Experience',
                'original': f'{days} days in {activity}',
                'understanding': f'{days} days allocated for {activity}',
                'ambiguous': False,
                'days': int(days)
            })
    
    # Extract accommodation preferences
    if 'star' in query.lower():
        star_match = re.search(r'(\d+)\s*star', query.lower())
        if star_match:
            stars = int(star_match.group(1))
            components.append({
                'key': 'accommodation',
                'label': 'Hotel Category',
                'original': star_match.group(0),
                'understanding': f'{stars}-star hotels',
                'ambiguous': False,
                'value': stars
            })
    
    # Extract group size
    people_match = re.search(r'(\d+)\s*people', query.lower())
    if people_match:
        people = int(people_match.group(1))
        components.append({
            'key': 'group_size',
            'label': 'Group Size',
            'original': people_match.group(0),
            'understanding': f'{people} travelers',
            'ambiguous': False,
            'value': people
        })
    
    # Extract meal preferences
    if 'dinner' in query.lower():
        components.append({
            'key': 'meals',
            'label': 'Meal Inclusion',
            'original': 'dinner',
            'understanding': 'Dinner included in package',
            'ambiguous': False,
            'value': 'dinner_included'
        })
    
    # Extract transport preferences
    if 'car' in query.lower():
        components.append({
            'key': 'transport',
            'label': 'Transportation',
            'original': 'car',
            'understanding': 'Private car with driver',
            'ambiguous': False,
            'value': 'private_car'
        })
    
    return components

def generate_itinerary(analysis, selections):
    """Generate detailed itinerary based on analysis and user selections"""
    
    # Calculate total days
    total_days = 12  # Default from the example query
    for component in analysis['components']:
        if component['key'] == 'duration':
            total_days = component['value']
            break
    
    # Build destination list based on selections
    destinations = []
    day_counter = 1
    
    for component in analysis['components']:
        if component.get('ambiguous') and component['key'] in selections:
            selected_dest = selections[component['key']]
            if selected_dest in DESTINATION_DETAILS:
                dest_info = DESTINATION_DETAILS[selected_dest].copy()
                dest_info['allocated_days'] = component.get('days', 2)
                dest_info['start_day'] = day_counter
                dest_info['end_day'] = day_counter + dest_info['allocated_days'] - 1
                destinations.append(dest_info)
                day_counter += dest_info['allocated_days']
    
    # Generate day-by-day itinerary
    itinerary_days = []
    current_day = 1
    
    for dest in destinations:
        for day_in_dest in range(dest['allocated_days']):
            day_info = {
                'day': current_day,
                'destination': dest['name'],
                'destination_link': f'#destination-{dest["name"].lower()}',
                'hotel': dest['hotels'][0] if dest['hotels'] else 'Premium Hotel',
                'hotel_link': f'#hotel-{dest["name"].lower()}',
                'activities': f'Explore {", ".join(dest["highlights"][:2])}' if day_in_dest == 0 else f'Continue exploring {dest["name"]} - {", ".join(dest["highlights"][2:4])}',
                'artisan': dest['artisans'][day_in_dest % len(dest['artisans'])] if dest['artisans'] else None
            }
            
            if day_info['artisan']:
                day_info['artisan']['link'] = f'#artisan-{day_info["artisan"]["name"].lower().replace(" ", "-")}'
            
            itinerary_days.append(day_info)
            current_day += 1
    
    # Generate complete itinerary response
    itinerary = {
        'title': f'{total_days}-Day Grand Tour Package of India',
        'description': f'A carefully curated {total_days}-day journey through India\'s most captivating destinations, featuring authentic artisan experiences and cultural immersion.',
        'theme_title': 'Cultural Heritage & Authentic Experiences',
        'introduction': f'Embark on an extraordinary {total_days}-day adventure through India\'s diverse landscapes and rich cultural tapestry. This thoughtfully designed itinerary combines iconic destinations with authentic artisan encounters, ensuring you experience the true essence of Incredible India. From spiritual awakening to royal grandeur, each day offers unique insights into India\'s magnificent heritage.',
        'photos': [
            {'emoji': '🕉️', 'description': 'Spiritual experiences'},
            {'emoji': '🏰', 'description': 'Royal palaces'},
            {'emoji': '🎨', 'description': 'Artisan crafts'},
            {'emoji': '🌅', 'description': 'Scenic beauty'}
        ],
        'days': itinerary_days,
        'inclusions': [
            'Accommodation in selected hotels',
            'Daily breakfast and dinner',
            'Private air-conditioned vehicle with driver',
            'Professional English-speaking guide',
            'All monument entrance fees',
            'Artisan workshop experiences',
            'Cultural performances',
            'Airport transfers'
        ],
        'exclusions': [
            'International flights',
            'Visa fees',
            'Personal expenses',
            'Tips and gratuities',
            'Travel insurance',
            'Lunch (unless specified)',
            'Camera fees at monuments'
        ],
        'pricing': {
            'total': '₹1,25,000 - ₹2,50,000',
            'per_person': '₹31,250 - ₹62,500',
            'flights': '₹25,000 - ₹75,000 additional'
        }
    }
    
    return itinerary

@app.route('/api/search', methods=['POST'])
def analyze_search_query():
    """Analyze complex travel queries and detect ambiguities"""
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query is required'
        })
    
    # Parse the query
    components = parse_travel_query(query)
    
    analysis = {
        'original_query': query,
        'components': components,
        'has_ambiguities': any(comp.get('ambiguous', False) for comp in components),
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route('/api/generate-itinerary', methods=['POST'])
def generate_itinerary_endpoint():
    """Generate detailed itinerary based on analysis and user selections"""
    data = request.get_json()
    analysis = data.get('analysis', {})
    selections = data.get('selections', {})
    
    if not analysis:
        return jsonify({
            'success': False,
            'error': 'Analysis data is required'
        })
    
    # Generate the itinerary
    itinerary = generate_itinerary(analysis, selections)
    
    return jsonify({
        'success': True,
        'itinerary': itinerary
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TravMechanix Intelligent Search API',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

