import datetime
import re
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.dates import date2num
from matplotlib.colors import Colormap


def seconds_to_text(seconds, *args):
    if len(args) > 1: return
    elif len(args) == 1: addS = args[0]
    else: addS = False

    if seconds == 0: return 0
    days = int(seconds // 86400)
    seconds %= 86400
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = round(seconds % 60, 3)

    days_text = ''
    if days: days_text = f"{f'{days:,}'} days"
    if days == 1 or (days and addS): days_text = f"{f'{days:,}'} day"
    days_comma = ''
    if days and (hours or minutes or seconds): days_comma = ', '

    hours_text = ''
    if hours: hours_text = f"{hours} hours"
    if hours == 1 or (hours and addS): hours_text = f"{hours} hour"
    hours_comma = ''
    if hours and (minutes or seconds): hours_comma = ', '

    minutes_text = ''
    if minutes: minutes_text = f"{minutes} minutes"
    if minutes == 1 or (minutes and addS): minutes_text = f"{minutes} minute"
    minutes_comma = ''
    if minutes and seconds: minutes_comma = ', '

    seconds_text = ''
    if seconds: seconds_text = f"{seconds} seconds"
    if seconds == 1 or (seconds and addS): seconds_text = f"{seconds} second"
    return days_text + days_comma + hours_text + hours_comma + minutes_text + minutes_comma + seconds_text


def num_to_text(n):
    endings = ['th', 'st', 'nd', 'rd']
    try:
        ending = endings[n % 10]
    except IndexError:
        ending = 'th'
    if n % 100 - n % 10 == 10: ending = 'th'
    return f"{f'{n:,}'}{ending}"


def href_universe(universe):
    return f"[`{universe}`](https://play.typeracer.com/?universe={universe})"


def graph_color(ax, information, boxplot, *patches):
    to_rgba = lambda x: (x // 65536 / 255,
                         ((x % 65536) // 256) / 255, x % 256 / 255)

    (bg, graph_bg, axis, line, text, grid, cmap, user) = information.values()
    legend = ax.get_legend()
    black = True

    if bg != None:
        ax.figure.set_facecolor(to_rgba(bg))

    if graph_bg != None:
        ax.set_facecolor(to_rgba(graph_bg))

        if legend:
            legend.get_frame().set_facecolor(to_rgba(graph_bg))

        if sum(to_rgba(graph_bg)) <= 1.5:
            black = False

    if axis != None:
        ax.spines['bottom'].set_color(to_rgba(axis))
        ax.spines['top'].set_color(to_rgba(axis))
        ax.spines['left'].set_color(to_rgba(axis))
        ax.spines['right'].set_color(to_rgba(axis))

    if line != None:
        line_color = to_rgba(line)

        index = 0
        graph_lines = ax.get_lines()
        for i, graph_line in enumerate(graph_lines):
            if graph_line.get_label() == user:
                index = i
                break

        if graph_lines:
            if boxplot:
                for line_ in graph_lines[0:5]:
                    line_.set_color(line_color)
            else:
                if cmap != None:
                    x, y = graph_lines[index].get_data()
                    label = graph_lines[index].get_label()
                    ax.lines.pop(index)

                    if isinstance(x[0], datetime.date):
                        x = date2num(list(x))
                    points = np.array([x, y]).T.reshape(-1, 1, 2)

                    segments = np.concatenate([points[:-1], points[1:]],
                                              axis=1)
                    lc = LineCollection(segments, cmap=cmap)
                    lc.set_array(y)
                    ax.add_collection(lc)
                else:
                    graph_lines[index].set_color(line_color)
        elif len(patches) > 0:
            for patch in patches[0]:
                patch.set_facecolor(line_color)

        if legend:
            legend.get_lines()[index].set_color(line_color)

    if text != None:
        text_color = to_rgba(text)
        ax.set_title(label=ax.get_title(), color=text_color)
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.tick_params(colors=text_color)

        if legend:
            for text_ in legend.get_texts():
                text_.set_color(text_color)

    if grid != None:
        ax.grid(b=True, color=to_rgba(grid))

    if ax.collections:
        color_ = (0, 0, 0) if black else (1, 1, 1)
        for collection in ax.collections:
            collection.set_color(color_)


escape_sequence = lambda x: bool(re.findall('[^a-z^0-9^_]', x.lower()))
