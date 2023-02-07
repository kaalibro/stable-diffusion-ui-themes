import os
import re
import gradio as gr
from modules import script_callbacks
from modules import shared, scripts
import modules.scripts as scripts

accents = [
    "rosewater",
    "flamingo",
    "pink",
    "mauve",
    "red",
    "maroon",
    "peach",
    "yellow",
    "green",
    "teal",
    "sky",
    "blue",
    "sapphire",
    "lavender",
]
themes = ["Latte", "Frappe", "Macchiato", "Mocha", "OneDark", "Civitai"]
script_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def on_ui_settings():
    section = ("uit", "UI Theme")
    shared.opts.add_option(
        "uit_theme",
        shared.OptionInfo(
            default="Mocha",
            label="Theme",
            component=gr.Radio,
            component_args={"choices": themes},
            onchange=on_ui_settings_change,
            section=section,
        ),
    )

    shared.opts.add_option(
        "accent_color",
        shared.OptionInfo(
            default="blue",
            label="Accent",
            component=gr.Radio,
            component_args={"choices": accents},
            onchange=on_accent_color_change,
            section=section,
        ),
    )


def on_accent_color_change():
    pattern = re.compile(r"--accent:\s*(.*)")
    # Replace the accent color
    with open(os.path.join(script_path, "style.css"), "r+") as file:
        text = re.sub(
            pattern,
            f"--accent: var(--{shared.opts.accent_color});",
            file.read(),
            count=1,
        )
        file.seek(0)
        file.write(text)
        file.truncate()


def on_ui_settings_change():
    style_theme = os.path.join(script_path, f"themes/{shared.opts.uit_theme}.css")
    style_common = os.path.join(script_path, "themes/styles-common.css")
    with open(style_theme, "r+") as f1, open(style_common, "r+") as f2, open(
        os.path.join(script_path, "style.css"), "w"
    ) as file:
        file.write(f1.read())
        file.write(f2.read())

    # Reappply accent color
    on_accent_color_change()


script_callbacks.on_ui_settings(on_ui_settings)
