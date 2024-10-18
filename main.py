import flet as ft
import display.setting.SettingScreen as setting
import display.conversion.conversionScreen as conversion
import display.live.liveScreen as setting
import display.capture.captureScreen as capture


def main(page: ft.page):
    page.add(conversion.screen())



if __name__ == '__main__':
    ft.app(target=main)


