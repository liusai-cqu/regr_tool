class regress_cfg:
    TC_LIST = [
        # {"TC": "Test_Case_1", "SEED": 123456, "SIM_OPTS": "pl=UVM_HIGH", "RUN_TIMES": 3, "TIMEOUT_LMT": 300, "MODE": ["mode1"]},
        # {"TC": "Test_Case_2", "SEED": 987654, "SIM_OPTS": "pl=UVM_LOW", "RUN_TIMES": 2, "MODE": ["mode2"]},
        {"TC": "tc_sanity", "SEED": 123456, "SIM_OPTS": "", "RUN_TIMES": 1, "MODE": "base_fun"},
    ]

    ERR_KEYWORD = "Failed|Error|FAILED|ERROR"
    BLK_NAME = "cm_ahb_mon"
    CCOV = "on"
    COMMON_TIMEOUT_LMT = 15
    WAVE = "off"
    BSB_OPTS = "Local Machine"
    REGRESS_UDC = ""