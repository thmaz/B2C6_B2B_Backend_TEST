""" Flet Calendar Widget/Application """

import flet
from flet import * 
import calendar
import datetime

CELL_SIZE = (28, 28)
CELL_BG_COLOR = ("white10")
TODAY_BG_COLOR = ("teal600")

class SetCalendar(UserControl):
    def __init__(self, start_year=datetime.date.today().year):
# Hier worden de maanden van 2024 getoond, als we de maanden van andere jaren willen tonen, moeten we een extra instance aanmaken voor dat jaar
        
        self.current_year = start_year # Huidige jaar
        self.m1 = datetime.date.today().month # Huidige maand
        self.m2 = self.m1 + 1 

        # Tracking van clicks
        self.click_count: list = []
        self.long_press_count: list = []

        self.current_color = "blue" # Highlight kleur

        self.selected_date = any # Geselecteerde datum van de kalender

        self.calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        super().__init__()

    def _change_month(self, delta):
        self.m1 = min(max(1, self.m1 + delta), 12)
        self.m2 = min(max(2, self.m2 + delta), 13)

        new_calendar = self.create_month_calendar(self.current_year)
        self.calendar_grid = new_calendar
        self.update()

    def one_click_date(self, e):
        self.selected_date = e.control.data
        e.control.bgcolor = "blue600"
        e.control.update()
        self.update()


    def long_click_date(self, e):
        self.long_press_count.append(e.control.data)
        if len(self.long_press_count) == 2:
            date1, date2 = self.long_press_count

            delta = abs(date2 - date1)

            if date1 < date2:
                dates = [
                    date1 + datetime.timedelta(days=x) for x in range(delta.days + 1)
                ]
            else:
                dates = [
                    date2 + datetime.timedelta(days=x) for x in range(delta.days + 1)
                ]

            for _ in self.calendar_grid.controls[:]:
                for __ in _.controls[:]:
                    if isinstance(__, Row):
                        for box in __.controls[:]:
                            if box.data in dates:
                                box.bgcolor = "blue600"
                                box.update()

            self.long_press_count = []
        else:
            pass

    def create_month_calendar(self,year):
        self.current_year = year
        self.calendar_grid.controls: list = [] # type: ignore

        for month in range(self.m1, self.m2):
            # Hier halen we de naam van de maand en het jaar op
            month_label = Text(
                f"{calendar.month_name[month]} {self.current_year}",
                size=14,
                weight='bold',
                color = "white"
            )

            month_matrix = calendar.monthcalendar(self.current_year, month)
            month_grid = Column(alignment=MainAxisAlignment.CENTER)
            month_grid.controls.append(
                Row(
                    alignment=MainAxisAlignment.START, controls=
                    [month_label],
                )
            )

            weekday_labels = [
                Container(
                    width=28,
                    height=28,
                    alignment=alignment.center,
                    content=Text(
                        weekday,
                        size=12,
                        color="white", 
                    ),
                )
                for weekday in ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]
            ]

            weekday_row = Row(controls=weekday_labels)
            month_grid.controls.append(weekday_row)

            for week in month_matrix:
                week_container = Row()
                for day in week:
                    if day==0:
                        day_container = Container(
                            width=28,
                            height=28,
                        )
                    else:
                        day_container = Container(
                            width=28,
                            height=28,
                            border=border.all(0.5, "white"),
                            alignment=alignment.center,
                            data=datetime.date(
                                year=self.current_year,
                                month=month,
                                day=day,
                            ),
                            on_click=lambda e: self.one_click_date(e),
                            on_long_press=lambda e: self.long_click_date(e),
                            animate=400,
                        )

                    day_label = Text(str(day), size=12)

                    if day == 0:
                        day_label = None
                    if (
                        day == datetime.date.today().day
                        and month == datetime.date.today().month
                        and self.current_year == datetime.date.today().year
                    ):
                        day_container.bgcolor = "teal700"
                    day_container.content = day_label
                    week_container.controls.append(day_container)
                month_grid.controls.append(week_container)

            self.calendar_grid.controls.append(month_grid)

            return self.calendar_grid

    def build(self):
        return self.create_month_calendar(self.current_year)
    
class DateSetUp(UserControl):
    def __init__(self, cal_grid):
        self.cal_grid = cal_grid # Kalender instance

        self.prev_btn = BtnPagination("Prev.", lambda e: cal_grid._change_month(-1))
        self.next_btn = BtnPagination("Next", lambda e: cal_grid._change_month(1))


        self.today = Text(
            datetime.date.today().strftime("%B %d, %Y"),
            width=260,
            size=13,
            color="white",
            weight="w400",
        )

        # Hier maken we knoppen aan
        self.btn_container = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.prev_btn,
                self.next_btn,
            ],
        )

        self.calendar = Container(
            width=320,
            height=45,
            bgcolor="#989c99",
            border_radius=8,
            animate=300,
            clip_behavior=ClipBehavior.HARD_EDGE,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Divider(height=60, color='transparent'),
                    self.cal_grid,
                    Divider(height=10, color='transparent'),
                    self.btn_container,
                ],
            ),
        )

        super().__init__()

    def _get_calendar(self, e:None):
        if self.calendar.height == 45:
            self.calendar.height = 450
            self.calendar.update()
        else:
            self.calendar.height = 45
            self.calendar.update()
        pass

    def build(self):
        return Stack(
            width=320,
            controls=[
                self.calendar,
                Container(
                    on_click= lambda e: self._get_calendar(e),
                    width=320,
                    height=45,
                    border_radius=8,
                    bgcolor="white24",
                    padding=padding.only(left=15, right=5),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.today,
                            Container(
                                width=32, 
                                height=32,
                                border=border.only(
                                    left=BorderSide(0.9, "white24"),
                                ),
                                alignment=alignment.center,
                                content=Icon(
                                    name=icons.CALENDAR_MONTH_SHARP,
                                    size=15,
                                    opacity=0.65,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )
    
class BtnPagination(UserControl):
    def __init__(self, txt_name, function):
        self.txt_name = txt_name
        self.function = function
        super().__init__()

    def build(self):
        return IconButton(
            content=Text(self.txt_name, size=8, weight="bold"),
            width=56,
            height=28,
            on_click=self.function,
            style=ButtonStyle(
                shape={
                    "": RoundedRectangleBorder(radius=6)}, bgcolor={"": "white"}
            ),
        )

def main(page: Page):
    page.horizontal_alignments = "center"
    page.vertical_alignment = "center"
    page.padding = 80

    # Instances
    cal = SetCalendar()
    date = DateSetUp(cal)

    # Main UI 
    page.add(Row(
        alignment=MainAxisAlignment.CENTER,
        controls=[
            date,
        ],
    ))
    page.update()

if __name__ == "__main__":
    flet.app(target=main)