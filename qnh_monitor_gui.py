#!/usr/bin/env python
import sys

if sys.version_info[0] < 3:
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk as ttk

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'


class MainView:
    """Main GUI class responsible for initiating separate window frames for the various display elements."""

    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, padx=5, pady=5)
        self.qnh_view = QNHview(master)
        self.controls_view = ControlsView(master)


class QNHview:
    """Label window frame containing the widgets for displaying Obs time, latest and previous QNH. """

    def __init__(self, root):
        self.frame_qnh_monitor = tk.LabelFrame(root, text='Heathrow QNH monitor')
        self.frame_qnh_monitor.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        self.time_label = ttk.Label(self.frame_qnh_monitor, text="Obs Time (Z) :")
        self.time_label.grid(row=1, column=0, padx=5, pady=5)

        self.time = tk.StringVar()
        self.time_result = ttk.Label(self.frame_qnh_monitor, textvariable=self.time, width=10,
                                         justify='center', anchor=tk.W)
        self.time_result.grid(row=1, column=1, padx=5, pady=5)

        self.prev_qnh_label = ttk.Label(self.frame_qnh_monitor, text='Previous (hPa) :')
        self.prev_qnh_label.grid(row=1, column=2, padx=5, pady=5)

        self.prev_qnh = tk.StringVar()
        self.prev_qnh_result = ttk.Label(self.frame_qnh_monitor, textvariable=self.prev_qnh, width=10,
                                         justify='center')
        self.prev_qnh_result.grid(row=1, column=3, padx=5, pady=5)

        self.now_qnh_label = ttk.Label(self.frame_qnh_monitor, text='Latest (hPa) :')
        self.now_qnh_label.grid(row=1, column=4, padx=5, pady=5)

        self.latest_qnh = tk.StringVar()
        self.latest_qnh_result = ttk.Label(self.frame_qnh_monitor, textvariable=self.latest_qnh, width=10,
                                           justify='center', anchor=tk.W)
        self.latest_qnh_result.grid(row=1, column=5, padx=5, pady=5)


class ControlsView:
    """ GUI elements - monitoring, update and exit buttons"""
    def __init__(self, root):
        self.frame_controls = ttk.Frame(root)
        self.frame_controls.grid(row=2, column=0, padx=5, pady=5)

        self.monitor_button = ttk.Button(self.frame_controls, text='Start Monitor', width=16)
        self.monitor_button.grid(sticky=tk.W, row=0, column=0, padx=5, pady=5)

        self.status_label = ttk.Label(self.frame_controls, width=20, text='                 ')
        self.status_label.grid(sticky=tk.W, row=0, column=1, padx=5, pady=5)

        self.hh20_alert = tk.IntVar()
        self.hh20_checkbox = ttk.Checkbutton(self.frame_controls, text='HH+20 Alert',
                                             variable=self.hh20_alert)
        self.hh20_checkbox.grid(sticky=tk.E, row=0, column=3, padx=5, pady=5)

        self.update_data_button = ttk.Button(self.frame_controls, text='Update Now')
        self.update_data_button.grid(sticky=tk.W, row=0, column=4, padx=5, pady=5)

        self.exit_button = ttk.Button(self.frame_controls, text='Exit')
        self.exit_button.grid(sticky=tk.E, row=0, column=5, padx=5, pady=5)

