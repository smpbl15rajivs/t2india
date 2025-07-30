"""
T2India Integrated System with Intermediate Connectivity
Complete implementation with A→C→B routing logic
"""

from t2india_comprehensive_system import T2IndiaComprehensiveSystem
from intermediate_connectivity_system import IntermediateConnectivitySystem

class T2IndiaIntegratedSystem:
    def __init__(self):
        self.comprehensive_system = T2IndiaComprehensiveSystem()
        self.connectivity_system = IntermediateConnectivitySystem()
    
    def process_query_with_connectivity(self, user_input):
        """Process query with full connectivity analysis"""
        
        # Get comprehensive analysis
        comprehensive_result = self.comprehensive_system.process_comprehensive_query(user_input)
        
        # Add intermediate connectivity analysis
        route = comprehensive_result['recommendation']['optimized_route']
        connectivity_analysis = {}
        
        for i in range(len(route) - 1):
            origin = route[i]
            destination = route[i + 1]
            
            # Get all routing options including intermediate hubs
            routing_options = self.connectivity_system.get_all_possible_routes(origin, destination)
            connectivity_analysis[f"{origin}→{destination}"] = routing_options
        
        # Integrate connectivity into comprehensive result
        comprehensive_result['intermediate_connectivity'] = connectivity_analysis
        
        return comprehensive_result
    
    def format_integrated_output(self, result):
        """Format output with connectivity details"""
        
        # Start with comprehensive output
        output = self.comprehensive_system.format_comprehensive_output(result)
        
        # Add intermediate connectivity section
        if 'intermediate_connectivity' in result:
            output += "\n=== INTERMEDIATE CONNECTIVITY ANALYSIS ===\n"
            
            for route_segment, routing_options in result['intermediate_connectivity'].items():
                output += f"\n{route_segment.replace('→', ' → ')}:\n"
                
                primary_route = routing_options[0]
                
                if primary_route.get('direct_connection'):
                    output += "  ✓ Direct connection available\n"
                else:
                    hub = primary_route['intermediate_hub']
                    output += f"  → Via {hub} (Intermediate Hub)\n"
                    
                    if 'leg1' in primary_route:
                        leg1 = primary_route['leg1']
                        if 'time' in leg1:
                            output += f"    Leg 1: {leg1['time']} by {leg1['transport']}\n"
                    
                    # Calculate total time
                    time_analysis = self.connectivity_system.calculate_total_journey_time(primary_route)
                    output += f"    Total Journey: {time_analysis['total_time']}\n"
                    
                    # Show alternatives if available
                    if len(routing_options) > 1:
                        output += f"    Alternatives: {len(routing_options) - 1} other hub options\n"
        
        return output

def test_integrated_system():
    """Test the fully integrated system"""
    
    system = T2IndiaIntegratedSystem()
    
    test_queries = [
        "Hampi to Delhi for 5 days",
        "Darjeeling to Mumbai spiritual journey 8 days", 
        "Cochin Goa Hampi Delhi Kolkata for 18 days",
        "Rishikesh yoga retreat to Kolkata 10 days"
    ]
    
    print("=" * 80)
    print("T2INDIA INTEGRATED SYSTEM - FULL TESTING")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n{'='*20} QUERY: {query} {'='*20}")
        
        result = system.process_query_with_connectivity(query)
        formatted_output = system.format_integrated_output(result)
        
        # Print summary
        print(f"Query ID: {result['query_id']}")
        print(f"Route: {' → '.join(result['recommendation']['optimized_route'])}")
        print(f"Connectivity Segments: {len(result.get('intermediate_connectivity', {}))}")
        
        # Count intermediate hubs needed
        hub_count = 0
        for routing_options in result.get('intermediate_connectivity', {}).values():
            if not routing_options[0].get('direct_connection'):
                hub_count += 1
        
        print(f"Intermediate Hubs Required: {hub_count}")
        print("-" * 60)
    
    print(f"\n{'='*80}")
    print("INTEGRATED SYSTEM TESTING COMPLETED")
    print(f"{'='*80}")

if __name__ == "__main__":
    test_integrated_system()

