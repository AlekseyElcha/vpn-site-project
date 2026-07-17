from typing import Dict


def extract_basic_client_info(
        data: Dict[str, str]
) -> Dict[str, str | int]:
    info_block = data.get("obj", {})
    client_data = info_block.get("client", {})

    used_traffic = info_block.get("usedTraffic")
    total_traffic = client_data.get("totalGB")

    traffic_left = (total_traffic - used_traffic) if total_traffic > 0 else -1

    total_gb = client_data.get("totalGB") if client_data.get("totalGB") > 0 else -1

    # expiry_time ???

    client_info = {
        "email": client_data.get("email"),
        "totalGB": total_gb ,
        "expiryTime": client_data.get("expiryTime"),
        "trafficLeft": traffic_left
    }

    return client_info
