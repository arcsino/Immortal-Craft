import customtkinter, json, sys, zipfile
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
from decimal import Decimal
from pathlib import Path
from PIL import Image


rp_name = None
rp_description = None
png_path = None
ogg_path = None
sound_volume = 0.2
format_version = None


def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / filename
    return Path(filename)


FONT_TYPE = "meiryo"

with open(resource_path("./json/format_version.json"), "r", encoding="utf-8") as f:
    FORMAT_VERSION_DICT = json.load(f)
with open(resource_path("./json/help_text.json"), "r", encoding="utf-8") as f:
    TEXT_DICT = json.load(f)


class MyLabelFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, content, level, height, image=None):
        super().__init__(master, fg_color="white")

        self.title = title
        self.content = content
        self.level = level
        self.height = height
        self.image = image
        self.grid_columnconfigure(0, weight=1)

        # label
        self.label = customtkinter.CTkLabel(
            self,
            text=self.title,
            corner_radius=6,
            fg_color="#ffa899",
            font=customtkinter.CTkFont(size=8 * self.level, weight="bold"),
            justify="left",
        )
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # textbox
        self.textbox = customtkinter.CTkTextbox(
            self,
            height=self.height,
            fg_color="transparent",
            font=customtkinter.CTkFont(FONT_TYPE, size=14),
            activate_scrollbars=False,
        )
        self.textbox.insert("0.0", self.content)
        self.textbox.configure(state="disabled")
        self.textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # image label
        self.image_label = customtkinter.CTkLabel(
            self,
            text="",
            corner_radius=6,
            font=customtkinter.CTkFont(FONT_TYPE, size=12),
            image=self.image,
            justify="left",
        )
        if not self.image == None:
            self.image_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")


class MyEntryFrame(MyLabelFrame):
    def __init__(self, master, title, content, placeholder, level, height):
        super().__init__(master, title, content, level, height)

        self.placeholder = placeholder

        # entry
        self.entry = customtkinter.CTkEntry(
            self,
            placeholder_text=self.placeholder,
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
        )
        self.entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")


class MyFileDialogFrame(MyLabelFrame):
    def __init__(self, master, title, content, level, height, file_type):
        super().__init__(master, title, content, level, height)

        self.file_type = file_type

        # "button and textbox" frame
        self.frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        # textbox of path (in the "button and textbox" frame)
        self.pathbox = customtkinter.CTkTextbox(
            self.frame,
            height=70,
            border_width=2,
            fg_color="#F9F9FA",
            border_color="#979DA2",
            font=customtkinter.CTkFont(FONT_TYPE, size=12),
        )
        self.pathbox.configure(state="disabled")
        self.pathbox.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="ew")

        # ask open file button (in the "button and textbox" frame)
        self.button = customtkinter.CTkButton(
            self.frame,
            width=32,
            corner_radius=8,
            text_color="gray10",
            text=TEXT_DICT["make_filedialog"],
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
            command=self.click_event,
            anchor="center",
        )
        self.button.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="nsew")

    def click_event(self):
        global png_path, ogg_path

        # file type "icon"
        if self.file_type == "icon":
            png_path = Path(
                filedialog.askopenfilename(
                    defaultextension="png",
                    filetypes=[("PNG", ".png")],
                    initialdir=Path.cwd(),
                )
            )
            # update pathbox
            self.pathbox.configure(state="normal")
            self.pathbox.delete("0.0", "end")
            self.pathbox.insert("0.0", png_path)
            self.pathbox.configure(state="disabled")

            # update image label
            self.image_label.configure(
                image=customtkinter.CTkImage(Image.open(png_path), size=(100, 100))
            )
            self.image_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # file type "ogg"
        if self.file_type == "ogg":
            ogg_path = [
                Path(op)
                for op in list(
                    filedialog.askopenfilenames(
                        defaultextension="ogg",
                        filetypes=[("OGG", ".ogg")],
                        initialdir=Path.cwd(),
                    )
                )
            ]
            # update pathbox
            self.pathbox.configure(state="normal")
            self.pathbox.delete("0.0", "end")
            self.pathbox.insert("0.0", ogg_path)
            self.pathbox.configure(state="disabled")

            # update image label
            self.image_label.configure(
                text="\n".join(["・" + op.name for op in ogg_path]), fg_color="gray90"
            )
            self.image_label.grid(row=2, column=0, padx=10, pady=(0, 10))


class MyVolumeFrame(MyLabelFrame):
    def __init__(self, master, title, content, level, height):
        super().__init__(master, title, content, level, height)

        # "entry and buttons" frame
        self.frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.frame.columnconfigure((0, 2), weight=0)
        self.frame.columnconfigure(1, weight=1)
        self.frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

        # minus button (in the "entry and buttons" frame)
        self.minus_button = customtkinter.CTkButton(
            self.frame,
            width=30,
            corner_radius=8,
            text_color="gray10",
            text="-",
            command=self.minus_button_event,
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
        )
        self.minus_button.grid(row=0, column=0, padx=(0, 5), pady=0)

        # entry (in the "entry and buttons" frame)
        self.entry = customtkinter.CTkEntry(
            self.frame,
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
        )
        self.entry.insert(0, "0.2")
        self.entry.configure(state="disabled")
        self.entry.grid(row=0, column=1, columnspan=1, padx=0, pady=0, sticky="ew")

        # plus button (in the "entry and buttons" frame)
        self.plus_button = customtkinter.CTkButton(
            self.frame,
            width=30,
            corner_radius=8,
            text_color="gray10",
            text="+",
            command=self.plus_button_event,
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
        )
        self.plus_button.grid(row=0, column=2, padx=(5, 0), pady=0)

    def minus_button_event(self):
        global sound_volume

        sound_volume = float(Decimal(self.entry.get()) - Decimal("0.1"))
        self.update_entry(str(sound_volume))
        self.check_button_state(sound_volume)

    def plus_button_event(self):
        global sound_volume

        sound_volume = float(Decimal(self.entry.get()) + Decimal("0.1"))
        self.update_entry(str(sound_volume))
        self.check_button_state(sound_volume)

    def update_entry(self, text):
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.insert(0, text)
        self.entry.configure(state="disabled")

    def check_button_state(self, volume):
        if volume == 0.0:
            self.minus_button.configure(state="disabled")
        elif volume == 1.0:
            self.plus_button.configure(state="disabled")
        else:
            self.plus_button.configure(state="normal")
            self.minus_button.configure(state="normal")


class MyOptionMenuFrame(MyLabelFrame):
    def __init__(self, master, title, content, level, height, options):
        super().__init__(master, title, content, level, height)

        self.options = options

        # option menu
        self.optionmenu = customtkinter.CTkOptionMenu(
            self,
            fg_color="gray90",
            button_color="#FF6347",
            button_hover_color="#cc4f39",
            dropdown_fg_color="white",
            dropdown_hover_color="#FF6347",
            values=self.options,
            text_color="gray10",
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
            dropdown_font=customtkinter.CTkFont(FONT_TYPE, size=12),
        )
        self.optionmenu.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title(TEXT_DICT["title"])
        self.geometry("1000x600")
        self.minsize(width=700, height=400)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # image
        self.home_image = customtkinter.CTkImage(
            Image.open(resource_path("./img/bgmrp_wp.png")), size=(420, 210)
        )

        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme(resource_path("./json/custom_theme.json"))

        # nav frame
        self.nav_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="gray80"
        )
        self.nav_frame.grid(row=0, column=0, sticky="nsew")

        # title label (in the nav frame)
        self.nav_frame_label = customtkinter.CTkLabel(
            self.nav_frame,
            text=TEXT_DICT["title"],
            font=customtkinter.CTkFont(FONT_TYPE, size=16, weight="bold"),
        )
        self.nav_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # home button (in the nav frame)
        self.nav_home_button = customtkinter.CTkButton(
            self.nav_frame,
            height=40,
            corner_radius=0,
            border_spacing=10,
            fg_color="transparent",
            hover_color="#cc4f39",
            text_color="gray10",
            text=TEXT_DICT["nav_home"],
            font=customtkinter.CTkFont(FONT_TYPE, size=14),
            command=self.home_button_event,
            anchor="w",
        )
        self.nav_home_button.grid(row=1, column=0, padx=0, sticky="ew")

        # make button (in the nav frame)
        self.nav_make_button = customtkinter.CTkButton(
            self.nav_frame,
            height=40,
            corner_radius=0,
            border_spacing=10,
            fg_color="transparent",
            hover_color="#cc4f39",
            text_color="gray10",
            text=TEXT_DICT["nav_make"],
            font=customtkinter.CTkFont(FONT_TYPE, size=14),
            command=self.make_button_event,
            anchor="w",
        )
        self.nav_make_button.grid(row=2, column=0, padx=0, sticky="ew")

        # help button (in the nav frame)
        self.nav_help_button = customtkinter.CTkButton(
            self.nav_frame,
            height=40,
            corner_radius=0,
            border_spacing=10,
            fg_color="transparent",
            hover_color="#cc4f39",
            text_color="gray10",
            text=TEXT_DICT["nav_help"],
            font=customtkinter.CTkFont(FONT_TYPE, size=14),
            command=self.help_button_event,
            anchor="w",
        )
        self.nav_help_button.grid(row=3, column=0, padx=0, sticky="ew")

        # home frame
        self.home_frame = customtkinter.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.home_frame.grid_columnconfigure(0, weight=1)

        # label frame 0 (in the home frame)
        self.home_label_frame_0 = MyLabelFrame(
            self.home_frame,
            title=TEXT_DICT["home_title"],
            content=TEXT_DICT["home_title_content"],
            level=3,
            height=100,
            image=self.home_image,
        )
        self.home_label_frame_0.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # label frame 1 (in the home frame)
        self.home_label_frame_1 = MyLabelFrame(
            self.home_frame,
            title=TEXT_DICT["home_version"],
            content=TEXT_DICT["home_version_content"],
            level=2,
            height=125,
        )
        self.home_label_frame_1.grid(
            row=1, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        # make frame
        self.make_frame = customtkinter.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.make_frame.grid_columnconfigure(0, weight=1)

        # entry frame 0 (in the make frame)
        self.make_entry_frame_0 = MyEntryFrame(
            self.make_frame,
            title=TEXT_DICT["make_name_title"],
            content=TEXT_DICT["make_name_content"],
            placeholder=TEXT_DICT["make_name_placeholder"],
            level=2,
            height=25,
        )
        self.make_entry_frame_0.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # entry frame 1 (in the make frame)
        self.make_entry_frame_1 = MyEntryFrame(
            self.make_frame,
            title=TEXT_DICT["make_description_title"],
            content=TEXT_DICT["make_description_content"],
            placeholder=TEXT_DICT["make_description_placeholder"],
            level=2,
            height=25,
        )
        self.make_entry_frame_1.grid(
            row=1, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        # filedialog frame 0 (in the make frame)
        self.make_filedialog_frame_0 = MyFileDialogFrame(
            self.make_frame,
            title=TEXT_DICT["make_icon_title"],
            content=TEXT_DICT["make_icon_content"],
            level=2,
            height=60,
            file_type="icon",
        )
        self.make_filedialog_frame_0.grid(
            row=2, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        # filedialog frame 1 (in the make frame)
        self.make_filedialog_frame_1 = MyFileDialogFrame(
            self.make_frame,
            title=TEXT_DICT["make_sounds_title"],
            content=TEXT_DICT["make_sounds_content"],
            level=2,
            height=60,
            file_type="ogg",
        )
        self.make_filedialog_frame_1.grid(
            row=3, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        # volume frame (in the make frame)
        self.make_volume_frame_0 = MyVolumeFrame(
            self.make_frame,
            title=TEXT_DICT["make_volume_title"],
            content=TEXT_DICT["make_volume_content"],
            level=2,
            height=25,
        )
        self.make_volume_frame_0.grid(
            row=4, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        # option menu frame (in the make frame)
        self.make_optionmenu_frame_0 = MyOptionMenuFrame(
            self.make_frame,
            title=TEXT_DICT["make_version_title"],
            content=TEXT_DICT["make_version_content"],
            level=2,
            height=25,
            options=[
                "1.21.5",
                "1.21.4",
                "1.21-1.21.3",
                "1.20.5-1.21.6",
                "1.20.3-1.20.4",
                "1.20.2",
                "1.20-1.20.1",
            ],
        )
        self.make_optionmenu_frame_0.grid(
            row=5, column=0, padx=10, pady=(0, 10), sticky="ew"
        )

        # save button (in the make frame)
        self.make_save_button = customtkinter.CTkButton(
            self.make_frame,
            height=48,
            corner_radius=8,
            text_color="gray10",
            text=TEXT_DICT["make_save_button"],
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
            command=self.save_button_event,
        )
        self.make_save_button.grid(row=6, column=0, padx=10, pady=(20, 30), sticky="ew")

        # help frame
        self.help_frame = customtkinter.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.help_frame.grid_columnconfigure(0, weight=1)

        # help label frame 0 (in the help frame)
        self.help_label_frame_0 = MyLabelFrame(
            self.help_frame,
            title=TEXT_DICT["help_ogg_title"],
            content=TEXT_DICT["help_ogg_content"],
            level=2,
            height=175,
        )
        self.help_label_frame_0.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.nav_home_button.configure(
            fg_color="#ff6347" if name == "home" else "transparent"
        )
        self.nav_make_button.configure(
            fg_color="#ff6347" if name == "make" else "transparent"
        )
        self.nav_help_button.configure(
            fg_color="#ff6347" if name == "help" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "make":
            self.make_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.make_frame.grid_forget()
        if name == "help":
            self.help_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.help_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def make_button_event(self):
        self.select_frame_by_name("make")

    def help_button_event(self):
        self.select_frame_by_name("help")

    def check_value(self):
        global rp_name, rp_description, png_path, ogg_path, sound_volume, format_version, filename

        rp_name = self.make_entry_frame_0.entry.get()
        rp_description = self.make_entry_frame_1.entry.get()
        format_version = FORMAT_VERSION_DICT[
            self.make_optionmenu_frame_0.optionmenu.get()
        ]

        # empty error
        value_list = [rp_name, rp_description, png_path, ogg_path]
        for i, value in enumerate(value_list):
            if not value:
                raise Exception(TEXT_DICT[f"empty_error_{i}"])

    def make_rp(self):
        global rp_name, rp_description, png_path, ogg_path, sound_volume, format_version, filename

        filename = Path(
            filedialog.asksaveasfilename(
                defaultextension="zip",
                filetypes=[("ZIP", ".zip")],
                initialdir=Path.cwd(),
                initialfile=rp_name + ".zip",
            )
        )
        if filename.exists():
            filename.unlink(missing_ok=True)

        # *.zip
        with zipfile.ZipFile(
            filename,
            "a",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as zf:
            # pack.mcmeta
            with zf.open("pack.mcmeta", "w") as f:
                obj = {
                    "pack": {
                        "pack_format": format_version,
                        "supported_formats": [format_version, format_version],
                        "description": rp_description,
                    }
                }
                f.write(json.dumps(obj).encode("utf-8"))
            # sounds.json
            with zf.open("assets/minecraft/sounds.json", "w") as f:
                s_list = []
                for i in range(len(ogg_path)):
                    s_list.append(
                        {
                            "name": "bgm/" + str(i),
                            "volume": sound_volume,
                            "stream": True,
                        }
                    )
                obj = {"bgm.1": {"sounds": s_list}}
                f.write(json.dumps(obj).encode("utf-8"))
            # pack.png
            zf.write(png_path, arcname="pack.png")
            # *.ogg
            for i, op in enumerate(ogg_path):
                zf.write(op, arcname=f"assets/minecraft/sounds/bgm/{i}.ogg")
        # show info
        CTkMessagebox(
            title="Info",
            message=str(TEXT_DICT["saved_info"]).replace("<filename>", filename.name),
            font=customtkinter.CTkFont(FONT_TYPE, size=16),
        )

    def save_button_event(self):
        try:
            self.check_value()
            self.make_rp()

        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=e,
                icon="cancel",
                font=customtkinter.CTkFont(FONT_TYPE, size=16),
            )


if __name__ == "__main__":
    app = App()
    app.mainloop()
