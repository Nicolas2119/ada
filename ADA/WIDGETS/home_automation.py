import os
import requests
from dotenv import load_dotenv

load_dotenv()

HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")
HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN")

AC_ENTITY_ID = os.getenv("AC_ENTITY_ID")
LIGHT_ENTITY_ID = os.getenv("LIGHT_ENTITY_ID")
TV_ENTITY_ID = os.getenv("TV_ENTITY_ID")


def _call_service(domain: str, service: str, entity_id: str) -> str:
    """Helper to call a Home Assistant service."""
    if not HOME_ASSISTANT_URL or not HOME_ASSISTANT_TOKEN:
        return "Home Assistant configuration missing."

    url = f"{HOME_ASSISTANT_URL}/{domain}/{service}"
    headers = {
        "Authorization": f"Bearer {HOME_ASSISTANT_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"entity_id": entity_id}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        response.raise_for_status()
        return f"Sent {service} to {entity_id}."
    except requests.RequestException as e:
        return f"Error calling service: {e}"


def ac_power(state: str) -> str:
    """Turn the AC on or off."""
    if not AC_ENTITY_ID:
        return "AC entity ID not configured."
    service = "turn_on" if state.lower() == "on" else "turn_off"
    return _call_service("climate", service, AC_ENTITY_ID)


def light_power(state: str) -> str:
    """Turn a light on or off."""
    if not LIGHT_ENTITY_ID:
        return "Light entity ID not configured."
    service = "turn_on" if state.lower() == "on" else "turn_off"
    return _call_service("light", service, LIGHT_ENTITY_ID)


def tv_power(state: str) -> str:
    """Turn the TV on or off."""
    if not TV_ENTITY_ID:
        return "TV entity ID not configured."
    service = "turn_on" if state.lower() == "on" else "turn_off"
    return _call_service("media_player", service, TV_ENTITY_ID)


if __name__ == "__main__":
    print(ac_power("on"))
    print(light_power("off"))
    print(tv_power("on"))
