def validate_schema(schema):
    alerts = []
    for col in schema:
        if col["null_pct"] > 0.2:
            alerts.append(f"Column '{col['column']}' has high null percentage: {col['null_pct']:.1%}")
    return alerts
