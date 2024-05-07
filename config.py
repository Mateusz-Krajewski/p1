import configparser



class Config:
    def __init__(self):
        config=configparser.ConfigParser()
        config.read('config.ini')
        self.m=config['config'].getfloat('m')
        self.b=config['config'].getfloat('b')
        self.alfa=config['config'].getfloat('alfa')
        self.v0=config['config'].getfloat('v0')
        self.step=config['config'].getfloat('step')
        self.sym_time=config['config'].getint("sym_time")
        self.g = config['config'].getfloat("g")
        self.calc_a_for_range = True if config.has_section("range") else False

    def __str__(self) -> str:
        return f"""
        m={self.m},
        b={self.b},
        alfa={self.alfa},
        v0={self.v0},
        time={self.sym_time}
        """
    