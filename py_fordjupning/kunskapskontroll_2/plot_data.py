import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
import matplotlib.dates as mdates

df = pd.read_csv("full_time_log.csv", parse_dates=["time_stamp"])
events = df[['event_id', 'match_name', 'event_start']].drop_duplicates().reset_index(drop=True)
match_labels = [f"{row['match_name']} ({row['event_start']})" for _, row in events.iterrows()]
event_map = dict(zip(match_labels, events['event_id']))

fig = plt.figure(figsize=(10, 6))
plt.subplots_adjust(left=0.3, bottom=0.2)

ax_radio = None
radio = None
ax_back = None
back_button = None

ax_plot = fig.add_axes([0.3, 0.2, 0.65, 0.7])
ax_plot.set_visible(False)

def plot_event(event_id, label):
    global ax_radio, radio
    match_data = df[df['event_id'] == event_id]
    match_name = label.split(' (')[0]

    ax_plot.clear()
    ax_plot.plot(match_data['time_stamp'], match_data['home_odds'], label='Home Odds', marker='o')
    ax_plot.plot(match_data['time_stamp'], match_data['even_odds'], label='Draw Odds', marker='o')
    ax_plot.plot(match_data['time_stamp'], match_data['away_odds'], label='Away Odds', marker='o')

    ax_plot.set_title(f"Odds Over Time: {match_name}")
    ax_plot.set_xlabel("Timestamp")
    ax_plot.set_ylabel("Odds")
    ax_plot.legend()
    ax_plot.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    if ax_radio:
        ax_radio.remove()
        ax_radio = None
        radio = None

    ax_plot.set_visible(True)
    back_button.ax.set_visible(True)
    fig.canvas.draw_idle()

def go_back(event):
    ax_plot.clear()
    ax_plot.set_visible(False)
    back_button.ax.set_visible(False)
    plot_radio()
    fig.suptitle("Select a Match", fontsize=14)
    fig.canvas.draw_idle()

def plot_radio():
    global ax_radio, radio, ax_back, back_button

    ax_radio = plt.axes([0.05, 0.2, 0.9, 0.7])
    radio = RadioButtons(ax_radio, match_labels)
    for label in radio.labels:
        label.set_fontsize(11)
    radio.on_clicked(lambda label: plot_event(event_map[label], label))

    if not back_button:
        ax_back = plt.axes([0.05, 0.5, 0.1, 0.05])
        back_button = Button(ax_back, 'Back')
        back_button.on_clicked(go_back)
    back_button.ax.set_visible(False)

# Initial screen
plot_radio()
fig.suptitle("Select a Match", fontsize=14)
plt.show()
