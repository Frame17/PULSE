from numpy import mean


Q_MONTH_MAPPING = ["01", "04", "07", "10"]


def aggregate_to_quarterly(data):
    quarterly_data = {}
    for entry in data:
        date = entry["timestamp"].split("-")
        quarter = (int(date[1]) - 1) // 3 + 1
        quarter_key = f"{date[0]}-{Q_MONTH_MAPPING[quarter - 1]}"

        if quarter_key not in quarterly_data:
            quarterly_data[quarter_key] = []
        quarterly_data[quarter_key].append(entry["value"])

    return [
        {
            "timestamp": key,
            "value": mean(values),
        }
        for key, values in quarterly_data.items()
    ]


def aggregate_to_yearly(data):
    yearly_data = {}
    for entry in data:
        date = entry["timestamp"].split("-")
        year_key = date[0]
        if year_key not in yearly_data:
            yearly_data[year_key] = []
        yearly_data[year_key].append(entry["value"])

    return [
        {"timestamp": key, "value": mean(values)} for key, values in yearly_data.items()
    ]


def aggregate_mean(aggregation_period, data):
    if aggregation_period == "Q":
        return aggregate_to_quarterly(data)
    if aggregation_period == "A":
        return aggregate_to_yearly(data)
    raise ValueError(f'Invalid aggregation period: "{aggregation_period}"')
