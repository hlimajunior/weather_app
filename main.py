import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from PyQt5.QtCore import Qt
from datetime import datetime

        
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Qual cidade?", self)
        self.city_input = QLineEdit("Osasco", self)
        self.get_weather_button = QPushButton("Obter meteorologia", self)
        self.temperature_label = QLabel(self)
        self.min_max_label = QLabel(self)
        self.sunrise_sunset_label = QLabel(self)
        self.sensation_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    @staticmethod
    def format_to_show(value: str) -> str:
        # Timestamp recebido
        timestamp = value
        data_hora_local = datetime.fromtimestamp(timestamp)
        data_formatada = data_hora_local.strftime("%H:%M")
        return data_formatada

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.min_max_label)
        vbox.addWidget(self.sunrise_sunset_label)
        vbox.addWidget(self.sensation_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.min_max_label.setAlignment(Qt.AlignCenter)
        self.sunrise_sunset_label.setAlignment(Qt.AlignCenter)
        self.sensation_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Setados os nomes para serem acessados pelo CSS.
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.min_max_label.setObjectName("min_max_label")
        self.sunrise_sunset_label.setObjectName("sunrise_sunset_label")
        self.sensation_label.setObjectName("sensation_label")
        self.get_weather_button.setObjectName("get_weather_button")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.format_screen()

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "SUA_API_KEY"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=pt_br&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
            print(response.status_code)
        except requests.exceptions.RequestException:
            pass

    def display_error(self, message):
        self.temperature_label.setText(message)

    def clear_weather(self):
        self.temperature_label.setText("")
        self.min_max_label.setText("")
        self.sunrise_sunset_label.setText("")
        self.sensation_label.setText("")
        self.description_label.setText("")
        self.emoji_label.setText("")

    def display_weather(self, data):
        self.clear_weather()
        # Mapeamento de ícones da API para emojis
        weather_icons = {
            "01d": "☀️",  # Céu limpo (dia)
            "01n": "🌙",  # Céu limpo (noite)
            "02d": "⛅",  # Poucas nuvens (dia)
            "02n": "☁️",  # Poucas nuvens (noite)
            "03d": "🌥️",  # Nuvens dispersas (dia)
            "03n": "☁️",  # Nuvens dispersas (noite)
            "04d": "☁️",  # Nublado
            "04n": "☁️",
            "09d": "🌧️",  # Chuva leve
            "09n": "🌧️",
            "10d": "🌦️",  # Chuva moderada (dia)
            "10n": "🌧️",  # Chuva moderada (noite)
            "11d": "⛈️",  # Tempestade
            "11n": "⛈️",
            "13d": "❄️",  # Neve
            "13n": "❄️",
            "50d": "🌫️",  # Névoa
            "50n": "🌫️",
        }

        emoji = weather_icons.get(data["weather"][0].get("icon"), "❓")  # ❓ caso não encontre
        min_temp = data["main"]["temp_min"]
        max_temp = data["main"]["temp_max"]
        vento = data["wind"]["speed"]
        direcao = data["wind"]["deg"]
        sunrise = self.format_to_show(data["sys"]["sunrise"])
        sunset = self.format_to_show(data["sys"]["sunset"])

        self.temperature_label.setText(f'{data["main"]["temp"]:.1f}°C')
        self.min_max_label.setText(f"🌡️ min {min_temp:.1f} / max {max_temp:.1f}\n🍃Vento {vento:.1f}m/s {vento*3.6:.0f}km/h 🧭 {direcao}°")
        self.sunrise_sunset_label.setText(f"🌞 {sunrise} 🌚 {sunset}")
        self.sensation_label.setText(f'🥵🥶 Sensação de {data["main"]["feels_like"]:.1f}°C')
        self.description_label.setText(f'{data["weather"][0].get("description")}')
        self.emoji_label.setText(f"{emoji}")

    def format_screen(self):
        self.setStyleSheet(
            """
            QLabel,QPushButton, QLineEdit{
                font-family: calibri;
                font-size: 40px;
            }                   
            QLabel#city_label{
                font-size: 30px;
                font-style: italic;
            }
            QPushButton#get_weather_button,
            QLabel#description_label{
                font-size: 30px;
                color: #0000ff
            }
            QPushButton#get_weather_button{
                font-weight: bold
            }
            QLabel#temperature_label{
                font-size: 70px;
                color: #007700
            }
            QLabel#emoji_label,
            QLabel#sensation_label,
            QLabel#min_max_label,
            QLabel#sunrise_sunset_label{
                font-family: Segoe UI emoji;
                font-size: 20px;
            }
            QLabel#emoji_label{
                font-size: 100px;
            }
                
        """
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
