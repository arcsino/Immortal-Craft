from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox
import json, tkinter, zipfile


rp_name = ""
rp_description = ""
png_path = ""
ogg_path = []
save_path = ""


class PartsGroup:
    def __init__(
        self,
        lbl_frm=None,
        lbl_txt=None,
        lbl_w=None,
        lbl_anchor=None,
        entry_frm=None,
        btn_frm=None,
        btn_txt=None,
        btn_w=None,
        btn_cmd=None,
    ):
        self.label = tkinter.Label(
            lbl_frm, text=lbl_txt, width=lbl_w, anchor=lbl_anchor
        )
        self.entry = tkinter.Entry(entry_frm, width=59, bg="#dddddd")
        self.btn = tkinter.Button(
            btn_frm,
            text=btn_txt,
            width=btn_w,
            height=1,
            bg="#dddddd",
            command=btn_cmd,
        )

    def place_lbl(self, x, y):
        self.label.place(x=x, y=y)

    def place_entry(self, x, y):
        self.entry.place(x=x, y=y)

    def place_btn(self, x, y):
        self.btn.place(x=x, y=y)


def check_entry():
    global rp_name, rp_description, png_path, ogg_path, save_path

    rp_name = parts[0].entry.get()
    rp_description = parts[1].entry.get()
    png_path = parts[2].entry.get()
    ogg_path = [Path(fp) for fp in json.loads(parts[3].entry.get())]
    save_path = parts[4].entry.get()

    entry_list = [rp_name, rp_description, png_path, ogg_path, save_path]
    empty_errors = [
        "名前を入力してください。",
        "説明を入力してください。",
        "アイコンを選択してください。",
        "音声ファイルを選択してください。",
        "保存先を選択してください。",
    ]
    for entry, error in zip(entry_list, empty_errors):
        if entry == "" or entry == [Path(".")]:
            raise Exception(error)

    if Path(f"{save_path}/{rp_name}.zip").exists():
        raise Exception(f'既に"{rp_name}"という名前のファイルが存在します。')


def make_rp():
    global rp_name, rp_description, png_path, ogg_path, save_path
    # *.zip
    with zipfile.ZipFile(
        f"{save_path}/{rp_name}.zip",
        "a",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as zf:

        # pack.mcmeta
        with zf.open("pack.mcmeta", "w") as f:
            obj = {
                "pack": {
                    "pack_format": 46,
                    "supported_formats": [46, 46],
                    "description": rp_description,
                }
            }
            f.write(json.dumps(obj).encode("utf-8"))

        # sounds.json
        with zf.open("assets/minecraft/sounds.json", "w") as f:
            s_list = []
            for i in range(len(ogg_path)):
                s_list.append({"name": "bgm/" + str(i), "stream": True})
            obj = {"bgm.1": {"sounds": s_list}}
            f.write(json.dumps(obj).encode("utf-8"))

        # pack.png
        zf.write(png_path, arcname="pack.png")

        # *.ogg
        for i, fp in enumerate(ogg_path):
            zf.write(fp, arcname=f"assets/minecraft/sounds/bgm/{i}.ogg")


def click_btn_2():
    path = filedialog.askopenfilename(initialdir=Path.cwd())
    parts[2].entry.delete(0, tkinter.END)
    parts[2].entry.insert(tkinter.END, path)


def click_btn_3():
    ogg_files = list(filedialog.askopenfilenames(initialdir=Path.cwd()))
    parts[3].entry.delete(0, tkinter.END)
    parts[3].entry.insert(tkinter.END, json.dumps(ogg_files))


def click_btn_4():
    path = filedialog.askdirectory(initialdir=Path.cwd())
    parts[4].entry.delete(0, tkinter.END)
    parts[4].entry.insert(tkinter.END, path)


def click_btn_5():
    global rp_name
    try:
        check_entry()
        make_rp()
        parts[5].label["text"] = datetime.now().strftime(
            f"(%Y/%m/%d %H:%M:%S) Saved Bgm RP as {rp_name}.zip"
        )
        messagebox.showinfo(
            "INFO", f'リソースパックを"{rp_name}.zip"として保存しました。'
        )
    except Exception as e:
        parts[5].label["text"] = e
        messagebox.showerror("ERROR", e)


root = tkinter.Tk()
root.title("Bgm RP Maker")
root.geometry("600x300")
root.resizable(False, False)

frame_w = tkinter.Frame(root, width=150, height=300, bg="gray", padx=20)
frame_e = tkinter.Frame(root, width=450, height=300, bg="white", padx=20)
frame_w.place(x=0, y=0)
frame_e.place(x=150, y=0)

parts = [
    PartsGroup(
        lbl_frm=frame_w,
        lbl_txt="名前：",
        lbl_w=15,
        lbl_anchor=tkinter.E,
        entry_frm=frame_e,
    ),
    PartsGroup(
        lbl_frm=frame_w,
        lbl_txt="説明：",
        lbl_w=15,
        lbl_anchor=tkinter.E,
        entry_frm=frame_e,
    ),
    PartsGroup(
        lbl_frm=frame_w,
        lbl_txt="アイコン(.png)：",
        lbl_w=15,
        lbl_anchor=tkinter.E,
        entry_frm=frame_e,
        btn_frm=frame_e,
        btn_txt="参照",
        btn_w=5,
        btn_cmd=click_btn_2,
    ),
    PartsGroup(
        lbl_frm=frame_w,
        lbl_txt="音声ファイル(.ogg)：",
        lbl_w=15,
        lbl_anchor=tkinter.E,
        entry_frm=frame_e,
        btn_frm=frame_e,
        btn_txt="参照",
        btn_w=5,
        btn_cmd=click_btn_3,
    ),
    PartsGroup(
        lbl_frm=frame_w,
        lbl_txt="保存先：",
        lbl_w=15,
        lbl_anchor=tkinter.E,
        entry_frm=frame_e,
        btn_frm=frame_e,
        btn_txt="参照",
        btn_w=5,
        btn_cmd=click_btn_4,
    ),
    PartsGroup(
        lbl_frm=frame_e,
        lbl_txt="version:0.0.1",
        btn_frm=frame_e,
        btn_txt="作成",
        btn_w=50,
        btn_cmd=click_btn_5,
    ),
]

# place parts
for i in range(len(parts)):
    if 0 <= i <= 4:
        parts[i].place_lbl(x=0, y=20 + 40 * i)
        parts[i].place_entry(x=0, y=20 + 40 * i)
        if i >= 2:
            parts[i].place_btn(x=365, y=16 + 40 * i)
    if i == 5:
        parts[i].place_btn(x=0, y=220)
        parts[i].place_lbl(x=0, y=262)

root.mainloop()
