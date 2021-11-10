DI_SecondThrottleEnable = 37
DI_IVSSecondThrottle = 38
DI_SwitchoffBBMInputs = 68

StateOkayStd = 0
StateIVSArea1Std = 1
StateIVSArea3Std = 2
StateAccPedalSensorArea1Std = 3
StateAccPedalSensorArea3Std = 4
StateAccIVSArea1Std = 5
StateAccIVSArea3Std = 6
StateRangeErrorStd = 7
StatePowerErrorStd = 8

ComConf_ComSignal_RemDisablPrimryAccPedl_BB4_X_BB_oVP19_X_BB_oJ1939_4_BBNetwork_443582bf_Rx = 248
ComConf_ComSignal_RemDisablPrimryAccPedl_BB4_X_BBU_oVP19_X_BBU_oJ1939_4_BBNetwork_5240c857_Rx = 247
ComConf_ComSignal_AcceleratorPedalPosition1_oVP2_oJ1939_1_1ebe80d0_Rx = 27
ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx = 254
ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx = 255
RX_CAN3_VP19_55 = 32
RX_CAN3_VP19_E5 = 31

def on_reset():
    expect_pause()
    glb_filter(GRP_ON)
    continue_test() 
#################################TESTCASE 1########################################################################################
#Second accelerator pedal - Pedal Status
print( "\nTests for STest Case acc pedal:\n")
test ("Req desc: Test Case acc pedal ")
print("Test case-1")

# Set parameter ACC_SECOND_PEDAL_ENABLE = 1
current_obj(OBJ_AP,"RSL_Enable2ndPedal")
fill(0,1,1,0x01);

# Set parameter HANDTHROTTLE_ACTIVE = 0
current_obj(OBJ_AP,"RSL_HandThrottleActive")
fill(0,1,1,0x00);

# The digital input Second Throttle Enable
current_obj(OBJ_AP,"IO_list")
fill(37,1,1,0x01)

# Analog value Second Throttle <= ACC_MIN_SCALE
current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R8P_ACC_u16PedalMinMaxScaleLimit_v")
fill(0,2,1,0x0001);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIF_ACC_VOLTAGE_DIVISION_R1_v")
fill(0,2,1,0x0001);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIG_ACC_VOLTAGE_DIVISION_RTOT_v")
fill(0,2,1,0xFFEE);

command ("AD_CHECK",1000) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateOkayStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Check composition of VP45 message
command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 1"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

######################################
# StateOkayStd -> StatePowerErrorStd

command ("SET_LINEAR_CHANNEL_VALUE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIG_ACC_VOLTAGE_DIVISION_RTOT_v")
fill(0,2,1,0x0000);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StatePowerErrorStd 
command ("CHECK_Q_SGSTATE",1)  
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#StatePowerErrorStd -> StateOkayStd

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIG_ACC_VOLTAGE_DIVISION_RTOT_v")
fill(0,2,1,0xFFEE);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateOkayStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Check composition of VP45 message
command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 1"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#######################################
# StateOkayStd -> StateRangeErrorStd

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1G51_AccPedal_Min_Range_Limit_v")
fill(0,2,1,0x0001);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIE_ACC_ERROR_DELAY_v")
fill(0,2,1,0x0001);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100000) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateRangeErrorStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Check composition of VP45 message
command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 254"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 2"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# StateRangeErrorStd -> StateOkayStd

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1G51_AccPedal_Min_Range_Limit_v")
fill(0,2,1,0x0000);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1G50_AccPedal_Max_Range_Limit_v")
fill(0,2,1,0x0064);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIG_ACC_VOLTAGE_DIVISION_RTOT_v")
fill(0,2,1,0x0001);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIF_ACC_VOLTAGE_DIVISION_R1_v")
fill(0,2,1,0x0002);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_LINEAR_CHANNEL_VALUE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateOkayStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

############################################################
# StateOkayStd ->_StateAccIVSArea1Std (entered into conflict)
# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x01);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0002);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIE_ACC_ERROR_DELAY_v")
fill(0,2,1,0x0001);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100000) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateAccIVSArea1Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#############################################################################
#_StateAccIVSArea1Std -> _StateAccPedalSensorArea1Std (recovery from conflict)
# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x00);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateAccPedalSensorArea1Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Recover from Acc pedal sensor error
# _StateAccPedalSensorArea1Std -> StateOkayStd
#recovery from Accstd
# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x01);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0000);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateOkayStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

############################################################
# StateOkayStd -> _StateAccIVSArea3Std (after diagnostics)

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0000);

# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x00);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100000) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateAccIVSArea3Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#############################################################################
#_StateAccIVSArea3Std -> _StateAccPedalSensorArea3Std (recovery from conflict)
current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0000);

# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x01);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateAccPedalSensorArea3Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Recover from Acc pedal sensor error
# _StateAccPedalSensorArea3Std -> StateOkayStd
#recovery from Accstd
# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x00);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0002);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateOkayStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

##################################
#StateOkayStd -> _StateIVSArea1Std

# StateOkayStd ->_StateAccIVSArea1Std (entered into conflict)
# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x01);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0002);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIE_ACC_ERROR_DELAY_v")
fill(0,2,1,0x0001);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100000) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateAccIVSArea1Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0000);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateIVSArea1Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# _StateIVSArea1Std -> StateOkayStd
# Recover from IVS error

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0002);

# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x00);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateOkayStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

###################################
#StateOkayStd -> _StateIVSArea3Std

# StateOkayStd -> _StateAccIVSArea3Std (after diagnostics)

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0000);

# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x00);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SIMULATE_TIME",100000) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateAccIVSArea3Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x00);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0002);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is _StateIVSArea3Std 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# _StateIVSArea3Std -> StateOkayStd
# Recover from IVS error

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1R17_ACC_u16MaxValueForIVSActivation_v")
fill(0,2,1,0x0000);

# DI_IVSSecondThrottle
current_obj(OBJ_AP,"IO_list")
fill(38,1,1,0x01);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# check if the state is StateOkayStd 
command ("CHECK_Q_SGSTATE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#######################################TESTCASE 2############################################################################
#Second accelerator pedal - Hand throttle Status
print( "\nTests for STest Case acc pedal:\n")
test ("Req desc: Test Case acc pedal ")
print("Test case-2")

# Set parameter ACC_SECOND_PEDAL_ENABLE = 1
current_obj(OBJ_AP,"RSL_Enable2ndPedal")
fill(0,1,1,0x01);

# Set parameter HANDTHROTTLE_ACTIVE = 1
current_obj(OBJ_AP,"RSL_HandThrottleActive")
fill(0,1,1,0x01);

# The digital input Second Throttle Enable
current_obj(OBJ_AP,"IO_list")
fill(37,1,1,0x01)

# Analog value Second Throttle <= HANDTHROTTLE_ZERO_PERC
current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1TB0_AccPed_HandThrottle_LowerLimit_v")
fill(0,2,1,0x0400);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIF_ACC_VOLTAGE_DIVISION_R1_v")
fill(0,2,1,0x0001);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_X1CIG_ACC_VOLTAGE_DIVISION_RTOT_v")
fill(0,2,1,0x0001);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1TB3_AccPed_HandThrottle_MinRange_v")
fill(0,2,1,0x0002);

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1TB4_AccPed_HandThrottle_MaxRange_v")
fill(0,2,1,0x0064);

command ("AD_CHECK",20) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_LINEAR_CHANNEL_VALUE",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 1"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("AD_CHECK",1000) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 254"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 2"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

###################################TESTCASE 3######################################################################
# Second accelerator pedal - Primary Pedal disable
print( "\nTests for STest Case acc pedal:\n")
test ("Req desc: Test Case acc pedal ")
print("Test case-3")

# Set parameter ACC_SECOND_PEDAL_ENABLE = 0
current_obj(OBJ_AP,"RSL_Enable2ndPedal")
fill(0,1,1,0x00);

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Set parameter ACC_SECOND_PEDAL_ENABLE = 2
current_obj(OBJ_AP,"RSL_Enable2ndPedal")
fill(0,1,1,0x02);

#primary pedal disable over BBCAN VP19_55

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1TFO_BBUnit_SourceAddress_v")
fill(0,1,1,0x55);

command ("SET_J1939OK_MSGSTATUS",RX_CAN3_VP19_55) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#disable over BBCAN
command ("SET_J1939_RX_MESSAGES",ComConf_ComSignal_RemDisablPrimryAccPedl_BB4_X_BB_oVP19_X_BB_oJ1939_4_BBNetwork_443582bf_Rx,1)
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 1"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#primary pedal disable over BBCAN VP19_E5

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1TFO_BBUnit_SourceAddress_v")
fill(0,1,1,0xE5);

command ("SET_J1939OK_MSGSTATUS",RX_CAN3_VP19_E5) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#disable over BBCAN
command ("SET_J1939_RX_MESSAGES",ComConf_ComSignal_RemDisablPrimryAccPedl_BB4_X_BBU_oVP19_X_BBU_oJ1939_4_BBNetwork_5240c857_Rx,1)
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 1"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#primary pedal disable over DI_SecondThrottleEnable

command ("SET_J1939ERROR_MSGSTATUS",RX_CAN3_VP19_55) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_J1939ERROR_MSGSTATUS",RX_CAN3_VP19_E5) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# The digital input Second Throttle Enable
current_obj(OBJ_AP,"IO_list")
fill(37,1,1,0x01)

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 1"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# g_DisablePrimaryPedal = FALSE

current_obj(OBJ_AP,"Rte_AddrPar_0x29_P1TFO_BBUnit_SourceAddress_v")
fill(0,1,1,0xE5);

command ("SET_J1939OK_MSGSTATUS",RX_CAN3_VP19_E5) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

#disable over BBCAN
command ("SET_J1939_RX_MESSAGES",ComConf_ComSignal_RemDisablPrimryAccPedl_BB4_X_BBU_oVP19_X_BBU_oJ1939_4_BBNetwork_5240c857_Rx,0)
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# The digital input Second Throttle Enable
current_obj(OBJ_AP,"IO_list")
fill(37,1,1,0x00)

# PrimaryPedalPosition
command ("SET_J1939_RX_MESSAGES",ComConf_ComSignal_AcceleratorPedalPosition1_oVP2_oJ1939_1_1ebe80d0_Rx,0)
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# PrimaryPedalPosition
command ("SET_J1939_RX_MESSAGES",ComConf_ComSignal_AcceleratorPedalPosition1_oVP2_oJ1939_1_1ebe80d0_Rx,1)
expect ("@timestamp Trg-Done QS_RX_COMMAND")

# Call the task function
command ("ACC_TASK",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

###################################TESTCASE 4######################################################################
#EnableExternalBBMInputs
print( "\nTests for STest Case acc pedal:\n")
test ("Req desc: Test Case acc pedal ")
print("Test case-4")

command ("EnableExternalBBMInputs",1) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

command ("SET_VP45_DATA",1) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalPos_oVP45_B_oJ1939_1_974d7bd5_Tx)) 
expect ("@timestamp COM_TRANSMIT %d 0"  %(ComConf_ComSignal_VP45B_SecondAccPedalStatus_oVP45_B_oJ1939_1_64a06fbb_Tx)) 
expect ("@timestamp Trg-Done QS_RX_COMMAND")

###################################################################################################################















