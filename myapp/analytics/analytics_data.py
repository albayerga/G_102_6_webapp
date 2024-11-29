import json
import random
from datetime import datetime, timedelta


class AnalyticsData:
    def __init__(self):
        self.fact_clicks = dict([])  # {doc_id: [{"query_id": int, "timestamp": datetime, "dwell_time": float}]}
        self.fact_queries = []  # [{"query_id": int, "terms": str, "timestamp": datetime, "user_agent": str, "ip": str}]
        self.fact_visitors = []  # [{"user_agent": str, "ip": str, "os": str, "device": str, "timestamp": datetime}]
        self.fact_sessions = dict([])  # {session_id: {"ip": str, "user_agent": str, "start_time": datetime, "queries": [...], "clicks": [...]}}
        self.session_timeout = timedelta(minutes=30)  # Sesión expira tras 30 minutos de inactividad

    def save_query_terms(self, terms: str, user_agent: str, ip: str) -> int:
        query_id = random.randint(0, 100000)
        timestamp = datetime.now()
        self.fact_queries.append({
            "query_id": query_id,
            "terms": terms,
            "timestamp": timestamp,
            "user_agent": user_agent,
            "ip": ip
        })
        self._update_session(ip, user_agent, {"type": "query", "query_id": query_id, "timestamp": timestamp})
        return query_id

    def track_click(self, doc_id: str, query_id: int):
        timestamp = datetime.now()
        if doc_id not in self.fact_clicks:
            self.fact_clicks[doc_id] = []
        self.fact_clicks[doc_id].append({"query_id": query_id, "timestamp": timestamp, "dwell_time": None})
        # Asociar clic a la sesión
        self._update_session_by_query(query_id, {"doc_id": doc_id, "timestamp": timestamp})

    def track_return(self, doc_id: str):
        """Registrar retorno para calcular el dwell time."""
        return_timestamp = datetime.now()
        #for click in self.fact_clicks.get(doc_id, []):
        for click in reversed(self.fact_clicks.get(doc_id, [])):
            if click["dwell_time"] is None:
                click["dwell_time"] = (return_timestamp - click["timestamp"]).total_seconds()
                break

    def track_visitor(self, user_agent: str, ip: str):
        visitor_id = self._generate_session_id(ip, user_agent)  # Crear ID único
        timestamp = datetime.now()
        
        visitor_data = {
            "visitor_id": visitor_id,
            "user_agent": user_agent,
            "ip": ip,
            "os": self._get_os_from_user_agent(user_agent),
            "device": self._get_device_from_user_agent(user_agent),
            "timestamp": timestamp
        }
        # Verificar si el visitante ya existe
        if visitor_id not in self.fact_visitors:
            self.fact_visitors.append(visitor_data)
            self._update_session(ip, user_agent, {"type": "visitor", "timestamp": timestamp})

    def _update_session(self, ip: str, user_agent: str, activity: dict):
        """Actualizar o crear una sesión basada en la IP y User-Agent."""
        session_id = self._generate_session_id(ip, user_agent)
        session = self.fact_sessions.get(session_id)

        if session is None or datetime.now() - session["start_time"] > self.session_timeout:
            # Crear una nueva sesión si no existe o si expiró
            self.fact_sessions[session_id] = {
                "ip": ip,
                "user_agent": user_agent,
                "start_time": datetime.now(),
                "queries": [],
                "clicks": []
            }
        # Agregar la actividad correspondiente
        if activity["type"] == "query":
            self.fact_sessions[session_id]["queries"].append(activity)
        elif activity["type"] == "visitor":
            self.fact_sessions[session_id]["start_time"] = activity["timestamp"]

    def _update_session_by_query(self, query_id: int, click_data: dict):
        """Asociar clics a sesiones basadas en el query_id."""
        for session in self.fact_sessions.values():
            if any(query["query_id"] == query_id for query in session["queries"]):
                session["clicks"].append(click_data)
                break

    def _generate_session_id(self, ip: str, user_agent: str) -> str:
        """Generar un ID único basado en IP y User-Agent."""
        return f"{ip}:{user_agent}"

    def _get_os_from_user_agent(self, user_agent: str) -> str:
        """Analizar el sistema operativo desde el User-Agent (simplificado)."""
        if "Windows" in user_agent:
            return "Windows"
        elif "Mac" in user_agent:
            return "MacOS"
        elif "Linux" in user_agent:
            return "Linux"
        elif "Android" in user_agent:
            return "Android"
        elif "iPhone" in user_agent:
            return "iOS"
        return "Unknown"

    def _get_device_from_user_agent(self, user_agent: str) -> str:
        """Determinar el tipo de dispositivo (simplificado)."""
        if "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent:
            return "Mobile"
        elif "Tablet" in user_agent:
            return "Tablet"
        return "Desktop"
