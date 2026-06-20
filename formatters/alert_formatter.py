class AlertFormatter:

    @staticmethod
    def format(feature: dict) -> str:

        props = feature.get("properties", {})

        return (
            f"Event: {props.get('event', 'Unknown')}\n"
            f"Area: {props.get('areaDesc', 'Unknown')}\n"
            f"Severity: {props.get('severity', 'Unknown')}\n"
            f"Description: {props.get('description', '')}\n"
            f"Instructions: "
            f"{props.get('instruction', '')}"
        )