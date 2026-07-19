def build_vpn_subscription_link_from_params(
        domain: str,
        port: int,
        prefix: str,
        sub_id: str
) -> str:
    return f"{domain}:{port}/{prefix}/{sub_id}"
