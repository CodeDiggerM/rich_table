from .color_map import COLOR_MAP
from st_aggrid import AgGrid, ColumnsAutoSizeMode,JsCode

class richTable(object):
    COMPARE_COLOR_MAP_FILE = 'color_map.config'
    js_cell_code = """function(params) {
                                    colors = {color_map};
                                    level = parseFloat(params.data.{col});
                                    if ((isNaN(params.data.{col}) == false || params.data.{col}.toString().includes("%") || params.data.{col}.toString().includes("."))&& isNaN(level) == false  ) {
                                        index = Math.floor((level - {min_val}) * {scales} / ({max_val} - {min_val}));
                                        index = Math.min(index, {scales} - 1);
                                        return {
                                            'color': 'black',
                                            'backgroundColor': colors[index]}
                                }
                            }
                            """
                            
    def __init__(self,data,
                 header_conf={},
                 index_cols=[],
                 pinned_cols=[],
                 color_map_file='',
                 backgroundColor='white',
                 fontWeight='bold',
                 key=None,
                 color='black'):
        color_map = self.load_color_map_file(color_map_file)
        if color_map is None:
            self.color_map = self.load_color_map()
        else:
            self.color_map = color_map
        self.data = data.copy()
        self.data = self.data.fillna('')
        self.header_conf = header_conf
        self.index_cols = index_cols
        self.pinned_cols = pinned_cols
        self.fontWeight = fontWeight
        self.backgroundColor = backgroundColor
        self.color = color
        self.key = key
        scales = str(len([c for c in self.color_map.split("\n") if len(c.strip()) > 0]) - 1)
        self.js_cell_code = self.js_cell_code.replace('{color_map}',self.color_map)
        self.js_cell_code = self.js_cell_code.replace('{scales}',scales)
        self.color_setting = {"backgroundColor": self.backgroundColor,
                                            'fontWeight': self.fontWeight,
                                            "color": self.color}

    @staticmethod
    def is_number(n):
        try:
            float(n)
            return True
        except:
            return False
        
    
    def get_col_color(self,col):
        vals = set([float(v) for v in self.data[col] if self.is_number(v)])
        if len(vals) > 1:
            max_val = max(vals)
            min_val = min(vals)
            js_code = self.js_cell_code.replace("{col}", col)
            js_code = js_code.replace("{max_val}", str(max_val))
            js_code = js_code.replace("{min_val}", str(min_val))

            return JsCode(js_code)
    
    @staticmethod
    def parse_number_formatter(number_type):
        if number_type == "%":
            return "!isNaN(parseFloat(x.toLocaleString()))?(x * 100.0).toLocaleString() + '%':x.toLocaleString()"
        elif number_type == "$":
            return "!isNaN(parseFloat(x.toLocaleString()))?'$' + x.toLocaleString():x.toLocaleString()"
        elif number_type == "￥":
            return "!isNaN(parseFloat(x.toLocaleString()))?'￥'+ x.toLocaleString():x.toLocaleString()"
        else:
            return "x.toLocaleString()"
        
    def get_group_header(self,with_color):
        all_confs = []
        asigned_cols = []
        for header in self.header_conf:
            conf = {}
            conf["headerName"] = header
            conf["children"] = []
            for col_conf in self.header_conf[header]:
                assert "field"  in col_conf, 'please set "field" in you header config dict.'
                col = col_conf["field"]
                header_name = col_conf.get("headerName",None)
                if col not in self.pinned_cols and col in  self.data.columns.values:
                    asigned_cols += [col]
                    c_con = {}
                    c_con["field"] = col
                    if header_name is not None:
                        c_con["headerName"] = header_name
                    number_type = col_conf.get('formatter', None)
                    formatter = self.parse_number_formatter(number_type)
                    c_con["valueFormatter"] = formatter
                    if with_color: 
                        js_code = self.get_col_color(col)
                        if js_code is not None:
                            c_con["cellStyle"] =  js_code
                    else:
                        c_con["cellStyle"] =  self.color_setting
                    conf["children"] += [c_con]
            all_confs += [conf]
        for col in self.pinned_cols:
            all_confs += [{ 'field': col,
                           'pinned': 'left',
                            'wrapText':True,
                           "cellStyle":self.color_setting}]
        asigned_cols += self.pinned_cols
        for col in self.data.columns.values:
            if col not in asigned_cols:
                conf = {}
                conf["field"] = col
                if with_color: 
                    js_code = self.get_col_color(col)
                    if js_code is not None:
                        conf["cellStyle"] =  js_code
                    else:
                        conf["cellStyle"] = self.color_setting
                else:
                    conf["cellStyle"] = self.color_setting
                all_confs += [conf]
        grid_options = {}
        grid_options["columnDefs"] = all_confs
        grid_options["enableRangeSelection"] = True
        grid_options["autoSizeStrategy"] ={"type":"fitCellContents","skipHeader":False}
        return grid_options            

    def load_color_map_file(self,file_name):
        # You can generate color from here https://hihayk.github.io/scale/#0/300/62/80/-55/67/20/-15/940000/149/0/0/white
        color_map = "["
        try:
            with open(file_name, 'r') as file:
                contents = [l for l in file.readlines()][::-1]
                for color in contents:
                    color = color.strip()
                    if len(color) > 0:
                        color_map += "'%s',\n" % color
                color_map += "]"
                return color_map
        except FileNotFoundError:
            return None
        
    def load_color_map(self):
        color_map = "["
        for color in COLOR_MAP.split('\n')[::-1]:
            color = color.strip()
            if len(color) > 0:
                color_map += "'%s',\n" % color
        color_map += "]"
        return color_map
    
    
    def show(self, with_color=False):
        grid_options = self.get_group_header(with_color)
        return AgGrid(self.data, 
                      grid_options,
                      columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                      enable_enterprise_modules=True,
                      allow_unsafe_jscode=True,
                      key=self.key)
        

