import sys
from src.milestone_1.phase_2_preferences.parser import parse_preferences
from src.milestone_1.pipeline.orchestrator import Orchestrator
from src.milestone_1.phase_5_output.formatter import format_as_terminal

def main():
    """
    Main entry point for the CLI interface.
    """
    print("\n" + "="*40)
    print("AI RESTAURANT RECOMMENDER CLI")
    print("="*40 + "\n")
    
    try:
        location = input("Enter location (e.g., Delhi, Bellandur): ").strip()
        if not location:
            print("Location is required.")
            return
            
        cuisines = input("Enter cuisines (comma separated, e.g., Italian, Chinese): ").strip()
        if not cuisines:
            print("At least one cuisine is required.")
            return
            
        budget_mode = input("Budget mode (category/range) [category]: ").strip().lower() or "category"
        
        data = {
            "location": location,
            "cuisines": cuisines,
            "budget_mode": budget_mode
        }
        
        if budget_mode == "category":
            data["category"] = input("Category (low/medium/high) [medium]: ").strip().lower() or "medium"
        else:
            try:
                min_c = input("Min cost [0]: ").strip()
                data["min_cost"] = int(min_c) if min_c else 0
                max_c = input("Max cost [1000]: ").strip()
                data["max_cost"] = int(max_c) if max_c else 1000
            except ValueError:
                print("Invalid cost format. Using defaults.")
                data["min_cost"] = 0
                data["max_cost"] = 1000
        
        min_rating = input("Minimum rating (0-5) [3.5]: ").strip()
        data["min_rating"] = float(min_rating) if min_rating else 3.5
        
        print("\n" + "-"*40)
        print("Parsing preferences...")
        prefs = parse_preferences(data)
        
        print("Running recommendation pipeline...")
        recommendations = Orchestrator.run(prefs)
        
        print("\nRESULTS:")
        print(format_as_terminal(recommendations))
        
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
