"""
T2India Complete Itinerary Display System
Name, Description, Pictures, Handicrafts, Day-wise Activities, Hotels, Cost Proposal
"""

import json
from datetime import datetime

class T2IndiaItineraryDisplaySystem:
    def __init__(self):
        # Complete itinerary database with all display elements
        self.itinerary_database = {
            "GT001": {
                "name": "Classic Golden Triangle",
                "short_description": "Experience India's most iconic destinations with the majestic Taj Mahal, royal palaces of Jaipur, and historic monuments of Delhi in this timeless 6-day journey.",
                "prominent_pictures": [
                    {
                        "image": "taj_mahal_sunrise.jpg",
                        "caption": "Taj Mahal at Sunrise - Symbol of Eternal Love",
                        "location": "Agra",
                        "link": "https://t2india.com/attractions/taj-mahal"
                    },
                    {
                        "image": "hawa_mahal_jaipur.jpg", 
                        "caption": "Hawa Mahal - Palace of Winds",
                        "location": "Jaipur",
                        "link": "https://t2india.com/attractions/hawa-mahal"
                    },
                    {
                        "image": "red_fort_delhi.jpg",
                        "caption": "Red Fort - Mughal Grandeur",
                        "location": "Delhi", 
                        "link": "https://t2india.com/attractions/red-fort"
                    },
                    {
                        "image": "amber_fort_jaipur.jpg",
                        "caption": "Amber Fort - Rajasthani Architecture",
                        "location": "Jaipur",
                        "link": "https://t2india.com/attractions/amber-fort"
                    }
                ],
                "available_handicrafts": {
                    "Delhi": [
                        {
                            "name": "Traditional Pottery",
                            "artisan": "Master Ramesh Kumar",
                            "duration": "3 hours",
                            "price": "₹1,200",
                            "link": "https://t2india.com/experiences/delhi-pottery"
                        },
                        {
                            "name": "Block Printing", 
                            "artisan": "Sita Devi",
                            "duration": "4 hours",
                            "price": "₹1,500",
                            "link": "https://t2india.com/experiences/delhi-block-printing"
                        }
                    ],
                    "Jaipur": [
                        {
                            "name": "Blue Pottery",
                            "artisan": "Master Krishan Kant",
                            "duration": "4 hours", 
                            "price": "₹2,000",
                            "link": "https://t2india.com/experiences/jaipur-blue-pottery"
                        },
                        {
                            "name": "Gem Cutting",
                            "artisan": "Rajesh Soni",
                            "duration": "6 hours",
                            "price": "₹5,000", 
                            "link": "https://t2india.com/experiences/jaipur-gem-cutting"
                        }
                    ]
                },
                "day_wise_activities": {
                    "Day 1": {
                        "title": "Delhi Arrival & Historic Exploration",
                        "activities": [
                            {
                                "time": "Morning",
                                "activity": "Arrival at Delhi Airport",
                                "description": "Meet & greet by T2India representative, transfer to hotel",
                                "link": "https://t2india.com/services/airport-transfer"
                            },
                            {
                                "time": "Afternoon", 
                                "activity": "Red Fort Visit",
                                "description": "Explore the magnificent Mughal fortress and UNESCO World Heritage site",
                                "duration": "2 hours",
                                "link": "https://t2india.com/attractions/red-fort"
                            },
                            {
                                "time": "Evening",
                                "activity": "India Gate & Rajpath",
                                "description": "Visit the war memorial and enjoy the ceremonial boulevard",
                                "duration": "1 hour",
                                "link": "https://t2india.com/attractions/india-gate"
                            }
                        ],
                        "overnight": "Delhi"
                    },
                    "Day 2": {
                        "title": "Delhi to Agra - Taj Mahal Sunset",
                        "activities": [
                            {
                                "time": "Morning",
                                "activity": "Drive to Agra",
                                "description": "Comfortable 3-hour drive via Yamuna Expressway",
                                "duration": "3 hours",
                                "link": "https://t2india.com/transport/delhi-agra"
                            },
                            {
                                "time": "Afternoon",
                                "activity": "Hotel Check-in & Lunch",
                                "description": "Rest and refresh at your heritage hotel",
                                "link": "https://t2india.com/hotels/agra"
                            },
                            {
                                "time": "Evening",
                                "activity": "Taj Mahal Sunset Visit",
                                "description": "Witness the marble monument change colors in golden hour",
                                "duration": "2 hours",
                                "link": "https://t2india.com/attractions/taj-mahal"
                            }
                        ],
                        "overnight": "Agra"
                    },
                    "Day 3": {
                        "title": "Agra Fort & Drive to Jaipur",
                        "activities": [
                            {
                                "time": "Morning",
                                "activity": "Agra Fort Exploration",
                                "description": "Discover the red sandstone fortress with Taj views",
                                "duration": "2 hours",
                                "link": "https://t2india.com/attractions/agra-fort"
                            },
                            {
                                "time": "Afternoon",
                                "activity": "Drive to Jaipur",
                                "description": "Scenic 4-hour journey to the Pink City",
                                "duration": "4 hours",
                                "link": "https://t2india.com/transport/agra-jaipur"
                            },
                            {
                                "time": "Evening",
                                "activity": "Jaipur Arrival & Local Markets",
                                "description": "Explore colorful bazaars and local handicrafts",
                                "duration": "2 hours",
                                "link": "https://t2india.com/shopping/jaipur-markets"
                            }
                        ],
                        "overnight": "Jaipur"
                    },
                    "Day 4": {
                        "title": "Jaipur Royal Heritage",
                        "activities": [
                            {
                                "time": "Morning",
                                "activity": "Amber Fort & Elephant Ride",
                                "description": "Majestic hilltop fort with optional elephant experience",
                                "duration": "3 hours",
                                "link": "https://t2india.com/attractions/amber-fort"
                            },
                            {
                                "time": "Afternoon",
                                "activity": "City Palace Complex",
                                "description": "Royal residence with museums and courtyards",
                                "duration": "2 hours",
                                "link": "https://t2india.com/attractions/city-palace-jaipur"
                            },
                            {
                                "time": "Evening",
                                "activity": "Hawa Mahal & Handicraft Workshop",
                                "description": "Palace of Winds and traditional blue pottery experience",
                                "duration": "2 hours",
                                "link": "https://t2india.com/experiences/jaipur-blue-pottery"
                            }
                        ],
                        "overnight": "Jaipur"
                    },
                    "Day 5": {
                        "title": "Jaipur to Delhi",
                        "activities": [
                            {
                                "time": "Morning",
                                "activity": "Jantar Mantar Observatory",
                                "description": "UNESCO World Heritage astronomical instruments",
                                "duration": "1 hour",
                                "link": "https://t2india.com/attractions/jantar-mantar"
                            },
                            {
                                "time": "Afternoon",
                                "activity": "Drive to Delhi",
                                "description": "Return journey to the capital city",
                                "duration": "5 hours",
                                "link": "https://t2india.com/transport/jaipur-delhi"
                            },
                            {
                                "time": "Evening",
                                "activity": "Delhi Hotel Check-in",
                                "description": "Rest and prepare for departure",
                                "link": "https://t2india.com/hotels/delhi"
                            }
                        ],
                        "overnight": "Delhi"
                    },
                    "Day 6": {
                        "title": "Delhi Departure",
                        "activities": [
                            {
                                "time": "Morning",
                                "activity": "Humayun's Tomb (Optional)",
                                "description": "Mughal architecture precursor to Taj Mahal",
                                "duration": "1 hour",
                                "link": "https://t2india.com/attractions/humayuns-tomb"
                            },
                            {
                                "time": "Afternoon",
                                "activity": "Airport Transfer",
                                "description": "Comfortable transfer for international departure",
                                "link": "https://t2india.com/services/airport-transfer"
                            }
                        ],
                        "overnight": "Departure"
                    }
                },
                "hotel_choices": {
                    "Delhi": [
                        {
                            "name": "The Imperial New Delhi",
                            "category": "4-star Heritage",
                            "comment": "Colonial elegance in heart of Delhi (or similar)",
                            "amenities": ["Pool", "Spa", "Multiple Restaurants"],
                            "link": "https://t2india.com/hotels/imperial-delhi"
                        },
                        {
                            "name": "Taj Palace New Delhi", 
                            "category": "4-star Luxury",
                            "comment": "Modern luxury with traditional hospitality (or similar)",
                            "amenities": ["Business Center", "Fitness", "Fine Dining"],
                            "link": "https://t2india.com/hotels/taj-palace-delhi"
                        }
                    ],
                    "Agra": [
                        {
                            "name": "Taj Hotel & Convention Centre",
                            "category": "4-star Heritage",
                            "comment": "Taj view rooms available (or similar)",
                            "amenities": ["Taj Views", "Pool", "Multi-cuisine Restaurant"],
                            "link": "https://t2india.com/hotels/taj-agra"
                        },
                        {
                            "name": "Courtyard by Marriott Agra",
                            "category": "4-star Modern",
                            "comment": "Contemporary comfort near monuments (or similar)",
                            "amenities": ["Modern Rooms", "Fitness Center", "Business Facilities"],
                            "link": "https://t2india.com/hotels/courtyard-agra"
                        }
                    ],
                    "Jaipur": [
                        {
                            "name": "Hilton Jaipur",
                            "category": "4-star International",
                            "comment": "International standards with local charm (or similar)",
                            "amenities": ["Pool", "Spa", "Multiple Dining Options"],
                            "link": "https://t2india.com/hotels/hilton-jaipur"
                        },
                        {
                            "name": "Hotel Clarks Amer",
                            "category": "4-star Heritage",
                            "comment": "Rajasthani architecture and hospitality (or similar)",
                            "amenities": ["Traditional Decor", "Garden", "Cultural Programs"],
                            "link": "https://t2india.com/hotels/clarks-amer-jaipur"
                        }
                    ]
                },
                "unique_id": "T2I-GT-001",
                "duration": 6,
                "destinations": ["Delhi", "Agra", "Jaipur"],
                "rating": 4.8,
                "bookings": 156,
                "price_range": "₹15,000-45,000"
            }
        }
    
    def generate_description_with_api(self, itinerary_name, destinations):
        """Generate description using fallback logic if not available"""
        # Fallback description generation (can be replaced with Manus language API)
        destination_highlights = {
            "Delhi": "historic monuments and vibrant culture",
            "Agra": "the iconic Taj Mahal and Mughal architecture", 
            "Jaipur": "royal palaces and colorful markets",
            "Goa": "pristine beaches and Portuguese heritage",
            "Kolkata": "cultural richness and colonial charm",
            "Hampi": "ancient ruins and UNESCO World Heritage sites"
        }
        
        highlights = []
        for dest in destinations:
            if dest in destination_highlights:
                highlights.append(destination_highlights[dest])
        
        if highlights:
            highlight_text = ", ".join(highlights[:2])  # Take first 2
            return f"Experience the magnificent destinations of {', '.join(destinations)} featuring {highlight_text}. This carefully crafted itinerary offers the perfect blend of culture, heritage, and authentic Indian hospitality."
        else:
            return f"Explore the magnificent destinations of {', '.join(destinations)} in this carefully crafted itinerary. Experience the perfect blend of culture, heritage, and authentic Indian hospitality."
    
    def format_itinerary_display(self, itinerary_id):
        """Format complete itinerary display"""
        
        if itinerary_id not in self.itinerary_database:
            return "Itinerary not found"
        
        itinerary = self.itinerary_database[itinerary_id]
        
        # Generate description if not available
        description = itinerary.get("short_description")
        if not description:
            description = self.generate_description_with_api(
                itinerary["name"], 
                itinerary["destinations"]
            )
        
        output = f"""
=== T2INDIA ITINERARY PRESENTATION ===

{itinerary['name'].upper()}
Unique ID: {itinerary['unique_id']} | Duration: {itinerary['duration']} Days
Rating: {itinerary['rating']}★ | Successful Bookings: {itinerary['bookings']}

DESCRIPTION:
{description}

=== PROMINENT PICTURES ===
"""
        
        for i, picture in enumerate(itinerary['prominent_pictures'], 1):
            output += f"""
{i}. {picture['caption']}
   Location: {picture['location']}
   Link: {picture['link']}
"""
        
        output += "\n=== AVAILABLE HANDICRAFTS ===\n"
        
        for city, handicrafts in itinerary['available_handicrafts'].items():
            output += f"\nIn {city}:\n"
            for craft in handicrafts:
                output += f"""  • {craft['name']} with {craft['artisan']}
    Duration: {craft['duration']} | Price: {craft['price']}
    Experience Link: {craft['link']}
"""
        
        output += "\n=== DAY-WISE ACTIVITIES ===\n"
        
        for day, details in itinerary['day_wise_activities'].items():
            output += f"\n{day.upper()}: {details['title']}\n"
            output += "-" * 50 + "\n"
            
            for activity in details['activities']:
                output += f"""
{activity['time'].upper()}:
• {activity['activity']}
  {activity['description']}
"""
                if 'duration' in activity:
                    output += f"  Duration: {activity['duration']}\n"
                output += f"  Link: {activity['link']}\n"
            
            output += f"Overnight: {details['overnight']}\n"
        
        output += "\n=== 4-STAR HOTEL CHOICES ===\n"
        
        for city, hotels in itinerary['hotel_choices'].items():
            output += f"\n{city.upper()}:\n"
            for hotel in hotels:
                output += f"""
• {hotel['name']} ({hotel['category']})
  {hotel['comment']}
  Amenities: {', '.join(hotel['amenities'])}
  Booking Link: {hotel['link']}
"""
        
        output += f"""

=== COST PROPOSAL PROCESS ===

Once you confirm this itinerary, T2India will provide:

1. DETAILED COST BREAKDOWN
   • Accommodation costs (4-star hotels or similar)
   • Private transportation (vehicle appropriate for group size)
   • All entrance fees and permits
   • Professional guide services
   • Handicraft workshop costs

2. PRICING CATEGORIES
   • Budget Option: Standard 4-star accommodations
   • Premium Option: Luxury 4-star properties

3. CUSTOMIZATION OPTIONS
   • Hotel upgrades available
   • Additional handicraft experiences
   • Extended stays in any city
   • Special dietary requirements

4. CONFIRMATION PROCESS
   • Review and approve final itinerary
   • Receive detailed cost proposal
   • Secure booking with advance payment
   • Receive dedicated T2India app access

ESTIMATED PRICE RANGE: {itinerary['price_range']} per person
(Final pricing depends on group size, travel dates, and hotel selections)

=== NEXT STEPS ===

To proceed with cost proposal:
1. Confirm this itinerary suits your requirements
2. Provide travel dates and group size
3. Select preferred hotel category
4. Choose desired handicraft experiences
5. Receive detailed pricing within 24 hours

Contact: reservations@t2india.com | +91-XXXX-XXXX
Website: https://t2india.com/itineraries/{itinerary['unique_id'].lower()}

All elements in this itinerary are hyperlinked to t2india.com for detailed information and direct booking capabilities.
"""
        
        return output
    
    def create_itinerary_summary_list(self):
        """Create summary list of all available itineraries"""
        
        output = """
=== T2INDIA ITINERARY LIBRARY ===

Available Proven Itineraries:
"""
        
        for itinerary_id, itinerary in self.itinerary_database.items():
            output += f"""
{itinerary['name']} ({itinerary['unique_id']})
• Duration: {itinerary['duration']} days
• Destinations: {' → '.join(itinerary['destinations'])}
• Rating: {itinerary['rating']}★ ({itinerary['bookings']} bookings)
• Price Range: {itinerary['price_range']}
• View Details: https://t2india.com/itineraries/{itinerary['unique_id'].lower()}

"""
        
        return output

def test_itinerary_display_system():
    """Test the complete itinerary display system"""
    
    system = T2IndiaItineraryDisplaySystem()
    
    print("=" * 80)
    print("T2INDIA ITINERARY DISPLAY SYSTEM - TESTING")
    print("=" * 80)
    
    # Test complete itinerary display
    print("\n=== COMPLETE ITINERARY DISPLAY TEST ===")
    display_output = system.format_itinerary_display("GT001")
    print(display_output)
    
    # Test itinerary library summary
    print("\n=== ITINERARY LIBRARY SUMMARY ===")
    library_summary = system.create_itinerary_summary_list()
    print(library_summary)
    
    print("=" * 80)
    print("ITINERARY DISPLAY SYSTEM TESTING COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_itinerary_display_system()

