# import random
# from typing import Dict, Any
# from google.adk.agents import Agent

# # ---------------- Base class with logging ---------------- #
# class BaseADKAgent(Agent):
#     def log(self, message: str):
#         print(f"[{self.name}] {message}")  # Simple console logger

#     def send_message(self, target_agent: "BaseADKAgent", action: str, payload: dict):
#         self.log(f"Sending '{action}' to {target_agent.name} | Payload: {payload}")
#         result = target_agent.receive_message(action, payload)
#         self.log(f"Received from {target_agent.name}: {result}")
#         return result

#     def receive_message(self, action: str, payload: dict) -> Dict[str, Any]:
#         self.log(f"Received action '{action}' with payload {payload}")
#         return {"status": "ok"}


# # ---------------- Sub-Agents ---------------- #
# class CommunicationAlertAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="CommunicationAlertAgent",
#             model="gemini-2.5-flash",
#             instruction="Handle disaster alerts and broadcast safety instructions."
#         )

#     def send_alerts(self, location: str, disaster_type: str) -> Dict[str, Any]:
#         recipients = random.randint(5_000, 200_000)
#         sos = random.randint(0, 50)
#         self.log(f"Alert for {disaster_type} at {location}. Alerts sent: {recipients}, SOS: {sos}")
#         return {"agent": self.name, "alerts_sent": recipients, "sos_detected": sos}


# class PoliceAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="PoliceAgent",
#             model="gemini-2.5-flash",
#             instruction="Secure the disaster area and dispatch police resources."
#         )

#     def execute(self, location: str) -> Dict[str, Any]:
#         station = random.choice(["Central Precinct", "North Station", "Harbor Precinct"]) + f" near {location}"
#         cars = random.randint(2, 15)
#         self.log(f"Dispatching {cars} cars from {station} to secure {location}")
#         return {"agent": self.name, "station": station, "cars_dispatched": cars}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class HospitalEMSAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="HospitalEMSAgent",
#             model="gemini-2.5-flash",
#             instruction="Provide hospital and EMS support for disasters."
#         )

#     def execute(self, location: str) -> Dict[str, Any]:
#         hospital = random.choice(["City General", "Riverside Medical", "St. Anne's"]) + f" near {location}"
#         icu = random.randint(0, 30)
#         ambulances = random.randint(1, 8)
#         self.log(f"{hospital} ready. ICU beds: {icu}, {ambulances} ambulances prepared")
#         return {"agent": self.name, "hospital": hospital, "ambulances": ambulances, "icu_beds": icu}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class RescueAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="RescueAgent",
#             model="gemini-2.5-flash",
#             instruction="Deploy rescue vehicles and units during disaster."
#         )

#     def execute(self, location: str, disaster_type: str) -> Dict[str, Any]:
#         station = random.choice(["Rescue Station 12", "Firehouse 7"]) + f" near {location}"
#         units = random.randint(1, 6)
#         asset = "boats" if disaster_type == "flood" else "trucks/drones"
#         self.log(f"{station} sending {units} {asset} to {location}")
#         return {"agent": self.name, "station": station, "vehicles": units, "asset": asset}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"], payload.get("disaster_type", "unknown"))
#         return super().receive_message(action, payload)


# class UtilityInfrastructureAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="UtilityAgent",
#             model="gemini-2.5-flash",
#             instruction="Secure critical infrastructure during disaster."
#         )

#     def execute(self, location: str) -> Dict[str, Any]:
#         grid = random.choice(["Grid-Blue", "Grid-Delta"]) + f" near {location}"
#         self.log(f"Shutting down power grid {grid} near {location}")
#         return {"agent": self.name, "grid": grid, "crew_dispatched": True}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class TransportationEvacAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="TransportAgent",
#             model="gemini-2.5-flash",
#             instruction="Deploy evacuation transportation."
#         )

#     def execute(self, location: str) -> Dict[str, Any]:
#         buses = random.randint(5, 40)
#         routes = random.randint(1, 8)
#         self.log(f"{buses} buses deployed over {routes} routes near {location}")
#         return {"agent": self.name, "buses": buses, "routes_secured": routes}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class ReliefShelterAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="ReliefAgent",
#             model="gemini-2.5-flash",
#             instruction="Setup relief shelters and distribute supplies."
#         )

#     def execute(self, location: str) -> Dict[str, Any]:
#         center = random.choice(["Community Center West", "High School Gym"]) + f" near {location}"
#         supplies = random.randint(200, 5000)
#         self.log(f"Shelter {center} setup with {supplies} supplies")
#         return {"agent": self.name, "center": center, "supplies": supplies}


# # ---------------- Builder ---------------- #
# def build_default_agents() -> Dict[str, BaseADKAgent]:
#     return {
#         "communication": CommunicationAlertAgent(),
#         "police": PoliceAgent(),
#         "hospital": HospitalEMSAgent(),
#         "rescue": RescueAgent(),
#         "utility": UtilityInfrastructureAgent(),
#         "transport": TransportationEvacAgent(),
#         "relief": ReliefShelterAgent()
#     }


import random
from typing import Dict, Any
from google.adk.agents import Agent

# ---------------- Base class with internal logging ---------------- #
class BaseADKAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._internal_logs = []

    def log(self, message: str):
        full_message = f"[{self.name}] {message}"
        self._internal_logs.append(full_message)
        print(full_message)  # still print in console

    def get_logs(self):
        return self._internal_logs

    def send_message(self, target_agent: "BaseADKAgent", action: str, payload: dict):
        self.log(f"Sending '{action}' to {target_agent.name} | Payload: {payload}")
        result = target_agent.receive_message(action, payload)
        self.log(f"Received from {target_agent.name}: {result}")
        return result

    def receive_message(self, action: str, payload: dict) -> Dict[str, Any]:
        self.log(f"Received action '{action}' with payload {payload}")
        return {"status": "ok"}


# ---------------- Sub-Agents ---------------- #
class CommunicationAlertAgent(BaseADKAgent):
    def __init__(self):
        super().__init__(
            name="CommunicationAlertAgent",
            model="gemini-2.5-flash",
            instruction="Handle disaster alerts and broadcast safety instructions."
        )

    def send_alerts(self, location: str, disaster_type: str) -> Dict[str, Any]:
        recipients = random.randint(5_000, 200_000)
        sos = random.randint(0, 50)
        self.log(f"Alert for {disaster_type} at {location}. Alerts sent: {recipients}, SOS: {sos}")
        return {"agent": self.name, "alerts_sent": recipients, "sos_detected": sos}


class PoliceAgent(BaseADKAgent):
    cars_dispatched: int = 0
    station: str = ""
    
    def __init__(self):
        super().__init__(
            name="PoliceAgent",
            model="gemini-2.5-flash",
            instruction="Secure the disaster area and dispatch police resources."
        )

    def execute(self, location: str) -> Dict[str, Any]:
        self.station = random.choice(["Central Precinct", "North Station", "Harbor Precinct"]) + f" near {location}"
        self.cars_dispatched = random.randint(2, 15)
        self.log(f"Dispatching {self.cars_dispatched} cars from {self.station} to secure {location}")
        return {"agent": self.name, "station": self.station, "cars_dispatched": self.cars_dispatched}

    def receive_message(self, action: str, payload: dict):
        if action.startswith("alert_"):
            return self.execute(payload["location"])
        
        # SCENARIO 1: Hospital requests crowd control
        elif action == "hospital_crowd_control":
            hospital_loc = payload.get("location", "unknown")
            icu_capacity = payload.get("icu_capacity", 0)
            estimated_patients = payload.get("estimated_patients", 0)
            
            self.log(f"🚨 URGENT: Hospital crowd control requested at {hospital_loc}")
            self.log(f"   Reason: ICU overwhelmed ({icu_capacity} beds, {estimated_patients} patients expected)")
            
            # Deploy additional units
            additional_units = random.randint(3, 6)
            self.cars_dispatched += additional_units
            self.log(f"🚔 Dispatching {additional_units} additional units for crowd control")
            self.log(f"   Mission: Traffic management, crowd control, patient family support")
            
            return {
                "status": "deployed",
                "additional_cars": additional_units,
                "total_cars": self.cars_dispatched,
                "eta": "5 minutes",
                "mission": "Hospital crowd control and traffic management"
            }
        
        # SCENARIO 2: Transport requests route clearance
        elif action == "clear_evacuation_route":
            route = payload.get("route", "unknown")
            priority = payload.get("priority", "normal")
            
            self.log(f"🚦 Route clearance requested: {route} (Priority: {priority})")
            
            # Clear the route
            units_for_route = random.randint(2, 4)
            self.log(f"🚔 Deploying {units_for_route} units to clear and secure {route}")
            
            return {
                "status": "route_cleared",
                "route": route,
                "units_deployed": units_for_route,
                "estimated_clearance_time": "3 minutes",
                "traffic_diverted": True
            }
        
        return super().receive_message(action, payload)


class HospitalEMSAgent(BaseADKAgent):
    icu_beds: int = 0
    ambulances: int = 0
    hospital_name: str = ""
    
    def __init__(self):
        super().__init__(
            name="HospitalEMSAgent",
            model="gemini-2.5-flash",
            instruction="Provide hospital and EMS support for disasters."
        )

    def execute(self, location: str, police_agent=None, relief_agent=None, force_critical_icu: bool = False) -> Dict[str, Any]:
        self.hospital_name = random.choice(["City General", "Riverside Medical", "St. Anne's"]) + f" near {location}"
        
        # Force critical ICU situation for Scenario 1
        if force_critical_icu:
            self.icu_beds = random.randint(2, 5)  # Force critical shortage
        else:
            self.icu_beds = random.randint(0, 30)
        
        self.ambulances = random.randint(1, 8)
        
        # SCENARIO 1: If ICU beds are critically low, request police crowd control
        if self.icu_beds < 10 and police_agent:
            self.log(f"⚠️ CRITICAL: Only {self.icu_beds} ICU beds available! Requesting police support...")
            police_response = self.send_message(
                police_agent, 
                "hospital_crowd_control",
                {
                    "location": self.hospital_name,
                    "reason": "ICU overwhelmed",
                    "icu_capacity": self.icu_beds,
                    "estimated_patients": random.randint(20, 50)
                }
            )
            self.log(f"✅ Police responded: {police_response.get('status', 'deployed')}")
        
        # SCENARIO 3: Send ambulance to relief shelter if needed
        if relief_agent and self.ambulances > 3:
            self.log(f"🏥 Sending 1 ambulance to relief shelter for triage...")
            relief_response = self.send_message(
                relief_agent,
                "medical_support",
                {
                    "ambulances": 1,
                    "medics": 3,
                    "supplies": "First aid kits, oxygen"
                }
            )
            self.log(f"✅ Relief shelter acknowledged: {relief_response.get('status', 'received')}")
        
        self.log(f"{self.hospital_name} ready. ICU beds: {self.icu_beds}, ambulances: {self.ambulances} prepared")
        return {
            "agent": self.name, 
            "hospital": self.hospital_name, 
            "ambulances": self.ambulances, 
            "icu_beds": self.icu_beds
        }

    def receive_message(self, action: str, payload: dict):
        if action.startswith("alert_"):
            return self.execute(
                payload["location"],
                payload.get("police_agent"),
                payload.get("relief_agent"),
                payload.get("force_critical_icu", False)
            )
        elif action == "request_medical_support":
            self.log(f"📨 Received medical support request from {payload.get('from_agent', 'unknown')}")
            if self.ambulances > 0:
                return {"status": "ambulance_dispatched", "ambulances": 1, "eta": "10 minutes"}
            else:
                return {"status": "no_ambulances_available", "alternative": "Sending first responders"}
        return super().receive_message(action, payload)


class RescueAgent(BaseADKAgent):
    vehicles: int = 0
    asset_type: str = ""
    
    def __init__(self):
        super().__init__(
            name="RescueAgent",
            model="gemini-2.5-flash",
            instruction="Deploy rescue vehicles and units during disaster."
        )

    def execute(self, location: str, disaster_type: str, transport_agent=None, police_agent=None) -> Dict[str, Any]:
        station = random.choice(["Rescue Station 12", "Firehouse 7"]) + f" near {location}"
        self.vehicles = random.randint(1, 6)
        self.asset_type = "boats" if disaster_type == "flood" else "trucks/drones"
        
        # SCENARIO 2: Coordinate with Transport for evacuation points
        if transport_agent:
            self.log(f"📡 Coordinating with Transport for evacuation pickup locations...")
            transport_response = self.send_message(
                transport_agent,
                "request_pickup_locations",
                {
                    "rescue_units": self.vehicles,
                    "asset_type": self.asset_type,
                    "from_agent": "RescueAgent"
                }
            )
            
            pickup_points = transport_response.get("pickup_points", ["Main Square", "Community Center"])
            self.log(f"✅ Transport confirmed pickup points: {', '.join(pickup_points)}")
            
            # SCENARIO 2: Request police to clear routes to pickup points
            if police_agent:
                self.log(f"🚦 Requesting police to clear routes to evacuation points...")
                for point in pickup_points[:2]:  # Clear routes to first 2 points
                    police_response = self.send_message(
                        police_agent,
                        "clear_evacuation_route",
                        {
                            "route": f"Route to {point}",
                            "priority": "high",
                            "from_agent": "RescueAgent"
                        }
                    )
                    if police_response.get("status") == "route_cleared":
                        self.log(f"✅ Police cleared route to {point}")
        
        self.log(f"{station} sending {self.vehicles} {self.asset_type} to {location}")
        return {
            "agent": self.name, 
            "station": station, 
            "vehicles": self.vehicles, 
            "asset": self.asset_type
        }

    def receive_message(self, action: str, payload: dict):
        if action.startswith("alert_"):
            return self.execute(
                payload["location"], 
                payload.get("disaster_type", "unknown"),
                payload.get("transport_agent"),
                payload.get("police_agent")
            )
        return super().receive_message(action, payload)


class UtilityInfrastructureAgent(BaseADKAgent):
    def __init__(self):
        super().__init__(
            name="UtilityAgent",
            model="gemini-2.5-flash",
            instruction="Secure critical infrastructure during disaster."
        )

    def execute(self, location: str) -> Dict[str, Any]:
        grid = random.choice(["Grid-Blue", "Grid-Delta"]) + f" near {location}"
        self.log(f"Shutting down power grid {grid} near {location}")
        return {"agent": self.name, "grid": grid, "crew_dispatched": True}

    def receive_message(self, action: str, payload: dict):
        if action.startswith("alert_"):
            return self.execute(payload["location"])
        return super().receive_message(action, payload)


class TransportationEvacAgent(BaseADKAgent):
    buses: int = 0
    routes: int = 0
    pickup_locations: list = []
    
    def __init__(self):
        super().__init__(
            name="TransportAgent",
            model="gemini-2.5-flash",
            instruction="Deploy evacuation transportation."
        )

    def execute(self, location: str) -> Dict[str, Any]:
        self.buses = random.randint(5, 40)
        self.routes = random.randint(1, 8)
        
        # Define pickup locations for coordination
        self.pickup_locations = [
            "Main Square",
            "Community Center",
            "Shopping District",
            "Riverside Park"
        ][:self.routes]
        
        self.log(f"{self.buses} buses deployed over {self.routes} routes near {location}")
        self.log(f"   Pickup points: {', '.join(self.pickup_locations)}")
        return {
            "agent": self.name, 
            "buses": self.buses, 
            "routes_secured": self.routes,
            "pickup_points": self.pickup_locations
        }

    def receive_message(self, action: str, payload: dict):
        if action.startswith("alert_"):
            return self.execute(payload["location"])
        
        # SCENARIO 2: Rescue requests pickup locations
        elif action == "request_pickup_locations":
            from_agent = payload.get("from_agent", "unknown")
            rescue_units = payload.get("rescue_units", 0)
            
            self.log(f"📨 Pickup location request from {from_agent} ({rescue_units} rescue units)")
            self.log(f"   Coordinating {len(self.pickup_locations)} evacuation points")
            
            return {
                "status": "confirmed",
                "pickup_points": self.pickup_locations,
                "buses_per_point": self.buses // max(len(self.pickup_locations), 1),
                "coordination": f"Buses ready at {len(self.pickup_locations)} locations"
            }
        
        return super().receive_message(action, payload)


class ReliefShelterAgent(BaseADKAgent):
    supplies: int = 0
    center_name: str = ""
    capacity: int = 0
    
    def __init__(self):
        super().__init__(
            name="ReliefAgent",
            model="gemini-2.5-flash",
            instruction="Setup relief shelters and distribute supplies."
        )

    def execute(self, location: str, sos_count: int = 0, hospital_agent=None) -> Dict[str, Any]:
        self.center_name = random.choice(["Community Center West", "High School Gym"]) + f" near {location}"
        self.supplies = random.randint(200, 5000)
        self.capacity = random.randint(100, 500)
        
        # SCENARIO 3: If high SOS count, request medical support at shelter
        if sos_count > 20 and hospital_agent:
            self.log(f"⚠️ HIGH SOS COUNT: {sos_count} distress signals detected!")
            self.log(f"   Requesting medical support at shelter {self.center_name}")
            
            hospital_response = self.send_message(
                hospital_agent,
                "request_medical_support",
                {
                    "location": self.center_name,
                    "sos_count": sos_count,
                    "estimated_injured": sos_count // 2,
                    "from_agent": "ReliefAgent"
                }
            )
            
            if hospital_response.get("status") == "ambulance_dispatched":
                self.log(f"✅ Hospital dispatching ambulance to shelter (ETA: {hospital_response.get('eta', 'unknown')})")
                # Expand capacity knowing medical support is coming
                self.capacity += 50
                self.log(f"   Expanding shelter capacity to {self.capacity} people")
            else:
                self.log(f"⚠️ No ambulance available, preparing for first aid only")
        
        self.log(f"Shelter {self.center_name} setup with {self.supplies} supplies (Capacity: {self.capacity})")
        return {
            "agent": self.name, 
            "center": self.center_name, 
            "supplies": self.supplies,
            "capacity": self.capacity
        }
    
    def receive_message(self, action: str, payload: dict):
        if action.startswith("alert_"):
            return self.execute(
                payload["location"],
                payload.get("sos_count", 0),
                payload.get("hospital_agent")
            )
        
        # SCENARIO 3: Hospital sends medical support
        elif action == "medical_support":
            ambulances = payload.get("ambulances", 0)
            medics = payload.get("medics", 0)
            supplies = payload.get("supplies", "")
            
            self.log(f"🏥 Medical support arrived: {ambulances} ambulance(s), {medics} medics")
            self.log(f"   Medical supplies: {supplies}")
            
            return {
                "status": "received",
                "triage_area_setup": True,
                "message": "Medical support integrated at shelter"
            }
        
        return super().receive_message(action, payload)


# ---------------- Builder ---------------- #
def build_default_agents() -> Dict[str, BaseADKAgent]:
    return {
        "communication": CommunicationAlertAgent(),
        "police": PoliceAgent(),
        "hospital": HospitalEMSAgent(),
        "rescue": RescueAgent(),
        "utility": UtilityInfrastructureAgent(),
        "transport": TransportationEvacAgent(),
        "relief": ReliefShelterAgent()
    }



# import random
# from typing import Dict, Any
# from google.adk.agents import Agent

# # ---------------- Base class with logging and messaging ---------------- #
# class BaseADKAgent(Agent):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self._internal_logs = []

#     def log(self, message: str):
#         full_message = f"[{self.name}] {message}"
#         self._internal_logs.append(full_message)
#         print(full_message, flush=True)

#     def get_logs(self):
#         return self._internal_logs

#     def send_message(self, target_agent: "BaseADKAgent", action: str, payload: dict):
#         self.log(f"Sending '{action}' to {target_agent.name} | Payload: {payload}")
#         result = target_agent.receive_message(action, payload)
#         self.log(f"Received response from {target_agent.name}: {result}")
#         return result

#     def receive_message(self, action: str, payload: dict) -> Dict[str, Any]:
#         self.log(f"Received action '{action}' with payload {payload}")
#         return {"status": "ok"}


# ---------------- Sub-Agents ---------------- #

# class CommunicationAlertAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(
#             name="CommunicationAlertAgent",
#             model="gemini-2.5-flash",
#             instruction="Handle disaster alerts and broadcast safety instructions."
#         )

#     def send_alerts(self, location: str, disaster_type: str) -> Dict[str, Any]:
#         recipients = random.randint(5_000, 200_000)
#         sos = random.randint(0, 50)
#         self.log(f"Alert for {disaster_type} at {location}. Alerts sent: {recipients}, SOS: {sos}")
#         return {"agent": self.name, "alerts_sent": recipients, "sos_detected": sos}


# class PoliceAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(name="PoliceAgent", model="gemini-2.5-flash",
#                          instruction="Secure the disaster area and dispatch police resources.")

#     def execute(self, location: str) -> Dict[str, Any]:
#         station = random.choice(["Central Precinct", "North Station", "Harbor Precinct"]) + f" near {location}"
#         cars = random.randint(2, 15)
#         self.log(f"Dispatching {cars} police cars from {station}")
#         return {"agent": self.name, "station": station, "cars_dispatched": cars}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class HospitalEMSAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(name="HospitalEMSAgent", model="gemini-2.5-flash",
#                          instruction="Provide hospital and EMS support for disasters.")

#     def execute(self, location: str) -> Dict[str, Any]:
#         hospital = random.choice(["City General", "Riverside Medical", "St. Anne's"]) + f" near {location}"
#         icu = random.randint(0, 30)
#         ambulances = random.randint(1, 8)
#         self.log(f"{hospital} ready. ICU beds: {icu}, ambulances: {ambulances} prepared")
#         return {"agent": self.name, "hospital": hospital, "ambulances": ambulances, "icu_beds": icu}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             # Example inter-agent communication: alert Police if ICU is low
#             if payload.get("icu_needed", 0) > 10:
#                 self.log("ICU demand high, notifying PoliceAgent for crowd control.")
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class RescueAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(name="RescueAgent", model="gemini-2.5-flash",
#                          instruction="Deploy rescue vehicles and units during disaster.")

#     def execute(self, location: str, disaster_type: str) -> Dict[str, Any]:
#         station = random.choice(["Rescue Station 12", "Firehouse 7"]) + f" near {location}"
#         units = random.randint(1, 6)
#         asset = "boats" if disaster_type == "flood" else "trucks/drones"
#         self.log(f"{station} sending {units} {asset} to {location}")
#         return {"agent": self.name, "station": station, "vehicles": units, "asset": asset}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"], payload.get("disaster_type", "unknown"))
#         return super().receive_message(action, payload)


# class UtilityInfrastructureAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(name="UtilityAgent", model="gemini-2.5-flash",
#                          instruction="Secure critical infrastructure during disaster.")

#     def execute(self, location: str) -> Dict[str, Any]:
#         grid = random.choice(["Grid-Blue", "Grid-Delta"]) + f" near {location}"
#         self.log(f"Shutting down power grid {grid} near {location}")
#         return {"agent": self.name, "grid": grid, "crew_dispatched": True}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class TransportationEvacAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(name="TransportAgent", model="gemini-2.5-flash",
#                          instruction="Deploy evacuation transportation.")

#     def execute(self, location: str) -> Dict[str, Any]:
#         buses = random.randint(5, 40)
#         routes = random.randint(1, 8)
#         self.log(f"{buses} buses deployed over {routes} routes near {location}")
#         return {"agent": self.name, "buses": buses, "routes_secured": routes}

#     def receive_message(self, action: str, payload: dict):
#         if action.startswith("alert_"):
#             return self.execute(payload["location"])
#         return super().receive_message(action, payload)


# class ReliefShelterAgent(BaseADKAgent):
#     def __init__(self):
#         super().__init__(name="ReliefAgent", model="gemini-2.5-flash",
#                          instruction="Setup relief shelters and distribute supplies.")

#     def execute(self, location: str) -> Dict[str, Any]:
#         center = random.choice(["Community Center West", "High School Gym"]) + f" near {location}"
#         supplies = random.randint(200, 5000)
#         self.log(f"Shelter {center} setup with {supplies} supplies")
#         return {"agent": self.name, "center": center, "supplies": supplies}


# # ---------------- Builder ---------------- #
# def build_default_agents() -> Dict[str, BaseADKAgent]:
#     return {
#         "communication": CommunicationAlertAgent(),
#         "police": PoliceAgent(),
#         "hospital": HospitalEMSAgent(),
#         "rescue": RescueAgent(),
#         "utility": UtilityInfrastructureAgent(),
#         "transport": TransportationEvacAgent(),
#         "relief": ReliefShelterAgent()
#     }
