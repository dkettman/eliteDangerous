
station_events = [
    "DockingRequested",
    "DockingGranted",
    "DockingDenied",
]


def update_docking_status(data):
    if data["event"] == "DockingRequested":
        return "Docking Requested: {}".format(data["StationName"])
    elif data["event"] == "DockingGranted":
        return "Docking Granted: {} -- Pad: {}".format(data["StationName"], data["LandingPad"])
    elif data["event"] == "DockingDenied":
        return "Docking Denied: {} -- Reason: {}".format(data["StationName"], data["Reason"])
    else:
        return data["event"]
