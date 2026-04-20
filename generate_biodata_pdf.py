from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


OUTPUT = Path("Saurabh_Kumar_Biodata.pdf")
PHOTO = Path("Profile Photo.jfif")


class PremiumBiodataPDF:
    def __init__(self, output_path: Path):
        self.c = canvas.Canvas(str(output_path), pagesize=A4)
        self.w, self.h = A4
        self.margin = 30
        self.left = self.margin
        self.right = self.w - self.margin
        self.bottom_safe = self.margin + 26

    def wrap(self, text: str, font: str, size: float, width: float):
        words = text.split()
        lines = []
        current = ""

        for word in words:
            candidate = word if not current else f"{current} {word}"
            if self.c.stringWidth(candidate, font, size) <= width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines

    def draw_page_background(self):
        self.c.setFillColor(colors.HexColor("#f7f1e6"))
        self.c.rect(0, 0, self.w, self.h, stroke=0, fill=1)

        self.c.setFillColor(colors.HexColor("#efdfc9"))
        self.c.circle(46, self.h - 42, 94, stroke=0, fill=1)

        self.c.setFillColor(colors.HexColor("#e6d4b8"))
        self.c.circle(self.w - 18, 110, 112, stroke=0, fill=1)

        self.c.setStrokeColor(colors.HexColor("#cfb690"))
        self.c.setLineWidth(1)
        self.c.rect(16, 16, self.w - 32, self.h - 32, stroke=1, fill=0)

    def draw_header(self):
        banner_h = 148
        banner_y = self.h - self.margin - banner_h
        banner_w = self.right - self.left

        self.c.setFillColor(colors.HexColor("#7a4b2a"))
        self.c.roundRect(self.left, banner_y, banner_w, banner_h, 16, stroke=0, fill=1)

        self.c.setFillColor(colors.white)
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(self.left + 18, banner_y + 106, "Saurabh Kumar")

        self.c.setFont("Helvetica", 12)
        self.c.drawString(self.left + 18, banner_y + 84, "Senior Software Engineer | Family-Oriented | Tech Enthusiast")

        self.c.setFont("Helvetica-Oblique", 11)
        self.c.drawString(self.left + 18, banner_y + 62, "Building a meaningful life with values, ambition, and simplicity.")

        chips = ["Age 25", "5.9''", "Hindu, Suri", "Hindi, Maithili, English"]
        chip_x = self.left + 18
        chip_y = banner_y + 30
        for chip in chips:
            chip_w = self.c.stringWidth(chip, "Helvetica-Bold", 8.5) + 16
            self.c.setFillColor(colors.HexColor("#f5e8d5"))
            self.c.roundRect(chip_x, chip_y - 3, chip_w, 16, 8, stroke=0, fill=1)
            self.c.setFillColor(colors.HexColor("#5b371d"))
            self.c.setFont("Helvetica-Bold", 8.5)
            self.c.drawString(chip_x + 8, chip_y + 2, chip)
            chip_x += chip_w + 6

        if PHOTO.exists():
            try:
                image = ImageReader(str(PHOTO))
                frame_w = 106
                frame_h = 120
                frame_x = self.right - frame_w - 16
                frame_y = banner_y + 12
                self.c.setFillColor(colors.HexColor("#e8cfaa"))
                self.c.roundRect(frame_x - 5, frame_y - 5, frame_w + 10, frame_h + 10, 12, stroke=0, fill=1)
                self.c.drawImage(image, frame_x, frame_y, width=frame_w, height=frame_h, preserveAspectRatio=True, mask="auto")
            except Exception:
                pass

        return banner_y - 12

    def draw_card(self, x: float, y_top: float, width: float, title: str, rows, line_height=11.8):
        pad = 10
        title_h = 20
        text_w = width - (pad * 2) - 2

        wrapped_rows = []
        for row in rows:
            wrapped_rows.extend(self.wrap(row, "Helvetica", 9.6, text_w - 8))

        content_h = len(wrapped_rows) * line_height + 6
        card_h = pad + title_h + content_h + pad
        y0 = y_top - card_h

        self.c.setFillColor(colors.HexColor("#fffaf2"))
        self.c.setStrokeColor(colors.HexColor("#d8bf9c"))
        self.c.roundRect(x, y0, width, card_h, 9, stroke=1, fill=1)

        self.c.setFillColor(colors.HexColor("#f1dfc2"))
        self.c.roundRect(x + 1, y0 + card_h - title_h - 6, width - 2, title_h + 5, 8, stroke=0, fill=1)

        self.c.setFillColor(colors.HexColor("#5a3a1d"))
        self.c.setFont("Helvetica-Bold", 11.3)
        self.c.drawString(x + pad, y0 + card_h - 15, title)

        text = self.c.beginText()
        text.setTextOrigin(x + pad + 4, y0 + card_h - 31)
        text.setFont("Helvetica", 9.6)
        text.setFillColor(colors.HexColor("#32261b"))

        for line in wrapped_rows:
            text.textLine(f"- {line}")

        self.c.drawText(text)
        return y0 - 7

    def draw_footer(self):
        return

    def build(self):
        self.draw_page_background()
        start_y = self.draw_header()

        gutter = 10
        col_w = (self.right - self.left - gutter) / 2
        x_left = self.left
        x_right = x_left + col_w + gutter

        y_left = start_y
        y_right = start_y

        y_left = self.draw_card(
            x_left,
            y_left,
            col_w,
            "About Me",
            [
                "Saurabh Kumar, 25 years old, currently based in Kolkata.",
                "Grounded, calm, and family-oriented with modern outlook.",
                "Believes in trust, consistency, and mutual respect in marriage.",
                "Rooted in values and focused on building a meaningful life.",
            ],
        )

        y_left = self.draw_card(
            x_left,
            y_left,
            col_w,
            "Professional Details",
            [
                "Profession: Senior Software Engineer",
                "Company: Calsoft, Kolkata",
                "Experience: 4+ Years",
                "Education: B.Tech, IES College of Technology and Management, Bhopal",
                "Work style: Disciplined, sincere, and growth-oriented.",
            ],
        )

        y_left = self.draw_card(
            x_left,
            y_left,
            col_w,
            "Lifestyle and Interests",
            [
                "Food preference: Mixed",
                "Lifestyle: Balanced and health-conscious",
                "Hobbies: Travel, learning, and quality family time",
                "Instagram: @thesaurabhnayak",
            ],
        )

        y_right = self.draw_card(
            x_right,
            y_right,
            col_w,
            "Personal Snapshot",
            [
                "Date of Birth: 20/10/1999",
                "Height: 5.9''",
                "Religion: Hindu",
                "Caste: Suri",
                "Known Languages: Hindi, Maithili, English",
                "Native Place: Radhi, Darbhanga, Bihar",
                "Food Habit: Mixed",
            ],
        )

        y_right = self.draw_card(
            x_right,
            y_right,
            col_w,
            "Family Background",
            [
                "Father: Mr. Ram Naresh Nayak (Businessman)",
                "Mother: Mrs. Nitu Nayak (Anganwadi Sevika)",
                "Brother: Gaurav Kumar (Student)",
                "Family values: Respect, warmth, and togetherness.",
                "Facebook: thesaurabhnayak",
            ],
        )

        y_right = self.draw_card(
            x_right,
            y_right,
            col_w,
            "Partner Preferences",
            [
                "Looking for an understanding and supportive life partner.",
                "Values: Respectful, well-mannered, and positive mindset.",
                "Profession and background are flexible.",
                "Most important: Compatibility and shared values.",
            ],
        )

        self.draw_card(
            x_right,
            y_right,
            col_w,
            "Contact",
            [
                "Father Mobile / WhatsApp: +91 8002254088",
                "Families may connect directly for respectful discussion.",
            ],
        )

        self.draw_footer()
        self.c.save()


if __name__ == "__main__":
    PremiumBiodataPDF(OUTPUT).build()
    print(f"Created {OUTPUT.name}")
