"""
T2India Final Intelligent Routing & Itinerary System
Consolidates all components: routing, library integration, handicrafts, connectivity
"""

from intelligent_itinerary_builder import ItinerarySuggestionEngine
from itinerary_library_integration import T2IndiaItineraryLibrary
import json
import re

class T2IndiaFinalSystem:
    def __init__(self):
        self.routing_engine = ItinerarySuggestionEngine()
        self.itinerary_library = T2IndiaItineraryLibrary()
        
        # Handicraft database (from previous implementation)
        self.handicrafts_db = {
            "Delhi": [
                {
                    "name": "Traditional Pottery",
                    "artisan": "Master Ramesh Kumar",
                    "workshop_duration": "3 hours",
                    "price": "₹1,200",
                    "difficulty": "Beginner",
                    "description": "Learn traditional pottery techniques"
                },
                {
                    "name": "Block Printing",
                    "artisan": "Sita Devi",
                    "workshop_duration": "4 hours", 
                    "price": "₹1,500",
                    "difficulty": "Intermediate",
                    "description": "Traditional textile block printing"
                }
            ],
            "Jaipur": [
                {
                    "name": "Blue Pottery",
                    "artisan": "Master Krishan Kant",
                    "workshop_duration": "4 hours",
                    "price": "₹2,000",
                    "difficulty": "Intermediate",
                    "description": "Famous Jaipur blue pottery making"
                },
                {
                    "name": "Gem Cutting",
                    "artisan": "Rajesh Soni",
                    "workshop_duration": "6 hours",
                    "price": "₹5,000",
                    "difficulty": "Advanced",
                    "description": "Traditional gem cutting and polishing"
                }
            ],
            "Goa": [
                {
                    "name": "Azulejo Tile Painting",
                    "artisan": "Maria Fernandes",
                    "workshop_duration": "3 hours",
                    "price": "₹1,800",
                    "difficulty": "Beginner",
                    "description": "Portuguese-style tile painting"
                }
            ],
            "Kolkata": [
                {
                    "name": "Kantha Embroidery",
                    "artisan": "Malati Ghosh",
                    "workshop_duration": "5 hours",
                    "price": "₹2,500",
                    "difficulty": "Intermediate",
                    "description": "Traditional Bengali embroidery"
                }
            ]
        }

    def process_user_query(self, user_input):
        """
        Main function to process user query and return comprehensive suggestions
        """
        print(f"Processing: {user_input}")
        
        # Step 1: Parse user input
        destinations = self.routing_engine.extract_destinations(user_input)
        duration = self.extract_duration(user_input)
        
        # Step 2: Check existing itinerary library first
        library_result = self.itinerary_library.generate_hybrid_itinerary(
            user_input, destinations, duration
        )
        
        # Step 3: Generate routing suggestions
        routing_result = self.routing_engine.suggest_itinerary(user_input)
        
        # Step 4: Combine results
        final_result = {
            "user_query": user_input,
            "parsed_destinations": destinations,
            "parsed_duration": duration,
            "library_check": library_result,
            "routing_suggestions": routing_result,
            "handicraft_options": self.get_handicraft_options(destinations),
            "final_recommendation": self.generate_final_recommendation(
                library_result, routing_result, destinations, duration
            )
        }
        
        return final_result

    def extract_duration(self, user_input):
        """Extract duration from user input"""
        duration_match = re.search(r'(\d+)\s*days?', user_input.lower())
        return int(duration_match.group(1)) if duration_match else None

    def get_handicraft_options(self, destinations):
        """Get available handicraft options for destinations"""
        options = {}
        for destination in destinations:
            if destination in self.handicrafts_db:
                options[destination] = self.handicrafts_db[destination]
        return options

    def generate_final_recommendation(self, library_result, routing_result, destinations, duration):
        """Generate final recommendation combining all inputs"""
        
        recommendation = {
            "approach": "hybrid",
            "primary_suggestion": None,
            "alternatives": [],
            "extensions": [],
            "handicrafts": "optional",
            "next_steps": []
        }
        
        # Determine primary approach
        if library_result["recommendation"] == "modify_existing":
            recommendation["primary_suggestion"] = {
                "type": "existing_itinerary",
                "base": library_result["base_itinerary"],
                "modifications": library_result["existing_match"]["modifications_needed"],
                "confidence": "high",
                "reason": f"Perfect match with proven itinerary ({library_result['existing_match']['itinerary']['bookings']} bookings)"
            }
        elif library_result["recommendation"] == "create_new_with_reference":
            recommendation["primary_suggestion"] = {
                "type": "new_with_reference", 
                "reference": library_result["reference_itinerary"],
                "new_route": routing_result["suggested_route"],
                "confidence": "medium",
                "reason": "Combining proven elements with new routing"
            }
        else:
            recommendation["primary_suggestion"] = {
                "type": "completely_new",
                "route": routing_result["suggested_route"],
                "duration_options": routing_result["duration_options"],
                "confidence": "medium",
                "reason": "Custom itinerary for unique requirements"
            }
        
        # Add extensions
        if "regional_extensions" in routing_result:
            for city, extensions in routing_result["regional_extensions"].items():
                for theme, details in extensions.items():
                    recommendation["extensions"].append({
                        "from_city": city,
                        "theme": details["theme"],
                        "destinations": details["destinations"],
                        "additional_days": details["additional_days"],
                        "priority": details.get("priority", 3)
                    })
        
        # Sort extensions by priority
        recommendation["extensions"].sort(key=lambda x: x.get("priority", 3))
        
        # Add next steps
        recommendation["next_steps"] = [
            "Review suggested route and duration",
            "Select preferred extension theme (optional)",
            "Choose handicraft experiences (optional)",
            "Confirm dates and finalize itinerary"
        ]
        
        return recommendation

    def format_output_for_client(self, result):
        """Format the result for client presentation"""
        
        output = f"""
=== T2INDIA INTELLIGENT ITINERARY SUGGESTION ===

Query: {result['user_query']}
Destinations: {', '.join(result['parsed_destinations'])}
Duration: {result['parsed_duration']} days

=== PRIMARY RECOMMENDATION ===
Approach: {result['final_recommendation']['primary_suggestion']['type'].replace('_', ' ').title()}
Confidence: {result['final_recommendation']['primary_suggestion']['confidence'].title()}
Reason: {result['final_recommendation']['primary_suggestion']['reason']}

"""
        
        # Add route information
        if result['final_recommendation']['primary_suggestion']['type'] == 'existing_itinerary':
            base = result['final_recommendation']['primary_suggestion']['base']
            output += f"""
Base Itinerary: {base['name']}
Route: {' → '.join(base['route'])}
Rating: {base['rating']}★ ({base['bookings']} bookings)
Price Range: {base['price_range']}

Modifications Needed:
"""
            for mod in result['final_recommendation']['primary_suggestion']['modifications']:
                output += f"• {mod}\n"
        else:
            route = result['routing_suggestions']['suggested_route']
            output += f"\nSuggested Route: {' → '.join(route)}\n"
        
        # Add extensions
        if result['final_recommendation']['extensions']:
            output += "\n=== EXTENSION OPTIONS ===\n"
            for ext in result['final_recommendation']['extensions'][:3]:  # Top 3
                output += f"""
From {ext['from_city']}: {ext['theme']}
Destinations: {', '.join(ext['destinations'])}
Additional Days: {ext['additional_days']}
Priority: {ext['priority']}
"""
        
        # Add handicrafts
        if result['handicraft_options']:
            output += "\n=== HANDICRAFT EXPERIENCES AVAILABLE ===\n"
            for city, crafts in result['handicraft_options'].items():
                output += f"\nIn {city}:\n"
                for craft in crafts:
                    output += f"• {craft['name']} with {craft['artisan']} ({craft['price']})\n"
        
        output += f"""
=== NEXT STEPS ===
"""
        for step in result['final_recommendation']['next_steps']:
            output += f"1. {step}\n"
        
        return output

# Test the complete system
if __name__ == "__main__":
    system = T2IndiaFinalSystem()
    
    # Test cases
    test_queries = [
        "Golden Triangle for 6 days",
        "Goa Delhi Kolkata for 12 days", 
        "Rajasthan royal tour 8 days",
        "Kerala backwaters 5 days",
        "Mumbai Pune Nashik 7 days"
    ]
    
    for query in test_queries:
        print("=" * 80)
        result = system.process_user_query(query)
        formatted_output = system.format_output_for_client(result)
        print(formatted_output)
        print("=" * 80)
        print()

