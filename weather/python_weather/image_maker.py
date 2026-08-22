import cv2 as cv
import math


def get_yellow_mutated(value: int = 0):
    return (value, 255, 255)


def get_blue_dark_mutated(value: int = 0):
    return (255, value, value)


def get_blue_light_mutated(value: int = 0):
    green = 170 + value
    blue = 66 + value

    if green > 85:
        return (255, 255, blue)

    if blue > 189:
        return (255, 255, 255)

    return (255, green, blue)


def get_gray_mutated(value: int = 0):
    if value > 127:
        return (250, 255, 255)
    return (128 + value, 128 + value, 128 + value)


canvas_path = "canvas.jpg"


weather_logo_cloud_path = "weather_image/cloud.jpg"
weather_logo_rain_path = "weather_image/rain.jpg"
weather_logo_snow_path = "weather_image/snow.jpg"
weather_logo_sun_path = "weather_image/sun.jpg"


class ImageMaker:
    def __init__(self, options: list):
        self.weather_options = options
        self.draw_options = {
            "sunny": {
                "color": get_yellow_mutated,
                "icon": weather_logo_sun_path,
            },
            "snow": {
                "color": get_blue_light_mutated,
                "icon": weather_logo_snow_path,
            },
            "rain": {
                "color": get_blue_dark_mutated,
                "icon": weather_logo_rain_path,
            },
            "cloudy": {
                "color": get_gray_mutated,
                "icon": weather_logo_cloud_path,
            },
        }

    def draw_cards(self):

        for day in self.weather_options:
            img = cv.imread(canvas_path)

            weather = day["weather"] if "weather" in day else None

            if weather in self.draw_options:

                draw_option = self.draw_options[weather]

                weather_logo = cv.imread(draw_option["icon"])
                # os.remove(iconTemplatePath)

                font = cv.FONT_HERSHEY_TRIPLEX

                # размеры шаблона
                heigth_canvas, width_canvas = img.shape[:2]

                if weather == "rain":
                    # цвет заднего фона
                    step = math.floor(width_canvas / 255)
                    for period_number in range(0, width_canvas, step):
                        img[
                            0:heigth_canvas, 0 + period_number : step + period_number
                        ] = draw_option["color"](math.floor(period_number / step))

                if weather == "sunny":
                    # цвет заднего фона
                    step = math.floor(width_canvas / 255)
                    for period_number in range(0, width_canvas, step):
                        img[
                            0:heigth_canvas, 0 + period_number : step + period_number
                        ] = draw_option["color"](math.floor(period_number / step))

                if weather == "cloudy":
                    # цвет заднего фона
                    step = math.floor(width_canvas / 255)
                    for period_number in range(0, width_canvas, step):
                        img[
                            0:heigth_canvas, 0 + period_number : step + period_number
                        ] = draw_option["color"](math.floor(period_number / step))

                if weather == "snow":
                    # цвет заднего фона
                    step = math.floor(width_canvas / 255)
                    for period_number in range(0, width_canvas, step):
                        img[
                            0:heigth_canvas, 0 + period_number : step + period_number
                        ] = draw_option["color"](math.floor(period_number / step))

                font_options = [
                    {"param": "city", "font_size": 1, "point": (20, 30)},
                    {"param": "temperature", "font_size": 2, "point": (350, 110)},
                    {"param": "weather", "font_size": 2, "point": (20, 230)},
                ]

                for font_option in font_options:

                    param = font_option["param"]

                    text_param = day[param] if param in day else ""

                    cv.putText(
                        img=img,
                        text=text_param,
                        org=font_option["point"],
                        fontFace=font,
                        fontScale=font_option["font_size"],
                        thickness=2,
                        color=(0, 0, 0),
                    )

                # начало координат вставки иконки погоды
                x_offset = 200
                y_offset = 80

                # размер изображения
                height_weather_logo, width_weather_logo = weather_logo.shape[:2]

                # y - строка, х столбец в двухмерном массиве
                img[
                    y_offset : y_offset + height_weather_logo,
                    x_offset : x_offset + width_weather_logo,
                ] = weather_logo

                cv.imwrite(f"weather_image/{day['date']}.jpg", img)
