import dearpygui.dearpygui as dpg
import ctypes
import draw
import xdialog
import json
import pyvips
import os
import random

ctypes.windll.shcore.SetProcessDpiAwareness(2)
dpg.create_context()
    
ELEMENTS = json.load(open("elements.json","r",encoding="utf-8"))["index"]

with dpg.font_registry():
    with dpg.font("SourceHanSansSC-Medium.otf", 50) as font:

        # add the default font range
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)

        # helper to add range of characters
        #    Options:
        #        mvFontRangeHint_Japanese
        #        mvFontRangeHint_Korean
        #        mvFontRangeHint_Chinese_Full
        #        mvFontRangeHint_Chinese_Simplified_Common
        #        mvFontRangeHint_Cyrillic
        #        mvFontRangeHint_Thai
        #        mvFontRangeHint_Vietnamese
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)

        # add specific range of glyphs
        dpg.add_font_range(0x3100, 0x3ff0)

        # add specific glyphs
        dpg.add_font_chars([0x3105, 0x3107, 0x3108])

        # remap や to %
        dpg.add_char_remap(0x3084, 0x0025)
        
def export_svg(sender):
    path = xdialog.save_file("导出", filetypes=[("矢量图", "*.svg")])
    core_number = dpg.get_value("core_number_input")
    orbits_text = dpg.get_value("orbits_input")
    orbits = []
    for line in orbits_text.split("\n"):
        if line.strip() != "":
            orbits.append(int(line.strip()))
    info = {
        "core_number":core_number,
        "orbits":orbits
    }
    diagram = draw.StructureDiagram(info)
    diagram.draw(path)
    xdialog.info("导出", "已导出到" + path)

        
with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("logo.png")
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="logo_texture_tag")
    
dpg.set_global_font_scale(0.5)
dpg.bind_font(font)

def show_structure_diagram(sender):
    dpg.enable_item("export_menu_item")
    dpg.show_item("structure_diagram_window")

def print_me(sender):
    print(f"Menu Item: {sender}")

with dpg.window(tag="Primary Window"):
    with dpg.menu_bar():
        with dpg.menu(label="文件"):
            dpg.add_menu_item(label="打开 (未完成)", callback=print_me, tag="open_menu_item",enabled=False)
            dpg.add_menu_item(label="保存 (未完成)", callback=print_me, tag="save_menu_item",enabled=False)
            dpg.add_menu_item(label="另存为 (未完成)", callback=print_me, tag="save_as_menu_item",enabled=False)
            dpg.add_menu_item(label="导出", callback=export_svg, tag="export_menu_item",enabled=False)

            with dpg.menu(label="新建"):
                dpg.add_menu_item(label="结构示意图", callback=show_structure_diagram, tag="new_structure_diagram_menu_item")
                dpg.add_menu_item(label="化学方程式 (未完成)", callback=print_me, tag="new_chemical_equation_menu_item",enabled=False)

        with dpg.menu(label="关于"):
            dpg.add_text("ChemBroad v1.0\n作者: Loshop Wu")
    

with dpg.window(tag="welcome_window", label="欢迎", width=430, height=200, pos=(300, 200),no_resize=True):
    dpg.add_image("logo_texture_tag",pos=(0,60),width=128,height=128)
    dpg.add_text("欢迎使用 ChemBroad！")

 
with dpg.window(tag="structure_diagram_window", label="配置", width=600, height=400, pos=(0, 0),no_close=True):
    dpg.hide_item("structure_diagram_window")
    def draw_structure_diagram():
        core_number = dpg.get_value("core_number_input")
        orbits_text = dpg.get_value("orbits_input")
        orbits = []
        for line in orbits_text.split("\n"):
            if line.strip() != "":
                orbits.append(int(line.strip()))
        info = {
            "core_number":core_number,
            "orbits":orbits
        }
        diagram = draw.StructureDiagram(info)
        svg_file_name = "preview.svg" + str(random.randint(0,1000))
        diagram.draw(svg_file_name)

        image = pyvips.Image.new_from_file(svg_file_name, dpi=200)
        image.write_to_file("preview.jpg",background=[255,255,255])
        os.remove(svg_file_name)
        
        with dpg.texture_registry():
            width, height, channels, data = dpg.load_image("preview.jpg")
            texture_tag = "preview_image_texture_tag" + str(random.randint(0,1000))
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=texture_tag)
            
        pic_width = dpg.get_item_width("Primary Window") - 100 / 2
        pic_height = pic_width * height / width
        pic_pos_x = dpg.get_item_width("Primary Window") - pic_width - 50
        pic_pos_y = dpg.get_item_height("Primary Window") / 2 - pic_height / 2
        dpg.delete_item("preview_image")
        dpg.add_image(texture_tag,tag="preview_image",parent="Primary Window",width=pic_width,height=pic_height,pos=(pic_pos_x,pic_pos_y))
    with dpg.item_handler_registry(tag="primary_window_resize_handler"):
        dpg.add_item_resize_handler(callback=draw_structure_diagram)
    dpg.bind_item_handler_registry("Primary Window", "primary_window_resize_handler")
    
    def switch_auto_generate(sender):
        if dpg.get_value(sender):
            dpg.disable_item("orbits_input")
            core_number = dpg.get_value("core_number_input")
            element = ELEMENTS[core_number - 1]
            orbits = ""
            for orbit in element:
                orbits += str(orbit) + "\n"
            dpg.set_value("orbits_input",orbits.strip())
        else:
            dpg.enable_item("orbits_input")
    def on_core_number_change(sender):
        if dpg.get_value("auto_generate_orbits_checkbox"):
            core_number = dpg.get_value(sender)
            element = ELEMENTS[core_number - 1]
            orbits = ""
            for orbit in element:
                orbits += str(orbit) + "\n"
            dpg.set_value("orbits_input",orbits.strip())
        draw_structure_diagram()
    dpg.add_text("核电荷数")
    dpg.add_input_int( default_value=8, min_value=1, max_value=118, tag="core_number_input",width=dpg.get_item_width("structure_diagram_window")-25,callback=on_core_number_change)
    dpg.add_checkbox(label="自动生成轨道", tag="auto_generate_orbits_checkbox", default_value=True,callback=switch_auto_generate)
    dpg.add_text("电子轨道")
    dpg.add_input_text(default_value="2\n6", tag="orbits_input",multiline=True,callback=draw_structure_diagram)

with dpg.item_handler_registry(tag="structure_diagram_window_resize_handler"):
    def set_width(sender):
        dpg.set_item_width("core_number_input",dpg.get_item_width("structure_diagram_window")-25)
        dpg.set_item_width("orbits_input",dpg.get_item_width("structure_diagram_window")-25)
    dpg.add_item_resize_handler(callback=set_width)
    

dpg.bind_item_handler_registry("structure_diagram_window", "structure_diagram_window_resize_handler")
dpg.create_viewport(title='ChemBroad', width=1000, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

dpg.start_dearpygui()
dpg.destroy_context()