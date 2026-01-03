from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import csv

Window.size = (360, 700)

# --- Main logic ---
def get_mass_and_people_from_area(area, filename="information.csv"):
    valid_rows = []

    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["min_area"] and row["max_area"]:
                min_a = float(row["min_area"])
                max_a = float(row["max_area"])

                if min_a < area <= max_a:
                    valid_rows.append({
                        "mass": int(row["mass"]),
                        "people": int(row["people"])
                    })

    if not valid_rows:
        return None, None

    mass = max(r["mass"] for r in valid_rows)
    people = min(r["people"] for r in valid_rows)

    return mass, people


class LiftApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        title = Label(
            text="Lift Cabin Capacity Calculator",
            font_size=22,
            size_hint=(1, 0.15)
        )

        self.length_input = TextInput(
            hint_text="Cabin Length (meters)",
            multiline=False,
            input_filter="float",
            font_size=18
        )

        self.width_input = TextInput(
            hint_text="Cabin Width (meters)",
            multiline=False,
            input_filter="float",
            font_size=18
        )

        self.front_width_input = TextInput(
            hint_text="Front Width (meters)",
            multiline=False,
            input_filter="float",
            font_size=18
        )

        self.front_depth_input = TextInput(
            hint_text="Front Depth (meters)",
            multiline=False,
            input_filter="float",
            font_size=18
        )

        self.result_label = Label(
            text="",
            font_size=18,
            halign="center",
            valign="middle"
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))

        calc_button = Button(
            text="Calculate",
            font_size=18,
            size_hint=(1, 0.15)
        )
        calc_button.bind(on_press=self.calculate)

        layout.add_widget(title)
        layout.add_widget(self.length_input)
        layout.add_widget(self.width_input)
        layout.add_widget(self.front_width_input)
        layout.add_widget(self.front_depth_input)
        layout.add_widget(calc_button)
        layout.add_widget(self.result_label)

        return layout

    def calculate(self, instance):
        try:
            cabin_length = float(self.length_input.text)
            cabin_width = float(self.width_input.text)
            front_width = float(self.front_width_input.text)
            front_depth = float(self.front_depth_input.text)

            # Calculate usable area limited by front dimensions
            area = (cabin_length*cabin_width) + (front_width* front_depth)
            mass, people = get_mass_and_people_from_area(area)

            if mass:
                self.result_label.text = (
                    f"Masahat: {area:.3f} m²\n\n"
                    f"Zarfiat: {mass} kg\n"
                    f"Tedade nafarat: {people}"
                )
            else:
                self.result_label.text = "Bar asase etelaate dadeshode javabi peyda nashod."

        except ValueError:
            self.result_label.text = "Lotfan tanha meghdare adadi vared konid"


if __name__ == "__main__":
    LiftApp().run()