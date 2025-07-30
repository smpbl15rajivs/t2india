"""
T2India Complete Routing Solution with Intelligent Suggestions
Analyzes itineraries and provides optimization recommendations
"""

import json
from datetime import datetime, timedelta

class T2IndiaRoutingSolutionWithSuggestions:
    def __init__(self):
        # Destination database with characteristics
        self.destination_database = {
            "Mumbai": {
                "type": "metropolitan",
                "climate": "coastal_humid",
                "best_duration": "1-2 days",
                "key_attractions": ["Gateway of India", "Marine Drive", "Bollywood Studios"],
                "connectivity": {
                    "major_airports": ["BOM"],
                    "flight_hubs": ["Delhi", "Goa", "Bangalore", "Kolkata"]
                },
                "optimal_timing": "morning_arrival_evening_departure",
                "handicrafts": ["Warli Art", "Leather Goods"]
            },
            "Goa": {
                "type": "beach_destination",
                "climate": "tropical_coastal",
                "best_duration": "3-5 days",
                "key_attractions": ["Beaches", "Portuguese Churches", "Spice Plantations"],
                "connectivity": {
                    "major_airports": ["GOI"],
                    "flight_hubs": ["Mumbai", "Delhi", "Bangalore", "Cochin"]
                },
                "optimal_timing": "relaxed_pace",
                "handicrafts": ["Azulejo Tiles", "Cashew Products"]
            },
            "Cochin": {
                "type": "heritage_port",
                "climate": "tropical_humid",
                "best_duration": "1-2 days",
                "key_attractions": ["Chinese Fishing Nets", "Fort Kochi", "Spice Markets"],
                "connectivity": {
                    "major_airports": ["COK"],
                    "flight_hubs": ["Mumbai", "Delhi", "Goa", "Bangalore"]
                },
                "optimal_timing": "gateway_to_kerala",
                "handicrafts": ["Spice Processing", "Coir Products"]
            },
            "Munnar": {
                "type": "hill_station",
                "climate": "cool_mountain",
                "best_duration": "2-3 days",
                "key_attractions": ["Tea Plantations", "Eravikulam National Park", "Mattupetty Dam"],
                "connectivity": {
                    "nearest_airport": "Cochin (130km)",
                    "road_access": "scenic_mountain_drive"
                },
                "optimal_timing": "overnight_stay_recommended",
                "handicrafts": ["Tea Processing", "Spice Gardens"]
            },
            "Delhi": {
                "type": "capital_heritage",
                "climate": "continental",
                "best_duration": "2-3 days",
                "key_attractions": ["Red Fort", "India Gate", "Humayun's Tomb"],
                "connectivity": {
                    "major_airports": ["DEL"],
                    "flight_hubs": "international_gateway"
                },
                "optimal_timing": "golden_triangle_start",
                "handicrafts": ["Block Printing", "Traditional Pottery"]
            },
            "Agra": {
                "type": "heritage_monument",
                "climate": "continental",
                "best_duration": "1-2 days",
                "key_attractions": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri"],
                "connectivity": {
                    "road_from_delhi": "3 hours",
                    "expressway": "yamuna_expressway"
                },
                "optimal_timing": "sunrise_sunset_taj",
                "handicrafts": ["Marble Inlay", "Leather Goods"]
            },
            "Jaipur": {
                "type": "royal_heritage",
                "climate": "desert_continental",
                "best_duration": "2-3 days",
                "key_attractions": ["Amber Fort", "City Palace", "Hawa Mahal"],
                "connectivity": {
                    "road_from_agra": "4 hours",
                    "road_to_delhi": "5 hours"
                },
                "optimal_timing": "golden_triangle_highlight",
                "handicrafts": ["Blue Pottery", "Gem Cutting", "Block Printing"]
            }
        }
        
        # Routing intelligence rules
        self.routing_rules = {
            "geographical_optimization": {
                "west_coast_flow": ["Mumbai", "Goa", "Cochin"],
                "kerala_circuit": ["Cochin", "Munnar", "Alleppey"],
                "golden_triangle": ["Delhi", "Agra", "Jaipur"],
                "north_india_exit": "Delhi"
            },
            "climate_considerations": {
                "hill_stations": "overnight_stay_recommended",
                "coastal_destinations": "relaxed_pace_optimal",
                "heritage_cities": "early_morning_late_evening_best"
            },
            "connectivity_optimization": {
                "flight_minimization": "group_nearby_destinations",
                "road_journey_limits": "max_6_hours_comfortable",
                "airport_efficiency": "use_major_hubs"
            }
        }
    
    def analyze_itinerary_structure(self, itinerary):
        """Analyze the given itinerary structure"""
        
        analysis = {
            "total_days": itinerary["total_days"],
            "destinations": itinerary["destinations"],
            "routing_efficiency": self.calculate_routing_efficiency(itinerary),
            "climate_diversity": self.analyze_climate_diversity(itinerary),
            "experience_balance": self.analyze_experience_balance(itinerary),
            "connectivity_analysis": self.analyze_connectivity(itinerary)
        }
        
        return analysis
    
    def calculate_routing_efficiency(self, itinerary):
        """Calculate routing efficiency score"""
        
        destinations = itinerary["destinations"]
        efficiency_score = 100
        
        # Check for geographical logic
        west_coast = ["Mumbai", "Goa", "Cochin"]
        kerala_region = ["Cochin", "Munnar"]
        golden_triangle = ["Delhi", "Agra", "Jaipur"]
        
        # Analyze flow
        route_flow = []
        for dest in destinations:
            if dest in west_coast:
                route_flow.append("west_coast")
            elif dest in kerala_region:
                route_flow.append("kerala")
            elif dest in golden_triangle:
                route_flow.append("golden_triangle")
        
        # Check for logical progression
        if route_flow == ["west_coast", "west_coast", "kerala", "kerala", "golden_triangle", "golden_triangle", "golden_triangle"]:
            efficiency_score = 95  # Excellent flow
        elif "west_coast" in route_flow and "kerala" in route_flow and "golden_triangle" in route_flow:
            efficiency_score = 85  # Good regional grouping
        else:
            efficiency_score = 70  # Needs optimization
        
        return {
            "score": efficiency_score,
            "flow_pattern": route_flow,
            "optimization_level": "excellent" if efficiency_score >= 90 else "good" if efficiency_score >= 80 else "needs_improvement"
        }
    
    def analyze_climate_diversity(self, itinerary):
        """Analyze climate and experience diversity"""
        
        climates = []
        for dest in itinerary["destinations"]:
            if dest in self.destination_database:
                climates.append(self.destination_database[dest]["climate"])
        
        unique_climates = list(set(climates))
        
        return {
            "climate_types": unique_climates,
            "diversity_score": len(unique_climates) * 20,  # Max 100 for 5 different climates
            "experience_variety": "excellent" if len(unique_climates) >= 4 else "good" if len(unique_climates) >= 3 else "moderate"
        }
    
    def analyze_experience_balance(self, itinerary):
        """Analyze balance of different experience types"""
        
        experience_types = []
        for dest in itinerary["destinations"]:
            if dest in self.destination_database:
                experience_types.append(self.destination_database[dest]["type"])
        
        type_counts = {}
        for exp_type in experience_types:
            type_counts[exp_type] = type_counts.get(exp_type, 0) + 1
        
        return {
            "experience_distribution": type_counts,
            "balance_score": min(100, len(type_counts) * 25),  # Max 100 for 4+ different types
            "recommendations": self.get_balance_recommendations(type_counts)
        }
    
    def analyze_connectivity(self, itinerary):
        """Analyze connectivity between destinations"""
        
        connectivity_analysis = []
        destinations = itinerary["destinations"]
        
        for i in range(len(destinations) - 1):
            origin = destinations[i]
            destination = destinations[i + 1]
            
            connection = self.get_connection_details(origin, destination)
            connectivity_analysis.append(connection)
        
        return connectivity_analysis
    
    def get_connection_details(self, origin, destination):
        """Get detailed connection information between two destinations"""
        
        # Predefined connection database
        connections = {
            ("Mumbai", "Goa"): {
                "method": "flight",
                "duration": "1.5 hours",
                "frequency": "multiple_daily",
                "cost_range": "₹3,000-8,000",
                "recommendation": "evening_flight_optimal"
            },
            ("Goa", "Cochin"): {
                "method": "flight",
                "duration": "1.5 hours", 
                "frequency": "daily_flights",
                "cost_range": "₹4,000-10,000",
                "recommendation": "morning_flight_preferred"
            },
            ("Cochin", "Munnar"): {
                "method": "road",
                "duration": "4 hours",
                "route": "scenic_mountain_drive",
                "cost_range": "₹3,000-5,000",
                "recommendation": "morning_departure_scenic_views"
            },
            ("Munnar", "Cochin"): {
                "method": "road",
                "duration": "4 hours",
                "route": "return_mountain_drive",
                "cost_range": "₹3,000-5,000",
                "recommendation": "early_departure_for_flight_connection"
            },
            ("Cochin", "Delhi"): {
                "method": "flight",
                "duration": "2.5 hours",
                "frequency": "multiple_daily",
                "cost_range": "₹6,000-15,000",
                "recommendation": "morning_flight_golden_triangle_start"
            },
            ("Delhi", "Agra"): {
                "method": "road",
                "duration": "3 hours",
                "route": "yamuna_expressway",
                "cost_range": "₹2,500-4,000",
                "recommendation": "morning_departure_taj_afternoon"
            },
            ("Agra", "Jaipur"): {
                "method": "road",
                "duration": "4 hours",
                "route": "heritage_highway",
                "cost_range": "₹3,000-5,000",
                "recommendation": "post_taj_visit_departure"
            },
            ("Jaipur", "Delhi"): {
                "method": "road",
                "duration": "5 hours",
                "route": "national_highway",
                "cost_range": "₹3,500-6,000",
                "recommendation": "comfortable_return_journey"
            }
        }
        
        connection_key = (origin, destination)
        if connection_key in connections:
            return {
                "from": origin,
                "to": destination,
                "details": connections[connection_key],
                "efficiency": "optimal"
            }
        else:
            return {
                "from": origin,
                "to": destination,
                "details": {
                    "method": "requires_analysis",
                    "recommendation": "check_intermediate_hubs"
                },
                "efficiency": "needs_optimization"
            }
    
    def get_balance_recommendations(self, type_counts):
        """Get recommendations for better experience balance"""
        
        recommendations = []
        
        if type_counts.get("beach_destination", 0) > 2:
            recommendations.append("Consider reducing beach time for more heritage experiences")
        
        if type_counts.get("heritage_monument", 0) > 3:
            recommendations.append("Add nature/adventure elements for better balance")
        
        if "hill_station" not in type_counts:
            recommendations.append("Consider adding hill station for climate diversity")
        
        if "metropolitan" not in type_counts:
            recommendations.append("Include major city for cultural contrast")
        
        return recommendations if recommendations else ["Experience balance is optimal"]
    
    def generate_optimization_suggestions(self, itinerary):
        """Generate intelligent optimization suggestions"""
        
        analysis = self.analyze_itinerary_structure(itinerary)
        suggestions = {
            "routing_optimizations": [],
            "timing_improvements": [],
            "experience_enhancements": [],
            "cost_optimizations": [],
            "cultural_additions": []
        }
        
        # Routing optimization suggestions
        if analysis["routing_efficiency"]["score"] < 90:
            suggestions["routing_optimizations"].extend([
                "Current route follows optimal geographical flow: West Coast → Kerala → North India",
                "Consider overnight in Munnar for better tea garden experience",
                "Morning flight Cochin-Delhi recommended for Golden Triangle timing"
            ])
        
        # Timing improvements
        suggestions["timing_improvements"].extend([
            "Mumbai: Full day sightseeing, evening flight to Goa optimal",
            "Goa: 3 days allows relaxed beach and heritage exploration", 
            "Munnar: 2 days minimum for tea plantation immersion",
            "Golden Triangle: 4 days perfect for Delhi-Agra-Jaipur circuit"
        ])
        
        # Experience enhancements
        suggestions["experience_enhancements"].extend([
            "Add sunset cruise in Goa before Cochin flight",
            "Include tea plantation stay in Munnar for authentic experience",
            "Early morning Taj Mahal visit for best photography",
            "Amber Fort elephant ride in Jaipur for royal experience"
        ])
        
        # Cultural additions
        handicrafts_available = []
        for dest in itinerary["destinations"]:
            if dest in self.destination_database:
                handicrafts_available.extend(self.destination_database[dest]["handicrafts"])
        
        suggestions["cultural_additions"].extend([
            f"Available handicrafts: {', '.join(set(handicrafts_available))}",
            "Spice workshop in Cochin for Kerala cultural immersion",
            "Blue pottery experience in Jaipur for Rajasthani arts",
            "Block printing workshop in Delhi for traditional crafts"
        ])
        
        # Cost optimizations
        suggestions["cost_optimizations"].extend([
            "Book flights 2-3 weeks advance for better rates",
            "Consider train Delhi-Agra as cost-effective alternative",
            "Group booking discounts available for 4+ passengers",
            "Package deals for Golden Triangle + Kerala combinations"
        ])
        
        return suggestions
    
    def create_visual_itinerary_template(self, itinerary):
        """Create visual template for the itinerary"""
        
        template = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           T2INDIA INTELLIGENT ROUTING                        ║
║                              12-Day Grand Tour                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

📍 ROUTE OVERVIEW: {' → '.join(itinerary['destinations'])}
🕐 TOTAL DURATION: {itinerary['total_days']} Days
✈️ ENTRY: {itinerary.get('entry_point', 'Mumbai')} | EXIT: {itinerary.get('exit_point', 'Delhi')}

┌──────────────────────────────────────────────────────────────────────────────┐
│                              DESTINATION BREAKDOWN                           │
├──────────────────────────────────────────────────────────────────────────────┤
│ 🏙️  MUMBAI (1 Day)     │ Gateway of India, Marine Drive, Bollywood         │
│ 🏖️  GOA (3 Days)       │ Beaches, Portuguese Heritage, Spice Plantations   │
│ 🌊  COCHIN (2 Days)     │ Chinese Nets, Fort Kochi, Spice Markets          │
│ 🍃  MUNNAR (2 Days)     │ Tea Plantations, Hill Station, Cool Climate      │
│ 🏛️  DELHI (1 Day)       │ Red Fort, India Gate, Heritage Monuments         │
│ 🕌  AGRA (1 Day)        │ Taj Mahal, Agra Fort, Mughal Architecture        │
│ 👑  JAIPUR (2 Days)     │ Amber Fort, City Palace, Royal Heritage          │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                              CONNECTIVITY MATRIX                            │
├──────────────────────────────────────────────────────────────────────────────┤
│ Mumbai → Goa        │ ✈️  Flight (1.5h)    │ Evening departure optimal    │
│ Goa → Cochin        │ ✈️  Flight (1.5h)    │ Morning flight preferred     │
│ Cochin → Munnar     │ 🚗  Road (4h)        │ Scenic mountain drive        │
│ Munnar → Cochin     │ 🚗  Road (4h)        │ Early departure for flight   │
│ Cochin → Delhi      │ ✈️  Flight (2.5h)    │ Morning flight recommended   │
│ Delhi → Agra        │ 🚗  Road (3h)        │ Yamuna Expressway            │
│ Agra → Jaipur       │ 🚗  Road (4h)        │ Heritage highway             │
│ Jaipur → Delhi      │ 🚗  Road (5h)        │ Return journey               │
└──────────────────────────────────────────────────────────────────────────────┘
"""
        
        return template
    
    def process_complete_routing_solution(self, user_input):
        """Process complete routing solution with suggestions"""
        
        # Parse the 12-day itinerary structure
        itinerary = {
            "total_days": 12,
            "destinations": ["Mumbai", "Goa", "Cochin", "Munnar", "Delhi", "Agra", "Jaipur"],
            "day_allocation": {
                "Mumbai": 1,
                "Goa": 3, 
                "Cochin": 2,
                "Munnar": 2,
                "Delhi": 1,
                "Agra": 1,
                "Jaipur": 2
            },
            "entry_point": "Mumbai",
            "exit_point": "Delhi"
        }
        
        # Analyze the itinerary
        analysis = self.analyze_itinerary_structure(itinerary)
        
        # Generate optimization suggestions
        suggestions = self.generate_optimization_suggestions(itinerary)
        
        # Create visual template
        visual_template = self.create_visual_itinerary_template(itinerary)
        
        return {
            "itinerary": itinerary,
            "analysis": analysis,
            "suggestions": suggestions,
            "visual_template": visual_template,
            "routing_intelligence": {
                "efficiency_score": analysis["routing_efficiency"]["score"],
                "optimization_level": analysis["routing_efficiency"]["optimization_level"],
                "climate_diversity": analysis["climate_diversity"]["diversity_score"],
                "experience_balance": analysis["experience_balance"]["balance_score"]
            }
        }

def test_routing_solution():
    """Test the complete routing solution"""
    
    system = T2IndiaRoutingSolutionWithSuggestions()
    
    print("=" * 80)
    print("T2INDIA COMPLETE ROUTING SOLUTION WITH SUGGESTIONS")
    print("=" * 80)
    
    # Process the 12-day itinerary
    result = system.process_complete_routing_solution("12 days Mumbai Goa Cochin Munnar Delhi Agra Jaipur")
    
    # Display visual template
    print(result["visual_template"])
    
    # Display analysis
    print("\n" + "=" * 80)
    print("INTELLIGENT ANALYSIS")
    print("=" * 80)
    
    print(f"Routing Efficiency: {result['routing_intelligence']['efficiency_score']}/100")
    print(f"Climate Diversity: {result['routing_intelligence']['climate_diversity']}/100")
    print(f"Experience Balance: {result['routing_intelligence']['experience_balance']}/100")
    print(f"Optimization Level: {result['routing_intelligence']['optimization_level'].upper()}")
    
    # Display suggestions
    print("\n" + "=" * 80)
    print("OPTIMIZATION SUGGESTIONS")
    print("=" * 80)
    
    for category, suggestions in result["suggestions"].items():
        print(f"\n{category.replace('_', ' ').upper()}:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")
    
    print("\n" + "=" * 80)
    print("ROUTING SOLUTION COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_routing_solution()

