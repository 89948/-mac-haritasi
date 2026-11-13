from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


Window.clearcolor = (0.03, 0.10, 0.16, 1)


class MacHaritasiApp(App):
    def build(self):
        self.title = "Maç Haritası"
        self.alanlar = {}

        kaydirma = ScrollView()

        ekran = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10),
            size_hint_y=None,
        )
        ekran.bind(minimum_height=ekran.setter("height"))

        ekran.add_widget(
            Label(
                text="MAÇ HARİTASI",
                font_size="24sp",
                color=(0.85, 0.73, 0.36, 1),
                size_hint_y=None,
                height=dp(55),
            )
        )

        bilgiler = [
            ("mac", "Maç adı", "", "Takım A - Takım B"),
            (
                "tarih",
                "Tarih — gün/ay/yıl",
                datetime.now().strftime("%d/%m/%Y"),
                "13/11/2026",
            ),
            ("saat", "Başlama saati", "20:00", "20:00"),
            ("sehir", "Maçın oynanacağı şehir", "", "Şehir"),
            (
                "utc",
                "Maç yerinin UTC farkı — o tarih için",
                "+03:00",
                "+03:00 veya +01:00",
            ),
            ("enlem", "Enlem", "", "Örnek: 39.77"),
            ("boylam", "Boylam", "", "Örnek: 30.52"),
        ]

        for anahtar, baslik, deger, ipucu in bilgiler:
            ekran.add_widget(
                Label(
                    text=baslik,
                    color=(0.92, 0.94, 0.97, 1),
                    size_hint_y=None,
                    height=dp(28),
                )
            )

            alan = TextInput(
                text=deger,
                hint_text=ipucu,
                multiline=False,
                size_hint_y=None,
                height=dp(48),
                font_size="17sp",
                padding=[dp(10), dp(12)],
                background_normal="",
                background_active="",
                background_color=(0.10, 0.19, 0.26, 1),
                foreground_color=(1, 1, 1, 1),
                cursor_color=(0.85, 0.73, 0.36, 1),
            )

            self.alanlar[anahtar] = alan
            ekran.add_widget(alan)

        dugme = Button(
            text="Bilgileri kontrol et",
            size_hint_y=None,
            height=dp(54),
            background_normal="",
            background_color=(0.75, 0.61, 0.25, 1),
            color=(0.04, 0.09, 0.13, 1),
            font_size="18sp",
        )
        dugme.bind(on_release=self.kontrol_et)
        ekran.add_widget(dugme)

        self.sonuc = Label(
            text=(
                "İlk sürüm: Bilgi giriş ekranı.\n"
                "Harita hesaplaması henüz eklenmedi."
            ),
            color=(0.92, 0.94, 0.97, 1),
            size_hint_y=None,
            halign="center",
            valign="middle",
            padding=(dp(5), dp(12)),
        )
        self.sonuc.bind(
            width=lambda nesne, genislik: setattr(
                nesne, "text_size", (genislik, None)
            ),
            texture_size=lambda nesne, boyut: setattr(
                nesne, "height", boyut[1] + dp(24)
            ),
        )

        ekran.add_widget(self.sonuc)
        kaydirma.add_widget(ekran)
        return kaydirma

    def kontrol_et(self, _):
        veri = {
            anahtar: alan.text.strip()
            for anahtar, alan in self.alanlar.items()
        }

        try:
            if not veri["mac"]:
                raise ValueError("Maç adını yazın.")

            if not veri["sehir"]:
                raise ValueError("Maçın oynanacağı şehri yazın.")

            datetime.strptime(
                veri["tarih"] + " " + veri["saat"],
                "%d/%m/%Y %H:%M",
            )

            # UTC farkını da doğrula.
            datetime.strptime(
                veri["tarih"] + " " + veri["saat"] + " " + veri["utc"],
                "%d/%m/%Y %H:%M %z",
            )

            enlem = float(veri["enlem"].replace(",", "."))
            boylam = float(veri["boylam"].replace(",", "."))

            if not -90 < enlem < 90:
                raise ValueError("Enlem -90 ile 90 arasında olmalı.")

            if not -180 <= boylam <= 180:
                raise ValueError("Boylam -180 ile 180 arasında olmalı.")

        except ValueError as hata:
            self.sonuc.text = (
                "Bilgiler kontrol edilemedi.\n"
                "Tarih: 13/11/2026\n"
                "Saat: 20:00 | UTC farkı: +03:00\n"
                "Koordinatlar sayı olmalı.\n\n"
                f"Ayrıntı: {hata}"
            )
            return

        self.sonuc.text = (
            "Bilgiler uygun.\n\n"
            f"{veri['mac']}\n"
            f"{veri['tarih']} — {veri['saat']}\n"
            f"{veri['sehir']} | UTC {veri['utc']}\n"
            f"Konum: {enlem:.4f}, {boylam:.4f}\n\n"
            "Harita hesaplaması sonraki aşamada eklenecek."
        )


if __name__ == "__main__":
    MacHaritasiApp().run()
