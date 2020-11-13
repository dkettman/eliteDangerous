from dataclasses import dataclass
from enum import IntFlag


class StatusFlag(IntFlag):
    Docked = 0x00000001,
    Landed = 0x00000002,
    LandingGearDown = 0x00000004,
    ShieldsUp = 0x00000008,
    Supercruise = 0x00000010,
    FlightAssistOff = 0x00000020,
    HardpointsDeployed = 0x00000040,
    InWing = 0x00000080,
    LightsOn = 0x00000100,
    CargoScoopDeployed = 0x00000200,
    SilentRunning = 0x00000400,
    ScoopingFuel = 0x00000800,
    SRV_HandBrake = 0x00001000,
    SRV_TurretView = 0x00002000,
    SRV_TurretRetracted = 0x00004000,
    SRV_DriveAssist = 0x00008000,
    FSD_MassLocked = 0x00010000,
    FSD_Charging = 0x00020000,
    FSD_Cooldown = 0x00040000,
    LowFuel = 0x00080000,
    OverHeating = 0x00100000,
    HasLatLong = 0x00200000,
    IsInDanger = 0x00400000,
    BeingInterdicted = 0x00800000,
    InMothership = 0x01000000,
    InFighter = 0x02000000,
    InSRV = 0x04000000,
    HUD_AnalysisMode = 0x08000000,
    NightVision = 0x10000000,
    AltitudeFromAvgRadius = 0x20000000,
    FSD_Jump = 0x40000000,
    SRV_HighBeam = 0x80000000,

class GuiFocus(IntFlag):
    NoFocus = 0,
    InternalPanel = 1,
    ExternalPanel = 2,
    CommsPanel = 3,
    RolePanel = 4,
    StationServices = 5,
    GalaxyMap = 6,
    SystemMap = 7,
    Orrery = 8,
    FSSMode = 9,
    SAAMode = 10,
    Codex = 11,

class SystemPips:
    power_pips = {
        0: "....",
        1: "o...",
        2: "0...",
        3: "0o..",
        4: "00..",
        5: "00o.",
        6: "000.",
        7: "000o",
        8: "0000",
    }

@dataclass
class InventoryItem:
    name: str
    count: int
    stolen: bool
    name_localized: str = ""

