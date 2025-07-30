"""
T2India Itinerary Library Integration System
Suggests existing itineraries before generating new ones
"""

import json
from datetime import datetime, timedelta
import re

class T2IndiaItineraryLibrary:
    def __init__(self):
        # Sample existing T2India itineraries database
        self.existing_itineraries = {
            "golden_triangle_6d": {
                "id": "GT001",
                "name": "Classic Golden Triangle",
                "destinations": ["Delhi", "Agra", "Jaipur"],
                "duration": 6,
                "route": ["Delhi", "Agra", "Jaipur", "Delhi"],
                "bookings": 156,
                "rating": 4.8,
                "price_range": "₹15,000",
                "highlights": ["Taj Mahal", "Red Fort", "Hawa Mahal", "Amber Fort"],
                "day_wise": {
                    "Day 1": "Delhi arrival, Red Fort, India Gate",
                    "Day 2": "Delhi to Agra, Taj Mahal visit",
                    "Day 3": "Agra Fort, drive to Jaipur",
                    "Day 4": "Amber Fort, City Palace, Hawa Mahal",
                    "Day 5": "Jaipur local sightseeing",
                    "Day 6": "Return to Delhi, departure"
                },
                "tags": ["heritage", "culture", "monuments", "unesco"]
            },
            "kerala_backwaters_5d": {
                "id": "KB001", 
                "name": "Kerala Backwater Bliss",
                "destinations": ["Kochi", "Alleppey", "Kumarakom"],
                "duration": 5,
                "route": ["Kochi", "Alleppey", "Kumarakom", "Kochi"],
                "bookings": 89,
                "rating": 4.9,
                "price_range": "₹18,000",
                "highlights": ["Houseboat", "Backwaters", "Spice Gardens", "Ayurveda"],
                "day_wise": {
                    "Day 1": "Kochi arrival, Fort Kochi exploration",
                    "Day 2": "Kochi to Alleppey, houseboat check-in",
                    "Day 3": "Backwater cruise, Kumarakom",
                    "Day 4": "Bird sanctuary, Ayurveda spa",
                    "Day 5": "Return to Kochi, departure"
                },
                "tags": ["nature", "backwaters", "ayurveda", "relaxation"]
            },
            "rajasthan_royal_8d": {
                "id": "RR001",
                "name": "Rajasthan Royal Heritage", 
                "destinations": ["Jodhpur", "Udaipur", "Jaisalmer"],
                "duration": 8,
                "route": ["Jodhpur", "Udaipur", "Jaisalmer", "Jodhpur"],
                "bookings": 134,
                "rating": 4.7,
                "price_range": "₹22,000",
                "highlights": ["Mehrangarh Fort", "Lake Palace", "Desert Safari", "Camel Ride"],
                "day_wise": {
                    "Day 1": "Jodhpur arrival, Mehrangarh Fort",
                    "Day 2": "Jodhpur to Udaipur, City Palace",
                    "Day 3": "Lake Pichola, Jagdish Temple",
                    "Day 4": "Udaipur to Jaisalmer",
                    "Day 5": "Jaisalmer Fort, Patwon Ki Haveli",
                    "Day 6": "Desert safari, camel ride",
                    "Day 7": "Sam Sand Dunes, cultural evening",
                    "Day 8": "Return to Jodhpur, departure"
                },
                "tags": ["royal", "desert", "forts", "heritage"]
            },
            "kashmir_paradise_7d": {
                "id": "KP001",
                "name": "Kashmir Paradise",
                "destinations": ["Srinagar", "Gulmarg", "Pahalgam"],
                "duration": 7,
                "route": ["Srinagar", "Gulmarg", "Pahalgam", "Srinagar"],
                "bookings": 67,
                "rating": 4.9,
                "price_range": "₹25,000",
                "highlights": ["Dal Lake", "Shikara Ride", "Gondola", "Valley Views"],
                "day_wise": {
                    "Day 1": "Srinagar arrival, Dal Lake shikara",
                    "Day 2": "Mughal Gardens, local markets",
                    "Day 3": "Srinagar to Gulmarg, Gondola ride",
                    "Day 4": "Gulmarg to Pahalgam",
                    "Day 5": "Betaab Valley, Aru Valley",
                    "Day 6": "Pahalgam to Srinagar",
                    "Day 7": "Departure from Srinagar"
                },
                "tags": ["mountains", "lakes", "nature", "adventure"]
            },
            "goa_hampi_heritage_6d": {
                "id": "GH001",
                "name": "Goa Hampi Heritage Circuit",
                "destinations": ["Goa", "Hampi"],
                "duration": 6,
                "route": ["Goa", "Hampi", "Goa"],
                "bookings": 45,
                "rating": 4.6,
                "price_range": "₹16,000",
                "highlights": ["Beaches", "UNESCO Heritage", "Vijayanagara Ruins", "Portuguese Architecture"],
                "day_wise": {
                    "Day 1": "Goa arrival, beach relaxation",
                    "Day 2": "Old Goa churches, spice plantation",
                    "Day 3": "Goa to Hampi (5 hours drive)",
                    "Day 4": "Hampi ruins, Virupaksha Temple",
                    "Day 5": "Vittala Temple, Stone Chariot",
                    "Day 6": "Return to Goa, departure"
                },
                "tags": ["heritage", "unesco", "beaches", "history"]
            },
            "kolkata_darjeeling_hills_8d": {
                "id": "KD001",
                "name": "Kolkata Darjeeling Hills",
                "destinations": ["Kolkata", "Darjeeling"],
                "duration": 8,
                "route": ["Kolkata", "Darjeeling", "Kolkata"],
                "bookings": 78,
                "rating": 4.5,
                "price_range": "₹19,000",
                "highlights": ["Victoria Memorial", "Tea Gardens", "Toy Train", "Tiger Hill"],
                "day_wise": {
                    "Day 1": "Kolkata arrival, Victoria Memorial",
                    "Day 2": "Howrah Bridge, Dakshineswar Temple",
                    "Day 3": "Kolkata to Darjeeling (train/road)",
                    "Day 4": "Tiger Hill sunrise, tea garden visit",
                    "Day 5": "Toy train ride, local markets",
                    "Day 6": "Darjeeling monastery visits",
                    "Day 7": "Return journey to Kolkata",
                    "Day 8": "Kolkata departure"
                },
                "tags": ["hills", "tea", "heritage", "train"]
            }
        }
        
        # Destination aliases for flexible matching
        self.destination_aliases = {
            "delhi": ["delhi", "new delhi"],
            "agra": ["agra"],
            "jaipur": ["jaipur", "pink city"],
            "goa": ["goa", "panaji"],
            "kolkata": ["kolkata", "calcutta"],
            "darjeeling": ["darjeeling"],
            "hampi": ["hampi"],
            "kochi": ["kochi", "cochin"],
            "alleppey": ["alleppey", "alappuzha"],
            "jodhpur": ["jodhpur", "blue city"],
            "udaipur": ["udaipur", "city of lakes"],
            "jaisalmer": ["jaisalmer", "golden city"],
            "srinagar": ["srinagar"],
            "gulmarg": ["gulmarg"],
            "pahalgam": ["pahalgam"]
        }

    def normalize_destination(self, destination):
        """Normalize destination names for matching"""
        dest_lower = destination.lower().strip()
        for standard, aliases in self.destination_aliases.items():
            if dest_lower in aliases:
                return standard.title()
        return destination.title()

    def find_matching_itineraries(self, user_destinations, duration=None):
        """Find existing itineraries that match user requirements"""
        normalized_destinations = [self.normalize_destination(d) for d in user_destinations]
        matches = []
        
        for itinerary_id, itinerary in self.existing_itineraries.items():
            # Check destination overlap
            itinerary_destinations = [self.normalize_destination(d) for d in itinerary["destinations"]]
            
            # Calculate match percentage
            common_destinations = set(normalized_destinations) & set(itinerary_destinations)
            match_percentage = len(common_destinations) / len(set(normalized_destinations) | set(itinerary_destinations))
            
            # Consider duration match if specified
            duration_match = 1.0
            if duration:
                duration_diff = abs(itinerary["duration"] - duration)
                duration_match = max(0, 1 - (duration_diff / 10))  # Penalty for duration difference
            
            # Overall match score
            overall_score = (match_percentage * 0.7) + (duration_match * 0.3)
            
            if overall_score > 0.3:  # Minimum threshold
                matches.append({
                    "itinerary": itinerary,
                    "match_score": overall_score,
                    "common_destinations": list(common_destinations),
                    "missing_destinations": list(set(normalized_destinations) - set(itinerary_destinations)),
                    "extra_destinations": list(set(itinerary_destinations) - set(normalized_destinations))
                })
        
        # Sort by match score
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches

    def suggest_itinerary_modifications(self, base_itinerary, user_destinations, user_duration):
        """Suggest how to modify existing itinerary to match user needs"""
        modifications = []
        
        # Duration adjustments
        duration_diff = user_duration - base_itinerary["duration"]
        if duration_diff > 0:
            modifications.append(f"Extend by {duration_diff} days for more exploration")
        elif duration_diff < 0:
            modifications.append(f"Compress by {abs(duration_diff)} days for shorter trip")
        
        # Destination adjustments
        base_destinations = set([self.normalize_destination(d) for d in base_itinerary["destinations"]])
        user_destinations_set = set([self.normalize_destination(d) for d in user_destinations])
        
        missing = user_destinations_set - base_destinations
        extra = base_destinations - user_destinations_set
        
        if missing:
            modifications.append(f"Add destinations: {', '.join(missing)}")
        if extra:
            modifications.append(f"Optional to remove: {', '.join(extra)}")
        
        return modifications

    def generate_hybrid_itinerary(self, user_input, user_destinations, user_duration):
        """Generate itinerary using existing library + new generation"""
        
        # First, try to find matching existing itineraries
        matches = self.find_matching_itineraries(user_destinations, user_duration)
        
        result = {
            "approach": "hybrid",
            "user_input": user_input,
            "requested_destinations": user_destinations,
            "requested_duration": user_duration
        }
        
        if matches:
            best_match = matches[0]
            result["existing_match"] = {
                "found": True,
                "itinerary": best_match["itinerary"],
                "match_score": best_match["match_score"],
                "modifications_needed": self.suggest_itinerary_modifications(
                    best_match["itinerary"], user_destinations, user_duration
                ),
                "common_destinations": best_match["common_destinations"],
                "missing_destinations": best_match["missing_destinations"]
            }
            
            # If match score is high, suggest using existing with modifications
            if best_match["match_score"] > 0.7:
                result["recommendation"] = "modify_existing"
                result["base_itinerary"] = best_match["itinerary"]
            else:
                result["recommendation"] = "create_new_with_reference"
                result["reference_itinerary"] = best_match["itinerary"]
        else:
            result["existing_match"] = {"found": False}
            result["recommendation"] = "create_completely_new"
        
        # Add alternative suggestions
        if len(matches) > 1:
            result["alternatives"] = [
                {
                    "itinerary": match["itinerary"],
                    "match_score": match["match_score"],
                    "why_suggested": f"Covers {len(match['common_destinations'])} of your destinations"
                }
                for match in matches[1:3]  # Top 2 alternatives
            ]
        
        return result

# Example usage and testing
if __name__ == "__main__":
    library = T2IndiaItineraryLibrary()
    
    # Test case 1: Exact match
    print("=== TEST 1: Golden Triangle Query ===")
    result1 = library.generate_hybrid_itinerary(
        "Golden Triangle for 6 days",
        ["Delhi", "Agra", "Jaipur"],
        6
    )
    print(f"Recommendation: {result1['recommendation']}")
    if result1['existing_match']['found']:
        print(f"Match Score: {result1['existing_match']['match_score']:.2f}")
        print(f"Base Itinerary: {result1['existing_match']['itinerary']['name']}")
    print()
    
    # Test case 2: Partial match with extension
    print("=== TEST 2: Goa Delhi Kolkata for 12 days ===")
    result2 = library.generate_hybrid_itinerary(
        "Goa Delhi Kolkata for 12 days",
        ["Goa", "Delhi", "Kolkata"],
        12
    )
    print(f"Recommendation: {result2['recommendation']}")
    if result2['existing_match']['found']:
        print(f"Match Score: {result2['existing_match']['match_score']:.2f}")
        print(f"Best Match: {result2['existing_match']['itinerary']['name']}")
        print(f"Modifications: {result2['existing_match']['modifications_needed']}")
    print()
    
    # Test case 3: No direct match
    print("=== TEST 3: Mumbai Pune Nashik for 5 days ===")
    result3 = library.generate_hybrid_itinerary(
        "Mumbai Pune Nashik for 5 days",
        ["Mumbai", "Pune", "Nashik"],
        5
    )
    print(f"Recommendation: {result3['recommendation']}")
    if result3['existing_match']['found']:
        print(f"Best Alternative: {result3['existing_match']['itinerary']['name']}")
    else:
        print("No existing matches found - will create new itinerary")

