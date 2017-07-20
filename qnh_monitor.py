#!/usr/bin/env python
import sys
import logging
import get_qnh
import qnh_monitor_gui as gui
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logging.basicConfig()

if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkMessageBox
else:
    import tkinter as tk
    from tkinter import messagebox as tkMessageBox

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'


class Controller:
    """Main GUI controller, handles mouse, keyboard and data change events."""

    def __init__(self):
        self.root = tk.Tk()
        self.main_view = gui.MainView(self.root)

        self.latest_qnh = None
        self.latest_time = None
        self.latest_data = None
        self.latest_data_str = None
        self.previous_qnh = None
        self.previous_time = None

        self.monitoring = False

        self.main_view.controls_view.monitor_button.bind('<Button>', self.start_monitor)
        self.main_view.controls_view.monitor_button.bind('<Return>', self.start_monitor)

        self.main_view.controls_view.exit_button.bind('<Button>', self.exit_app)
        self.main_view.controls_view.exit_button.bind('<Return>', self.exit_app)

        self.main_view.controls_view.update_data_button.bind('<Button>', self.update_data_now)
        self.main_view.controls_view.update_data_button.bind('<Return>', self.update_data_now)

    def run(self):
        """Start the application"""
        self.root.title('Heathrow QNH Monitor v0.4')
        self.root.deiconify()
        self.root.mainloop()

    def start_monitor(self, event):
        """Start the automatic monitoring of Heathrow QNH, initial value is collected and fields updated
        before setting up scheduled check
        :param event: Start Monitoring button pressed"""
        if not self.monitoring:
            self.monitoring = True
            self.update_qnh()
            self.data_check_sched()
            self.main_view.controls_view.monitor_button.configure(text='Monitoring...')
            self.main_view.controls_view.status_label.configure(text=' ')

    def data_check_sched(self):
        """Set a schedule for updating and checking the Heathrow METAR message using a background scheduler. """

        scheduler = BackgroundScheduler()
        trigger = IntervalTrigger(seconds=450)

        scheduler.add_job(self.update_qnh, trigger)
        scheduler.start()

    def update_data_now(self, event):
        """Response action for 'Update Now' button press - initiate update of QNH/Time fields.
        :param event: 'Update Now' button pressed.
        """
        self.update_qnh()

    def update_qnh(self):
        """ Get the latest QNH and obs time readings, check if time is different from last METAR and if
        QNH value has changed from a previous reading. Initiate an Info box message window if QNH has changed and this
        is not the first check"""

        self.latest_data = get_qnh.get_qnh_data()

        # Make sure we have some data
        if self.latest_data is not None:

            # set the latest QNH and time values from our latest dataset
            self.latest_qnh = self.latest_data[1]
            self.latest_time = self.latest_data[0]
            self.latest_data_str = self.latest_time + '    ' + str(self.latest_qnh)

            # Check is this is a new obs report
            if self.latest_time != self.previous_time:

                # Set the latest and previous values in the GUI elements
                self.main_view.qnh_view.prev_qnh.set(self.previous_qnh)
                self.main_view.qnh_view.latest_qnh.set(self.latest_qnh)
                self.main_view.qnh_view.time.set(self.latest_time)

                # If QNH has changed and this is not the first reading, raise an info box window to alert user
                if self.latest_qnh != self.previous_qnh and self.previous_qnh is not None:
                    tkMessageBox.showinfo('Heathrow QNH changed:', self.latest_data_str)

                # We've finished now so set the previous values to the latest values ready for the next update
                self.previous_qnh = self.latest_qnh
                self.previous_time = self.latest_time

    @staticmethod
    def exit_app(self):
        sys.exit()


if __name__ == '__main__':
    controller = Controller()
    controller.run()
