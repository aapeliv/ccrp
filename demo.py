import argparse
from datetime import datetime, timezone

from ccrp import hacky
from ccrp.commands import compressed_char_width
from images import ccrp as ccrp_data


def local_now():
    return datetime.now(tz=timezone.utc).astimezone().strftime("%A %d/%m/%y, %H:%M %Z")


def nice_heading(p, *, title=None, subtitle="", include_local_time=True):
    if title:
        p.font(bold=True, double_height=True, double_width=True)
        p.align("center")
        p.line(title)
        p.feed(1)

    if include_local_time:
        p.font(compressed=True)
        p.align("left")
        w = compressed_char_width
        if len(subtitle) > w:
            p.line(subtitle)
            subtitle = ""
        else:
            p.text(subtitle)
        if include_local_time:
            p.line(f"{local_now(): >{w-len(subtitle)}}")
        p.feed(2)

    p.font()
    p.align("left")


def demo_form(p):
    c = ""
    compress_fields = True
    p.reset()
    p.print_bits_bitmap(ccrp_data.bits, ccrp_data.width, ccrp_data.height)
    nice_heading(p)

    def line(text):
        p.font(compressed=compress_fields)
        p.line(f"{text}{c}")
        # width is 24
        p.font(double_width=True)
        p.raw([0xC4] * 24)
        p.feed(2)

    def checkboxes(text, options, own_lines=False):
        p.font(compressed=compress_fields)
        p.line(f"{text}{c}")
        p.font(compressed=True)
        length = 3 + 7 * len(options) + sum(map(len, options))
        if own_lines or length > 64:
            for option in options:
                p.text("    ")
                p.checkbox(compressed=True)
                p.line(f" {option}")
        else:
            p.text("   ")
            for option in options:
                p.text("    ")
                p.checkbox(compressed=True)
                p.text(f" {option}")
            p.line("")
        # p.feed(1)

    def textbox(text, lines=3):
        p.font(compressed=compress_fields)
        p.line(f"{text}{c}")
        p.font(double_width=True, double_height=True)
        p.raw([0xDA] + [0xC4] * 22 + [0xBF])
        p.lf()
        for _ in range(lines):
            p.raw([0xB3] + [0x20] * 22 + [0xB3])
            p.lf()
        p.raw([0xC0] + [0xC4] * 22 + [0xD9])
        p.lf()
        # p.feed(1)

    line("First Name")
    line("Last Name")
    checkboxes("Check one", ["Yes", "No", "Maybe"])

    textbox("Comments")

    p.font(compressed=True)
    p.align("center")

    p.std_cut(lines=4)


def demo_bit_of_everything(p):
    p.reset()

    p.font()
    p.align("left")
    p.text("This is just simple text, when you go over the line length it will wrap and might break mid-word.")
    p.lf_cr()

    p.font(compressed=True)
    p.text("This is 'compressed' text")
    p.lf_cr()

    p.font(compressed=True)
    p.align("right")
    p.text("This is compresed and right-aligned")
    p.lf_cr()

    p.font(bold=True, double_height=True, double_width=True)
    p.align("center")
    p.text("Centered, bold, double height/width text.")
    p.lf_cr()

    p.font(compressed=True)
    p.align("left")
    p.text("Back to normal")
    p.lf_cr()

    # reset fonts
    p.font()
    p.align("center")

    p.code128("https://example.com", text_compressed=True, text_below=True)
    p.lf_cr()

    p.qr_code("https://www.aapelivuorinen.com", err_level="H")
    p.lf_cr()

    p.data_matrix("Some text in data matrix format")
    p.lf_cr()

    p.text("Bitmap:")
    p.lf_cr()
    p.print_bits_bitmap(ccrp_data.bits, ccrp_data.width, ccrp_data.height)
    p.lf_cr()

    p.std_cut()

    print("done")


if __name__ == "__main__":
    funcs = {"demo_form": demo_form, "demo_bit_of_everything": demo_bit_of_everything}

    parser = argparse.ArgumentParser(description="ccrp cli")
    parser.add_argument("command", type=str, choices=funcs.keys(), help="Command to execute")
    args = parser.parse_args()

    p = hacky.get_hacky_volcora()

    func = funcs.get(args.command)
    if func:
        func(p)
    else:
        raise Exception("Unknown command")
