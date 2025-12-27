import json
from datetime import datetime
from utils.ui import print_success, print_error

def save_to_json(data, target_name, report_type):
    """Saves scan data to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{report_type}_{target_name.replace('.', '_')}_{timestamp}.json"
    
    report_data = {
        "target": target_name,
        "type": report_type,
        "timestamp": datetime.now().isoformat(),
        "results": data
    }
    
    try:
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=4)
        print_success(f"Report saved to: [bold yellow]{filename}[/bold yellow]")
        return filename
    except Exception as e:
        print_error(f"Failed to save report: {e}")
        return None
