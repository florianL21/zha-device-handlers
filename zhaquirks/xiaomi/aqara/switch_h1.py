from zigpy.profiles import zgp, zha, zcl
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import (
    Alarms,
    Basic,
    GreenPowerProxy,
    Groups,
    Identify,
    OnOff,
    Ota,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement

from zhaquirks.const import (
    ARGS,
    ATTR_ID,
    BUTTON,
    LEFT,
    RIGHT,
    CLUSTER_ID,
    COMMAND,
    COMMAND_DOUBLE,
    COMMAND_HOLD,
    COMMAND_SINGLE,
    DEVICE_TYPE,
    DOUBLE_PRESS,
    ENDPOINT_ID,
    ENDPOINTS,
    INPUT_CLUSTERS,
    LONG_PRESS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PRESS_TYPE,
    PROFILE_ID,
    SHORT_PRESS,
    VALUE,
)
from zhaquirks.xiaomi import (
    LUMI,
    BasicCluster,
    DeviceTemperatureCluster,
    OnOffCluster,
    XiaomiMeteringCluster,
    XiaomiAqaraE1Cluster,
)
from zhaquirks.xiaomi.aqara.opple_remote import MultistateInputCluster
from zhaquirks.xiaomi.aqara.opple_switch import OppleSwitchCluster, BOTH_BUTTONS

BUTTON_ANY = "any"
XIAOMI_COMMAND_SINGLE = f"41_{COMMAND_SINGLE}"
XIAOMI_COMMAND_DOUBLE = f"41_{COMMAND_DOUBLE}"
XIAOMI_COMMAND_HOLD = f"1_{COMMAND_HOLD}"
XIAOMI_COMMAND_LEFT_SINGLE = XIAOMI_COMMAND_SINGLE
XIAOMI_COMMAND_LEFT_DOUBLE = XIAOMI_COMMAND_DOUBLE
XIAOMI_COMMAND_RIGHT_SINGLE = f"42_{COMMAND_SINGLE}"
XIAOMI_COMMAND_RIGHT_DOUBLE = f"42_{COMMAND_DOUBLE}"
XIAOMI_COMMAND_BOTH_SINGLE = f"51_{COMMAND_SINGLE}"
XIAOMI_COMMAND_BOTH_DOUBLE = f"51_{COMMAND_DOUBLE}"


class AqaraH1SingleRockerBase(CustomDevice):
    """Device automation triggers for the Aqara H1 Single Rocker Switches"""

    device_automation_triggers = {
        (SHORT_PRESS, BUTTON): {
            ENDPOINT_ID: 41,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_SINGLE,
            ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_SINGLE, VALUE: 1},
        },
        (DOUBLE_PRESS, BUTTON): {
            ENDPOINT_ID: 41,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_DOUBLE,
            ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_DOUBLE, VALUE: 2},
        },
        (LONG_PRESS, BUTTON): {
            ENDPOINT_ID: 1,
            CLUSTER_ID: 64704,
            COMMAND: XIAOMI_COMMAND_HOLD,
            ARGS: {ATTR_ID: 0x00FC, PRESS_TYPE: COMMAND_HOLD, VALUE: 0},
        },
    }


class AqaraH1DoubleRockerBase(CustomDevice):
    """Device automation triggers for the Aqara H1 Double Rocker Switches"""

    device_automation_triggers = {
        (SHORT_PRESS, LEFT): {
            ENDPOINT_ID: 41,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_LEFT_SINGLE,
            ARGS: {ATTR_ID: 85, PRESS_TYPE: COMMAND_SINGLE, VALUE: 1},
        },
        (DOUBLE_PRESS, LEFT): {
            ENDPOINT_ID: 41,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_LEFT_DOUBLE,
            ARGS: {ATTR_ID: 85, PRESS_TYPE: COMMAND_DOUBLE, VALUE: 2},
        },
        (SHORT_PRESS, RIGHT): {
            ENDPOINT_ID: 42,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_RIGHT_SINGLE,
            ARGS: {ATTR_ID: 85, PRESS_TYPE: COMMAND_SINGLE, VALUE: 1},
        },
        (DOUBLE_PRESS, RIGHT): {
            ENDPOINT_ID: 42,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_RIGHT_DOUBLE,
            ARGS: {ATTR_ID: 85, PRESS_TYPE: COMMAND_DOUBLE, VALUE: 2},
        },
        (SHORT_PRESS, BOTH_BUTTONS): {
            ENDPOINT_ID: 51,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_BOTH_SINGLE,
            ARGS: {ATTR_ID: 85, PRESS_TYPE: COMMAND_SINGLE, VALUE: 1},
        },
        (DOUBLE_PRESS, BOTH_BUTTONS): {
            ENDPOINT_ID: 51,
            CLUSTER_ID: 18,
            COMMAND: XIAOMI_COMMAND_BOTH_DOUBLE,
            ARGS: {ATTR_ID: 85, PRESS_TYPE: COMMAND_DOUBLE, VALUE: 2},
        },
        (LONG_PRESS, BUTTON_ANY): {
            ENDPOINT_ID: 1,
            CLUSTER_ID: 64704,
            COMMAND: XIAOMI_COMMAND_HOLD,
            ARGS: {ATTR_ID: 252, PRESS_TYPE: COMMAND_HOLD, VALUE: 0},
        },
    }


class AqaraH1SingleRockerSwitchWithNeutral(AqaraH1SingleRockerBase):
    """Aqara H1 Single Rocker Switch (with neutral)."""

    signature = {
        MODELS_INFO: [(LUMI, "lumi.switch.n1aeu1")],
        ENDPOINTS: {
            #  input_clusters=[0, 2, 3, 4, 5, 6, 18, 64704], output_clusters=[10, 25]
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                    Alarms.cluster_id,  # 9
                    XiaomiMeteringCluster.cluster_id,  # 0x0702
                    ElectricalMeasurement.cluster_id,  # 0x0B04
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,  # 0x000a
                    Ota.cluster_id,  # 0x0019
                ],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,  # 0x0021
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    BasicCluster,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOffCluster,  # 6
                    Alarms.cluster_id,  # 9
                    MultistateInputCluster,  # 18
                    XiaomiMeteringCluster.cluster_id,  # 0x0702
                    OppleSwitchCluster,  # 0xFCC0 / 64704
                    ElectricalMeasurement.cluster_id,  # 0x0B04
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            41: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 18
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }


class AqaraH1SingleRockerSwitchNoNeutral(AqaraH1SingleRockerBase):
    """Aqara H1 Single Rocker Switch (no neutral)."""

    signature = {
        MODELS_INFO: [(LUMI, "lumi.switch.l1aeu1")],
        ENDPOINTS: {
            #  input_clusters=[0, 2, 3, 4, 5, 6, 9], output_clusters=[10, 25]
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                    Alarms.cluster_id,  # 9
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,  # 0x000a
                    Ota.cluster_id,  # 0x0019
                ],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,  # 0x0021
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    BasicCluster,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOffCluster,  # 6
                    Alarms.cluster_id,  # 9
                    MultistateInputCluster,  # 12
                    OppleSwitchCluster,  # 0xFCC0 / 64704
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            41: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 12
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }


class AqaraH1SingleRockerSwitchNoNeutralAlt1(AqaraH1SingleRockerSwitchNoNeutral):
    """Aqara H1 Single Rocker Switch (no neutral). Variant 1"""

    signature = {
        MODELS_INFO: [(LUMI, "lumi.switch.l1aeu1")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                    MultistateInputCluster.cluster_id,  # 12
                    XiaomiAqaraE1Cluster.cluster_id,  # 0xfcc0
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,  # 0x000a
                    Ota.cluster_id,  # 0x0019
                ],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,  # 0x0021
                ],
            },
        },
    }


class AqaraH1SingleRockerSwitchNoNeutralAlt2(AqaraH1SingleRockerSwitchNoNeutral):
    """Aqara H1 Single Rocker Switch (no neutral). Variant 2"""

    signature = {
        MODELS_INFO: [(LUMI, "lumi.switch.l1aeu1")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                    MultistateInputCluster.cluster_id,  # 12
                    XiaomiAqaraE1Cluster.cluster_id,  # 0xfcc0
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,  # 0x000a
                    Ota.cluster_id,  # 0x0019
                ],
            },
            41: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    MultistateInputCluster.cluster_id,  # 12
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,  # 0x0021
                ],
            },
        },
    }


class AqaraH1DoubleRockerSwitchNoNeutral(AqaraH1DoubleRockerBase):
    """Aqara H1 Double Rocker Switch (no neutral)."""

    signature = {
        MODELS_INFO: [(LUMI, "lumi.switch.l2aeu1")],
        ENDPOINTS: {
            #  input_clusters=[0, 2, 3, 4, 5, 6, 9], output_clusters=[10, 25]
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                    Alarms.cluster_id,  # 9
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,  # 0x000a
                    Ota.cluster_id,  # 0x0019
                ],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,  # 0x0021
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    BasicCluster,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOffCluster,  # 6
                    Alarms.cluster_id,  # 9
                    MultistateInputCluster,  # 18
                    OppleSwitchCluster,  # 0xFCC0 / 64704
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    MultistateInputCluster,
                    OppleSwitchCluster,
                ],
                OUTPUT_CLUSTERS: [],
            },
            41: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 18
                ],
                OUTPUT_CLUSTERS: [],
            },
            42: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 18
                ],
                OUTPUT_CLUSTERS: [],
            },
            51: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 18
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }


class AqaraH1DoubleRockerSwitchWithNeutral(AqaraH1DoubleRockerBase):
    """Aqara H1 Double Rocker Switch (with neutral)."""

    signature = {
        MODELS_INFO: [(LUMI, "lumi.switch.n2aeu1")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                    Alarms.cluster_id,  # 9
                    XiaomiMeteringCluster.cluster_id,  # 0x0702
                    ElectricalMeasurement.cluster_id,  # 0x0B04
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,  # 0x000a
                    Ota.cluster_id,  # 0x0019
                ],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,  # 0
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOff.cluster_id,  # 6
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [
                    GreenPowerProxy.cluster_id,  # 0x0021
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    BasicCluster,  # 0
                    DeviceTemperatureCluster.cluster_id,  # 2
                    Identify.cluster_id,  # 3
                    Groups.cluster_id,  # 4
                    Scenes.cluster_id,  # 5
                    OnOffCluster,  # 6
                    Alarms.cluster_id,  # 9
                    MultistateInputCluster,  # 18
                    XiaomiMeteringCluster.cluster_id,  # 0x0702
                    OppleSwitchCluster,  # 0xFCC0 / 64704
                    ElectricalMeasurement.cluster_id,  # 0x0B04
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    MultistateInputCluster,
                    OppleSwitchCluster,
                ],
                OUTPUT_CLUSTERS: [],
            },
            41: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 18
                ],
                OUTPUT_CLUSTERS: [],
            },
            42: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 18
                ],
                OUTPUT_CLUSTERS: [],
            },
            51: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    MultistateInputCluster,  # 18
                ],
                OUTPUT_CLUSTERS: [],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }
