import drawsvg as draw
import math

class StructureDiagram:
    def __init__(self,info:str | None=None):
        if info is not None:
            self.core = info["core_number"]
            self.orbits = info["orbits"]
            self.oebits_count = len(info["orbits"])
        else:
            self.core = 0
            self.orbits = []
            self.oebits_count = 0
        print("StructureDiagram initialized with core:", self.core, "orbits:", self.orbits)
            
    def draw(self, path=None):
        d = draw.Drawing(250, 180, origin='center')
        
        #画原子核电荷数
        core_text = "+" + str(self.core)
        match len(core_text):
            case 2:
                text_x = -59
            case 3:
                text_x = -63
            case 4:
                text_x = -67

        d.append(draw.Circle(-50,0,20,fill='none', stroke='black', stroke_width=2))
        d.append(draw.Text(core_text, 17, text_x, 6, fill='black', font_family='Times New Roman'))

        #画轨道
        for i in range(self.oebits_count):
            r = 60 + i * 15
            rad = math.asin(7.5 / r) / math.pi * 180
            d.append(draw.Arc(-75, 0, r, 15, rad, cw=False, stroke='black', stroke_width=2, fill='none'))
            d.append(draw.Arc(-75, 0, r, - rad, -15, cw=False, stroke='black', stroke_width=2, fill='none'))
        for i in range(self.oebits_count):
            text = str(self.orbits[i])
            text_x = -19 + i * 15
            match len(text):
                case 1:
                    text_x += 0
                case 2:
                    text_x += -3
            d.append(draw.Text(text, 15, text_x, 5, fill='black', font_family='Times New Roman'))
            
        d.set_pixel_scale(2)
        if path == None:
            return d
        d.save_svg(path)
        return None
        
