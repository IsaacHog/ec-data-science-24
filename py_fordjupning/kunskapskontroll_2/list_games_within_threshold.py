import pandas as pd

df = pd.read_csv("full_time_log.csv", parse_dates=["event_start", "time_stamp"])
df.sort_values(by=["event_id", "time_stamp"], inplace=True)

def percent_change(old, new):
    if old == 0:
        return 0
    return abs(new - old) / old

flagged_events = []
THRESHOLD = 0.08
for event_id, group in df.groupby("event_id"):
    group = group.reset_index(drop=True)
    for i in range(len(group) - 1):
        for j in range(i + 1, min(i + 4, len(group))):  # Compare up to 4 data points ahead
            row_i = group.loc[i]
            row_j = group.loc[j]
            changes = {
                "home": percent_change(row_i["home_odds"], row_j["home_odds"]),
                "even": percent_change(row_i["even_odds"], row_j["even_odds"]),
                "away": percent_change(row_i["away_odds"], row_j["away_odds"]),
            }
            if any(change > THRESHOLD for change in changes.values()):
                if (row_i["home_odds"] > 6000 or row_i["away_odds"] > 6000 or row_i["even_odds"] > 6000):
                    continue
                flagged_events.append({
                    "event_id": event_id,
                    "match_name": row_i["match_name"],
                    "event_start": row_i["event_start"],
                    "time_1": row_i["time_stamp"],
                    "time_2": row_j["time_stamp"],
                    "home_change": changes["home"],
                    "even_change": changes["even"],
                    "away_change": changes["away"],
                })

flagged_df = pd.DataFrame(flagged_events)
print(flagged_df)
