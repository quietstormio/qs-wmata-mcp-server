from typing import Any, List, Dict, Optional
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import json
import os

mcp = FastMCP("wmata-metro-guide")
WMATA_API_BASE = "https://api.wmata.com"
WMATA_API_KEY = os.environ.get('WMATA_API_KEY')

# Enhanced station mapping with line information
STATION_MAPPING = {
    "Metro Center": "C01",
    "Farragut North": "A02",
    "Dupont Circle": "A03",
    "Woodley Park-Zoo/Adams Morgan": "A04",
    "Cleveland Park": "A05",
    "Van Ness-UDC": "A06",
    "Tenleytown-AU": "A07",
    "Friendship Heights": "A08",
    "Bethesda": "A09",
    "Medical Center": "A10",
    "Grosvenor-Strathmore": "A11",
    "North Bethesda": "A12",
    "Twinbrook": "A13",
    "Rockville": "A14",
    "Shady Grove": "A15",
    "Gallery Pl-Chinatown": "F01",
    "Judiciary Square": "B02",
    "Union Station": "B03",
    "Rhode Island Ave-Brentwood": "B04",
    "Brookland-CUA": "B05",
    "Fort Totten": "E06",
    "Takoma": "B07",
    "Silver Spring": "B08",
    "Forest Glen": "B09",
    "Wheaton": "B10",
    "Glenmont": "B11",
    "NoMa-Gallaudet U": "B35",
    "McPherson Square": "C02",
    "Farragut West": "C03",
    "Foggy Bottom-GWU": "C04",
    "Rosslyn": "C05",
    "Arlington Cemetery": "C06",
    "Pentagon": "C07",
    "Pentagon City": "C08",
    "Crystal City": "C09",
    "Ronald Reagan Washington National Airport": "C10",
    "Potomac Yard": "C11",
    "Braddock Road": "C12",
    "King St-Old Town": "C13",
    "Eisenhower Avenue": "C14",
    "Huntington": "C15",
    "Federal Triangle": "D01",
    "Smithsonian": "D02",
    "L'Enfant Plaza": "F03",
    "Federal Center SW": "D04",
    "Capitol South": "D05",
    "Eastern Market": "D06",
    "Potomac Ave": "D07",
    "Stadium-Armory": "D08",
    "Minnesota Ave": "D09",
    "Deanwood": "D10",
    "Cheverly": "D11",
    "Landover": "D12",
    "New Carrollton": "D13",
    "Mt Vernon Sq 7th St-Convention Center": "E01",
    "Shaw-Howard U": "E02",
    "U Street/African-Amer Civil War Memorial/Cardozo": "E03",
    "Columbia Heights": "E04",
    "Georgia Ave-Petworth": "E05",
    "West Hyattsville": "E07",
    "Hyattsville Crossing": "E08",
    "College Park-U of Md": "E09",
    "Greenbelt": "E10",
    "Archives-Navy Memorial-Penn Quarter": "F02",
    "Waterfront": "F04",
    "Navy Yard-Ballpark": "F05",
    "Anacostia": "F06",
    "Congress Heights": "F07",
    "Southern Avenue": "F08",
    "Naylor Road": "F09",
    "Suitland": "F10",
    "Branch Ave": "F11",
    "Benning Road": "G01",
    "Capitol Heights": "G02",
    "Addison Road-Seat Pleasant": "G03",
    "Morgan Boulevard": "G04",
    "Downtown Largo": "G05",
    "Van Dorn Street": "J02",
    "Franconia-Springfield": "J03",
    "Court House": "K01",
    "Clarendon": "K02",
    "Virginia Square-GMU": "K03",
    "Ballston-MU": "K04",
    "East Falls Church": "K05",
    "West Falls Church": "K06",
    "Dunn Loring-Merrifield": "K07",
    "Vienna/Fairfax-GMU": "K08",
    "McLean": "N01",
    "Tysons": "N02",
    "Greensboro": "N03",
    "Spring Hill": "N04",
    "Wiehle-Reston East": "N06",
    "Reston Town Center": "N07",
    "Herndon": "N08",
    "Innovation Center": "N09",
    "Washington Dulles International Airport": "N10",
    "Loudoun Gateway": "N11",
    "Ashburn": "N12"
}

# Line colors for better user experience
LINE_COLORS = {
    "RD": "Red Line",
    "BL": "Blue Line",
    "YL": "Yellow Line",
    "OR": "Orange Line",
    "GR": "Green Line",
    "SV": "Silver Line"
}

# Station lines mapping (which lines serve each station)
STATION_LINES = {
    # Red Line
    "A01": ["RD"], "A02": ["RD"], "A03": ["RD"], "A04": ["RD"], "A05": ["RD"], 
    "A06": ["RD"], "A07": ["RD"], "A08": ["RD"], "A09": ["RD"], "A10": ["RD"],
    "A11": ["RD"], "A12": ["RD"], "A13": ["RD"], "A14": ["RD"], "A15": ["RD"],
    "B02": ["RD"], "B03": ["RD"], "B04": ["RD"], "B05": ["RD"], "B06": ["RD"],
    "B07": ["RD"], "B08": ["RD"], "B09": ["RD"], "B10": ["RD"], "B11": ["RD"], "B35": ["RD"],
    
    # Blue/Orange/Silver Line stations
    "C01": ["RD", "BL", "OR", "SV"], "C02": ["BL", "OR", "SV"], "C03": ["BL", "OR", "SV"],
    "C04": ["BL", "OR", "SV"], "C05": ["BL", "OR", "SV"], "C06": ["BL"], "C07": ["BL", "YL"],
    "C08": ["BL", "YL"], "C09": ["BL", "YL"], "C10": ["BL", "YL"], "C11": ["BL", "YL"],
    "C12": ["BL", "YL"], "C13": ["BL", "YL"], "C14": ["BL"], "C15": ["BL"],
    
    # Orange/Silver Line
    "D01": ["OR", "SV"], "D02": ["OR", "SV"], "D03": ["OR"], "D04": ["OR", "SV"],
    "D05": ["OR", "SV"], "D06": ["OR", "SV"], "D07": ["OR", "SV"], "D08": ["OR", "SV"],
    "D09": ["OR"], "D10": ["OR"], "D11": ["OR"], "D12": ["OR"], "D13": ["OR", "SV"],
    
    # Green/Yellow Line
    "E01": ["GR", "YL"], "E02": ["GR"], "E03": ["GR"], "E04": ["GR"],
    "E05": ["GR"], "E06": ["RD", "GR"], "E07": ["GR"], "E08": ["GR"],
    "E09": ["GR"], "E10": ["GR"],
    
    # Gallery Place / L'Enfant Plaza connections
    "F01": ["RD", "GR", "YL"], "F02": ["GR", "YL"], "F03": ["BL", "OR", "SV", "GR", "YL"],
    "F04": ["GR"], "F05": ["GR"], "F06": ["GR"], "F07": ["GR"], "F08": ["GR"],
    "F09": ["GR"], "F10": ["GR"], "F11": ["GR"],
    
    # Other stations
    "G01": ["BL"], "G02": ["BL"], "G03": ["BL"], "G04": ["BL"], "G05": ["BL", "SV"],
    "J02": ["BL"], "J03": ["BL"],
    
    # Orange/Silver Line (Arlington)
    "K01": ["OR", "SV"], "K02": ["OR", "SV"], "K03": ["OR", "SV"], "K04": ["OR", "SV"],
    "K05": ["OR", "SV"], "K06": ["OR", "SV"], "K07": ["OR", "SV"], "K08": ["OR", "SV"],
    
    # Silver Line
    "N01": ["SV"], "N02": ["SV"], "N03": ["SV"], "N04": ["SV"], "N06": ["SV"],
    "N07": ["SV"], "N08": ["SV"], "N09": ["SV"], "N10": ["SV"], "N11": ["SV"], "N12": ["SV"]
}

# Simple routing for common transfer patterns
COMMON_ROUTES = {
    # From Union Station (B03) to various destinations
    ("B03", "C07"): [  # Union Station to Pentagon
        {"station": "B03", "name": "Union Station", "line": "RD", "action": "start"},
        {"station": "C01", "name": "Metro Center", "line": "RD", "action": "transfer"},
        {"station": "C01", "name": "Metro Center", "line": "BL", "action": "board"},
        {"station": "C07", "name": "Pentagon", "line": "BL", "action": "arrive"}
    ],
    # From Dupont Circle to National Airport
    ("A03", "C10"): [
        {"station": "A03", "name": "Dupont Circle", "line": "RD", "action": "start"},
        {"station": "C01", "name": "Metro Center", "line": "RD", "action": "transfer"},
        {"station": "C01", "name": "Metro Center", "line": "BL", "action": "board"},
        {"station": "C10", "name": "Ronald Reagan Washington National Airport", "line": "BL", "action": "arrive"}
    ],
    # From Gallery Place to Rosslyn
    ("F01", "C05"): [
        {"station": "F01", "name": "Gallery Pl-Chinatown", "line": "RD", "action": "start"},
        {"station": "C01", "name": "Metro Center", "line": "RD", "action": "transfer"},
        {"station": "C01", "name": "Metro Center", "line": "OR", "action": "board"},
        {"station": "C05", "name": "Rosslyn", "line": "OR", "action": "arrive"}
    ]
}

async def make_wmata_request(url: str, params: dict = None) -> dict[str, Any] | None:
    """Make a request to WMATA API with error handling"""
    headers = {
        "Cache-Control": "no-cache",
        "api_key": WMATA_API_KEY,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

def get_station_code(station_name: str) -> str | None:
    """Convert station name to station code with fuzzy matching"""
    # Exact match first
    if station_name in STATION_MAPPING:
        return STATION_MAPPING[station_name]
    
    # If it's already a code, return uppercase
    if len(station_name) <= 3 and station_name.upper() in STATION_MAPPING.values():
        return station_name.upper()
    
    # Fuzzy matching for partial names
    for name, code in STATION_MAPPING.items():
        if station_name.lower() in name.lower() or name.lower().startswith(station_name.lower()):
            return code
    
    return None

def format_train_prediction(train: dict) -> str:
    """Format a single train prediction"""
    line = LINE_COLORS.get(train.get("Line", ""), train.get("Line", "Unknown"))
    destination = train.get("DestinationName", "Unknown")
    minutes = train.get("Min", "Unknown")
    cars = train.get("Car", "Unknown")
    
    if minutes == "ARR":
        time_info = "Arriving now"
    elif minutes == "BRD":
        time_info = "Boarding"
    else:
        time_info = f"{minutes} minutes"
    
    return f"🚇 {line} to {destination} - {time_info} ({cars} cars)"

def find_simple_route(from_code: str, to_code: str) -> List[Dict] | None:
    """Find a simple route using pre-defined common routes"""
    # Check direct route
    route_key = (from_code, to_code)
    if route_key in COMMON_ROUTES:
        return COMMON_ROUTES[route_key]
    
    # Check reverse route
    reverse_key = (to_code, from_code)
    if reverse_key in COMMON_ROUTES:
        route = list(reversed(COMMON_ROUTES[reverse_key]))
        # Update actions for reverse direction
        for step in route:
            if step["action"] == "start":
                step["action"] = "arrive"
            elif step["action"] == "arrive":
                step["action"] = "start"
        return route
    
    # Check if stations are on the same line
    from_lines = STATION_LINES.get(from_code, [])
    to_lines = STATION_LINES.get(to_code, [])
    common_lines = set(from_lines) & set(to_lines)
    
    if common_lines:
        line = list(common_lines)[0]
        from_name = next((name for name, code in STATION_MAPPING.items() if code == from_code), from_code)
        to_name = next((name for name, code in STATION_MAPPING.items() if code == to_code), to_code)
        return [
            {"station": from_code, "name": from_name, "line": line, "action": "start"},
            {"station": to_code, "name": to_name, "line": line, "action": "arrive"}
        ]
    
    return None

def find_optimal_transfer_point(from_code: str, to_code: str) -> str | None:
    """Find the closest transfer point between two stations on different lines"""
    from_lines = set(STATION_LINES.get(from_code, []))
    to_lines = set(STATION_LINES.get(to_code, []))
    
    # If they share a line, no transfer needed
    if from_lines & to_lines:
        return None
    
    # Find all possible transfer stations
    transfer_candidates = []
    
    for station_code, lines in STATION_LINES.items():
        station_lines = set(lines)
        # Station must connect to both origin and destination lines
        if (station_lines & from_lines) and (station_lines & to_lines):
            # Calculate "distance" (you could use actual station positions)
            transfer_candidates.append(station_code)
    
    # For now, prefer smaller transfer stations over major hubs
    # You could rank by proximity or other factors
    major_hubs = {"C01", "F01", "F03"}  # Metro Center, Gallery Place, L'Enfant
    
    # Return non-hub transfers first
    for candidate in transfer_candidates:
        if candidate not in major_hubs:
            return candidate
    
    # Fall back to major hubs if no other option
    return transfer_candidates[0] if transfer_candidates else None

def build_optimal_route(from_code: str, to_code: str) -> List[Dict] | None:
    """Build an optimal route with smart transfer selection"""
    from_name = next((name for name, code in STATION_MAPPING.items() if code == from_code), from_code)
    to_name = next((name for name, code in STATION_MAPPING.items() if code == to_code), to_code)
    
    from_lines = set(STATION_LINES.get(from_code, []))
    to_lines = set(STATION_LINES.get(to_code, []))
    
    # Direct route on same line
    common_lines = from_lines & to_lines
    if common_lines:
        line = list(common_lines)[0]
        return [
            {"station": from_code, "name": from_name, "line": line, "action": "start"},
            {"station": to_code, "name": to_name, "line": line, "action": "arrive"}
        ]
    
    # Find optimal transfer point
    transfer_code = find_optimal_transfer_point(from_code, to_code)
    if transfer_code:
        transfer_name = next((name for name, code in STATION_MAPPING.items() if code == transfer_code), transfer_code)
        
        # Choose lines for each segment
        first_line = list(from_lines & set(STATION_LINES.get(transfer_code, [])))[0]
        second_line = list(to_lines & set(STATION_LINES.get(transfer_code, [])))[0]
        
        return [
            {"station": from_code, "name": from_name, "line": first_line, "action": "start"},
            {"station": transfer_code, "name": transfer_name, "line": first_line, "action": "transfer_to", "next_line": second_line},
            {"station": to_code, "name": to_name, "line": second_line, "action": "arrive"}
        ]
    
    return None

# === TOOLS ===

@mcp.tool()
async def get_train_prediction(station: str) -> str:
    """
    Get live train predictions for a Metro station.
    
    Args:
        station: Station name or code (e.g., "Union Station", "B03")
    
    Returns:
        Formatted train arrival predictions
    """
    station_code = get_station_code(station)
    
    if not station_code:
        return f"❌ Station '{station}' not found. Please check the spelling or use a valid station name."

    url = f"{WMATA_API_BASE}/StationPrediction.svc/json/GetPrediction/{station_code}"
    data = await make_wmata_request(url)

    if not data or "Trains" not in data:
        return "❌ Unable to get train predictions. The service may be unavailable."
    
    if not data["Trains"]:
        return "ℹ️ No train predictions available. Metro may be closed or experiencing service disruptions."

    predictions = [format_train_prediction(train) for train in data["Trains"]]
    station_name = next((name for name, code in STATION_MAPPING.items() if code == station_code), station)
    
    return f"🚉 **{station_name}** Train Predictions:\n\n" + "\n".join(predictions)

@mcp.tool()
async def get_station_to_station_info(from_station: str, to_station: str) -> str:
    """
    Get travel information between two Metro stations using WMATA's actual API.
    
    Args:
        from_station: Starting station name or code
        to_station: Destination station name or code
    
    Returns:
        Travel time, fare, and basic routing information
    """
    from_code = get_station_code(from_station)
    to_code = get_station_code(to_station)
    
    if not from_code:
        return f"❌ Starting station '{from_station}' not found."
    if not to_code:
        return f"❌ Destination station '{to_station}' not found."
    
    if from_code == to_code:
        return "ℹ️ You're already at your destination!"

    # Use the actual WMATA API endpoint for station-to-station information
    url = f"{WMATA_API_BASE}/Rail.svc/json/jSrcStationToDstStationInfo"
    params = {"FromStationCode": from_code, "ToStationCode": to_code}
    
    data = await make_wmata_request(url, params)

    if not data or "StationToStationInfos" not in data:
        return "❌ Unable to get travel information between these stations."

    infos = data["StationToStationInfos"]
    if not infos:
        return "❌ No travel information available for this route."

    # Get station names
    from_name = next((name for name, code in STATION_MAPPING.items() if code == from_code), from_station)
    to_name = next((name for name, code in STATION_MAPPING.items() if code == to_code), to_station)

    info = infos[0]
    route_info = f"🗺️ **Travel from {from_name} to {to_name}**\n\n"
    
    # Travel time
    travel_time = info.get("RailTime")
    if travel_time:
        route_info += f"⏱️ **Estimated travel time:** {travel_time} minutes\n"
    
    # Fare information
    rail_fare = info.get("RailFare", {})
    if rail_fare:
        peak_fare = rail_fare.get("PeakTime")
        off_peak_fare = rail_fare.get("OffPeakTime")
        
        if peak_fare:
            route_info += f"💳 **Peak fare:** ${peak_fare:.2f}\n"
        if off_peak_fare:
            route_info += f"💳 **Off-peak fare:** ${off_peak_fare:.2f}\n"
    
    # Try to provide basic routing guidance
    route_steps = build_optimal_route(from_code, to_code)  # Use new function
    if route_steps:
        route_info += f"\n📍 **Recommended route:**\n"
        for i, step in enumerate(route_steps, 1):
            action = step["action"]
            station_name = step["name"]
            line = LINE_COLORS.get(step["line"], step["line"])
            
            if action == "start":
                route_info += f"{i}. Board {line} at **{station_name}**\n"
            elif action == "transfer_to":
                next_line = LINE_COLORS.get(step["next_line"], step["next_line"])
                route_info += f"{i}. Transfer at **{station_name}** from {line} to {next_line}\n"
            elif action == "arrive":
                route_info += f"{i}. Arrive at **{station_name}** on {line}\n"
    else:
        route_info += f"\n⚠️ **Note:** This route may require transfers.\n"
        route_info += f"Check service alerts and plan your connections at major transfer stations:\n"
        route_info += f"• Metro Center (Red/Blue/Orange/Silver)\n"
        route_info += f"• Gallery Place (Red/Green/Yellow)\n"
        route_info += f"• L'Enfant Plaza (Blue/Orange/Silver/Green/Yellow)\n"
    
    route_info += f"\n💡 **Travel tips:**\n"
    route_info += f"• Check train predictions before departing\n"
    route_info += f"• Stand right, walk left on escalators\n"
    route_info += f"• Consider checking service alerts before your trip"

    return route_info

@mcp.tool()
async def get_service_alerts() -> str:
    """
    Get current Metro service alerts and incidents.
    
    Returns:
        Current service disruptions and alerts
    """
    url = f"{WMATA_API_BASE}/Incidents.svc/json/Incidents"
    data = await make_wmata_request(url)

    if not data or "Incidents" not in data:
        return "❌ Unable to get service alerts."

    incidents = data["Incidents"]
    
    if not incidents:
        return "✅ No current service alerts. All Metro services are operating normally."

    alerts = []
    for incident in incidents:
        incident_type = incident.get("IncidentType", "Unknown")
        description = incident.get("Description", "No description available")
        lines_affected = incident.get("LinesAffected", "Unknown")
        
        alert = f"⚠️ **{incident_type}**"
        if lines_affected and lines_affected != "Unknown":
            line_names = [LINE_COLORS.get(line, line) for line in lines_affected.split(";")]
            alert += f" - {', '.join(line_names)}"
        alert += f"\n{description}\n"
        alerts.append(alert)

    return "🚨 **Current Metro Service Alerts:**\n\n" + "\n".join(alerts)

@mcp.tool()
async def get_elevator_outages() -> str:
    """
    Get current elevator and escalator outages affecting accessibility.
    
    Returns:
        List of accessibility equipment outages
    """
    url = f"{WMATA_API_BASE}/Incidents.svc/json/ElevatorIncidents"
    data = await make_wmata_request(url)

    if not data or "ElevatorIncidents" not in data:
        return "❌ Unable to get elevator status information."

    outages = data["ElevatorIncidents"]
    
    if not outages:
        return "✅ All elevators and escalators are currently operational."

    accessibility_alerts = []
    for outage in outages:
        station_code = outage.get("StationCode", "")
        station_name = next((name for name, code in STATION_MAPPING.items() if code == station_code), 
                           outage.get("StationName", "Unknown Station"))
        unit_type = outage.get("UnitType", "Equipment")
        description = outage.get("SymptomDescription", "No details available")
        
        alert = f"♿ **{station_name}** - {unit_type} Issue\n{description}\n"
        accessibility_alerts.append(alert)

    return "🛗 **Elevator & Escalator Outages:**\n\n" + "\n".join(accessibility_alerts)

@mcp.tool()
async def get_station_info(station: str) -> str:
    """
    Get detailed information about a Metro station including amenities and features.
    
    Args:
        station: Station name or code
    
    Returns:
        Detailed station information including location, lines, and amenities
    """
    station_code = get_station_code(station)
    
    if not station_code:
        return f"❌ Station '{station}' not found."

    url = f"{WMATA_API_BASE}/Rail.svc/json/jStationInfo"
    params = {"StationCode": station_code}
    
    data = await make_wmata_request(url, params)

    if not data:
        return "❌ Unable to get station information."

    station_name = data.get("Name", "Unknown Station")
    address = data.get("Address", {})
    
    info = f"🚉 **{station_name}** Station Information\n\n"
    
    # Address information
    if address:
        street = address.get("Street", "")
        city = address.get("City", "")
        state = address.get("State", "")
        zip_code = address.get("Zip", "")
        
        if street:
            info += f"📍 **Address:** {street}"
            if city:
                info += f", {city}"
            if state:
                info += f", {state}"
            if zip_code:
                info += f" {zip_code}"
            info += "\n"

    # Lines served
    lines_served = STATION_LINES.get(station_code, [])
    if lines_served:
        line_names = [LINE_COLORS[line] for line in lines_served]
        info += f"🚇 **Lines:** {', '.join(line_names)}\n"

    # Station features
    info += f"\n🏢 **Station Features:**\n"
    info += f"• Fully accessible (all Metro stations are ADA compliant)\n"
    info += f"• SmarTrip and contactless payment accepted\n"
    info += f"• Free WiFi available\n"
    
    # Parking information
    if "Parking" in data and data["Parking"]:
        parking = data["Parking"]
        if parking.get("TotalCount", 0) > 0:
            info += f"🅿️ **Parking:** {parking.get('TotalCount', 'Available')} spaces\n"

    info += f"\n💡 **Getting Here:**\n"
    info += f"• Check train predictions before traveling\n"
    info += f"• Plan for potential delays during rush hours\n"
    info += f"• Consider checking service alerts before your trip"

    return info

@mcp.tool()
async def get_all_stations() -> str:
    """
    Get a list of all Metro stations organized by line.
    
    Returns:
        Complete list of Metro stations by line
    """
    url = f"{WMATA_API_BASE}/Rail.svc/json/jStations"
    data = await make_wmata_request(url)

    if not data or "Stations" not in data:
        return "❌ Unable to get station list."

    stations = data["Stations"]
    
    # Organize stations by line
    lines = {}
    for station in stations:
        station_code = station.get("Code", "")
        station_name = station.get("Name", "Unknown")
        line_code1 = station.get("LineCode1", "")
        line_code2 = station.get("LineCode2", "")
        line_code3 = station.get("LineCode3", "")
        line_code4 = station.get("LineCode4", "")
        
        for line_code in [line_code1, line_code2, line_code3, line_code4]:
            if line_code and line_code in LINE_COLORS:
                if line_code not in lines:
                    lines[line_code] = []
                lines[line_code].append(f"{station_name} ({station_code})")

    result = "🚇 **Metro Station Directory**\n\n"
    
    for line_code in ["RD", "OR", "SV", "BL", "YL", "GR"]:
        if line_code in lines:
            line_name = LINE_COLORS[line_code]
            stations_list = sorted(set(lines[line_code]))
            result += f"**{line_name}:**\n"
            for station in stations_list:
                result += f"• {station}\n"
            result += "\n"

    result += "💡 **Usage Tips:**\n"
    result += "• Use station codes (like 'B03') or full names\n"
    result += "• Major transfer stations connect multiple lines\n"
    result += "• All stations are fully accessible"

    return result

# === RESOURCES ===

@mcp.resource("wmata://system/map")
def get_metro_map() -> str:
    """Provides information about the Metro system map and line structure"""
    return """
📍 Washington Metro System Map Overview

The Washington Metro consists of 6 colored lines serving 98 stations:

🔴 RED LINE (Glenmont ↔ Shady Grove)
- Serves: Downtown, Dupont Circle, Bethesda, Silver Spring
- Key stations: Union Station, Metro Center, Dupont Circle

🔵 BLUE LINE (Downtown Largo ↔ Franconia-Springfield)  
- Serves: Downtown, Arlington, Alexandria
- Key stations: Pentagon, Smithsonian, Capitol South

🟡 YELLOW LINE (Huntington ↔ Fort Totten)
- Serves: Downtown, National Airport, Pentagon
- Key stations: Gallery Place, L'Enfant Plaza, Pentagon

🟠 ORANGE LINE (New Carrollton ↔ Vienna)
- Serves: Downtown, Arlington, Fairfax County  
- Key stations: Federal Triangle, Rosslyn, Ballston

🟢 GREEN LINE (Branch Ave ↔ Greenbelt)
- Serves: Downtown, Anacostia, Prince George's County
- Key stations: Gallery Place, Navy Yard, Fort Totten

🩶 SILVER LINE (Downtown Largo ↔ Ashburn)
- Serves: Downtown, Tysons, Dulles Airport, Loudoun County
- Key stations: Metro Center, Rosslyn, Wiehle-Reston East

Major Transfer Stations:
• Metro Center (Red/Blue/Orange/Silver)
• Gallery Place-Chinatown (Red/Green/Yellow)  
• L'Enfant Plaza (Blue/Orange/Silver/Green/Yellow)
• Fort Totten (Red/Green/Yellow)
• Rosslyn (Blue/Orange/Silver)

Operating Hours: 5:00 AM - 12:00 AM (Mon-Thu), 5:00 AM - 1:00 AM (Fri), 7:00 AM - 1:00 AM (Sat), 8:00 AM - 12:00 AM (Sun)
"""

@mcp.resource("wmata://fares/structure")  
def get_fare_information() -> str:
    """Provides current Metro fare structure and payment options"""
    return """
💳 Metro Fare Information

BASE FARES (2024):
• Peak Hours: $2.45 - $6.75 (Mon-Fri 5:00-9:30 AM, 3:00-7:00 PM)
• Off-Peak: $2.25 - $6.00 (All other times)
• Weekend: $2.25 - $6.00

PAYMENT OPTIONS:
🎫 SmarTrip Card/App: Standard payment method
📱 Mobile Pay: Apple Pay, Google Pay, Samsung Pay  
💳 Contactless: Tap credit/debit cards directly

PASSES & DISCOUNTS:
• 7-Day Fast Pass: $66 (unlimited rail travel)
• 1-Day Pass: $15 (unlimited rail travel)
• Reduced Fare: 50% off for seniors (65+), disabled, Medicare cardholders
• Kids Under 5: Free with paying customer

TIPS:
• Fares calculated by distance traveled
• Same-day transfers between rail/bus: $0.50 discount
• Add value online, at stations, or participating retailers
• $2 fee for new SmarTrip cards at stations (free online)
• Mobile apps offer trip planning and real-time info
"""

# === PROMPTS ===

@mcp.prompt()
def plan_trip(origin: str, destination: str, departure_time: str = "now") -> str:
    """
    Plan a complete Metro trip with step-by-step directions.
    
    Args:
        origin: Starting location or station
        destination: Where you want to go  
        departure_time: When you want to leave (default: "now")
    """
    return f"""I need to plan a Metro trip from {origin} to {destination}, departing {departure_time}. 

Please help me by:
1. Finding the best route between these stations
2. Checking current service alerts that might affect my trip
3. Getting live train predictions for my starting station
4. Providing any accessibility information if needed
5. Suggesting the best exit/entrance to use at my destination

Also let me know about:
- Estimated travel time
- Any transfers required
- Current system status
- Tips for a smooth journey"""

@mcp.prompt()  
def check_accessibility(station: str) -> str:
    """
    Check accessibility status and features for a Metro station.
    
    Args:
        station: Station name to check accessibility for
    """
    return f"""I need accessibility information for {station} station. Please provide:

1. Current elevator and escalator status
2. Accessible entrance locations  
3. Platform accessibility features
4. Any current outages affecting accessibility
5. Alternative accessible routes if there are outages

This information is important for planning accessible Metro travel."""

@mcp.prompt()
def tourist_guide(destination: str) -> str:
    """
    Provide tourist-friendly Metro guidance to popular DC destinations.
    
    Args:
        destination: Tourist destination or attraction name
    """
    return f"""I'm visiting Washington DC and want to get to {destination} using Metro. As a tourist, I need:

1. Which Metro station is closest to {destination}
2. How to get there from a central location (like Union Station or Metro Center)
3. What exit to use at the destination station
4. Approximate walking time from the station
5. Any tourist tips for using Metro
6. Information about SmarTrip cards and payment options
7. Current service status and any alerts

Please provide beginner-friendly directions and Metro etiquette tips."""

@mcp.prompt()
def service_disruption_help() -> str:
    """Get help during Metro service disruptions and find alternatives."""
    return """There seems to be a service disruption affecting my Metro travel. Please help by:

1. Checking all current service alerts and incidents  
2. Identifying which lines and stations are affected
3. Suggesting alternative routes if possible
4. Providing information about shuttle bus services
5. Giving realistic time estimates for delays
6. Checking elevator/escalator status for accessibility needs

I need to understand my options and plan accordingly for the disruption."""

@mcp.prompt()
def rush_hour_strategy(origin: str, destination: str, time_of_day: str) -> str:
    """
    Get optimal travel strategy for rush hour Metro travel.
    
    Args:
        origin: Starting station
        destination: Ending station  
        time_of_day: Morning rush, evening rush, or specific time
    """
    return f"""I need to travel from {origin} to {destination} during {time_of_day}. Please help optimize my trip by:

1. Finding the best route with minimal transfers
2. Checking current train predictions and frequencies
3. Identifying less crowded cars or boarding spots
4. Suggesting optimal departure time to avoid peak crowding  
5. Providing backup routes in case of delays
6. Checking for any planned service work affecting my route

I want to minimize travel time and avoid the worst crowds during rush hour."""

if __name__ == "__main__":
    mcp.run(transport='stdio')