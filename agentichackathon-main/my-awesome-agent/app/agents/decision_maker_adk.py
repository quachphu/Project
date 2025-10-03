

# from pydantic import PrivateAttr
# from typing import Dict
# from .agents_adk import BaseADKAgent, build_default_agents

# class DecisionMakerAgent(BaseADKAgent):
#     _agents: Dict[str, BaseADKAgent] = PrivateAttr()

#     def __init__(self, **kwargs):
#         super().__init__(
#             name="DecisionMakerAgent",
#             model="gemini-2.5-flash",
#             instruction=(
#                 "Parent disaster coordinator. Receives disaster scenario + location, "
#                 "delegates tasks to sub-agents dynamically, aggregates results."
#             ),
#             **kwargs
#         )
#         self._agents = build_default_agents()          # private sub-agents
#         self.tools = list(self._agents.values())      # expose to ADK Playground

#     def simulate(self, disaster_type: str, location: str):
#         self.log(f"=== SIM START: {disaster_type.upper()} at {location} ===")
#         results = []

#         # Send alert first
#         alert_result = self._agents["communication"].send_alerts(location, disaster_type)
#         results.append(alert_result)

#         # Notify all other agents
#         for name, agent in self._agents.items():
#             if name != "communication":
#                 result = agent.receive_message(
#                     action=f"alert_{disaster_type.lower()}",
#                     payload={"location": location, "disaster_type": disaster_type}
#                 )
#                 results.append(result)

#         self.log("=== SIM END: Aggregating Results ===")
#         return {"disaster_type": disaster_type, "location": location, "results": results}


from pydantic import PrivateAttr
from typing import Dict
from app.agents.agents_adk import BaseADKAgent, build_default_agents

class DecisionMakerAgent(BaseADKAgent):
    _agents: Dict[str, BaseADKAgent] = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(
            name="DecisionMakerAgent",
            model="gemini-2.5-flash",
            instruction=(
                "Parent disaster coordinator. Receives disaster scenario + location, "
                "delegates tasks to sub-agents dynamically, aggregates results."
            ),
            **kwargs
        )
        self._agents = build_default_agents()
        self.tools = list(self._agents.values())

    def simulate(self, disaster_type: str, location: str, scenario: int = 1):
        self.log(f"=== SIM START: {disaster_type.upper()} at {location} (SCENARIO {scenario}) ===")
        results = []
        simulation_logs = []

        # Step 1: Send alert - Communication goes first
        alert_result = self._agents["communication"].send_alerts(location, disaster_type)
        results.append(alert_result)
        simulation_logs.extend(self._agents["communication"].get_logs())
        
        # Extract SOS count - VARY based on scenario
        if scenario == 1:
            # Scenario 1: Hospital overwhelmed situation
            sos_count = 15  # Moderate SOS, focus on hospital crisis
        else:
            # Scenario 2: Mass evacuation situation  
            sos_count = 45  # High SOS, triggers relief → hospital coordination

        # Step 2: Notify other agents WITH INTER-AGENT REFERENCES
        for name, agent in self._agents.items():
            if name != "communication":
                # Build payload with references to other agents for cross-communication
                payload = {
                    "location": location, 
                    "disaster_type": disaster_type
                }
                
                # ENABLE INTER-AGENT COMMUNICATION - SCENARIO SPECIFIC
                if scenario == 1:
                    # SCENARIO 1: Hospital Overwhelmed → Police → Transport Chain
                    if name == "hospital":
                        payload["police_agent"] = self._agents.get("police")
                        payload["relief_agent"] = self._agents.get("relief")
                        payload["force_critical_icu"] = True  # Force hospital crisis
                    elif name == "police":
                        payload["transport_agent"] = self._agents.get("transport")  # Enable police → transport coordination
                    elif name == "relief":
                        payload["hospital_agent"] = self._agents.get("hospital")
                        payload["sos_count"] = sos_count
                    elif name == "rescue":
                        # Minimal coordination in scenario 1
                        pass
                
                else:
                    # SCENARIO 2: Mass Evacuation → Rescue → Transport → Police Chain
                    if name == "rescue":
                        payload["transport_agent"] = self._agents.get("transport")
                        payload["police_agent"] = self._agents.get("police")
                        payload["force_evacuation"] = True  # Force major evacuation
                    elif name == "transport":
                        payload["police_agent"] = self._agents.get("police")  # Enable transport → police coordination
                    elif name == "relief":
                        payload["hospital_agent"] = self._agents.get("hospital")
                        payload["sos_count"] = sos_count  # High SOS in scenario 2
                    elif name == "hospital":
                        payload["police_agent"] = self._agents.get("police")
                        payload["relief_agent"] = self._agents.get("relief")
                
                result = agent.receive_message(
                    action=f"alert_{disaster_type.lower()}",
                    payload=payload
                )
                # Include inter-agent communication logs in the result
                result["internal_logs"] = agent.get_logs().copy()
                results.append(result)
                simulation_logs.extend(agent.get_logs())

        self.log("=== SIM END: Aggregating Results ===")
        simulation_logs.append(f"[DecisionMakerAgent] Simulation complete for {disaster_type} at {location}")

        return {
            "disaster_type": disaster_type,
            "location": location,
            "results": results,
            "logs": simulation_logs
        }


# from pydantic import PrivateAttr
# from .agents_adk import BaseADKAgent, build_default_agents

# class DecisionMakerAgent(BaseADKAgent):
#     _agents: dict = PrivateAttr()

#     def __init__(self, **kwargs):
#         super().__init__(
#             name="DecisionMakerAgent",
#             model="gemini-2.5-flash",
#             instruction="Parent disaster coordinator. Receives disaster scenario + location, delegates tasks to sub-agents dynamically, aggregates results.",
#             **kwargs
#         )
#         self._agents = build_default_agents()
#         self.tools = list(self._agents.values())

#     def simulate(self, disaster_type: str, location: str):
#         # Clear logs
#         for agent in self._agents.values():
#             agent._internal_logs.clear()

#         self.log(f"=== SIMULATION START: {disaster_type.upper()} at {location} ===\n")
#         results = []

#         # Step 1: Communication Alert
#         alert_result = self._agents["communication"].send_alerts(location, disaster_type)
#         results.append(alert_result)

#         # Print logs immediately
#         for log in self._agents["communication"].get_logs():
#             print(log, flush=True)

#         # Step 2: Notify other agents and simulate inter-agent communication
#         for name, agent in self._agents.items():
#             if name == "communication":
#                 continue
#             if name == "rescue":
#                 result = self.send_message(agent, f"alert_{disaster_type.lower()}", {"location": location, "disaster_type": disaster_type})
#             else:
#                 result = self.send_message(agent, f"alert_{disaster_type.lower()}", {"location": location})

#             results.append(result)

#             # Example: hospital notifies police if ICU demand high
#             if name == "hospital":
#                 icu_demand = 12  # arbitrary example
#                 if icu_demand > 10:
#                     self.send_message(self._agents["police"], "alert_high_icu", {"location": location})

#             # Print logs
#             for log in agent.get_logs():
#                 print(log, flush=True)

#         self.log("\n=== SIMULATION END ===")

#         # Step 3: Human-readable summary
#         summary_lines = []
#         for res in results:
#             if res["agent"] == "CommunicationAlertAgent":
#                 summary_lines.append(f"Communication Alert Agent: Sent {res['alerts_sent']} alerts and detected {res['sos_detected']} SOS signals.")
#             elif res["agent"] == "PoliceAgent":
#                 summary_lines.append(f"Police Agent: Dispatched {res['cars_dispatched']} cars from {res['station']}.")
#             elif res["agent"] == "HospitalEMSAgent":
#                 summary_lines.append(f"Hospital EMS Agent: {res['hospital']} ready with {res['icu_beds']} ICU beds and {res['ambulances']} ambulances.")
#             elif res["agent"] == "RescueAgent":
#                 summary_lines.append(f"Rescue Agent: {res['station']} sent {res['vehicles']} {res['asset']}.")
#             elif res["agent"] == "UtilityAgent":
#                 summary_lines.append(f"Utility Agent: Shut down {res['grid']} power grid.")
#             elif res["agent"] == "TransportAgent":
#                 summary_lines.append(f"Transport Agent: Deployed {res['buses']} buses over {res['routes_secured']} routes.")
#             elif res["agent"] == "ReliefAgent":
#                 summary_lines.append(f"Relief Shelter Agent: Setup {res['center']} with {res['supplies']} supplies.")

#         print("\n--- SIMULATION SUMMARY ---")
#         for line in summary_lines:
#             print(line)

#         return {"disaster_type": disaster_type, "location": location, "results": results, "summary": summary_lines}
