////////////////////////////////////////////////////////////////////////////////
//! @file		CsvDefine.h
//! @brief		CsvDefine
//! @details	��`�t�@�C��
//! @date		2013/09/18 Create
//! @author		FSI Hidetaka Kawamura
//
//  Copyright 2013 NISSAN MOTOR CO.,LTD.
////////////////////////////////////////////////////////////////////////////////

#ifndef __CSV_DEFINE_H__
#define __CSV_DEFINE_H__

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000


//////////////////////////////////////////////////////////////////////////////
//	define																	//
//////////////////////////////////////////////////////////////////////////////
//------------------
// ���ʂŎg�p����l
//------------------
#define CSV_DECIMAL_NUM								(8)							// �����_�ȉ��̌���
#define CSV_DECIMAL_NUM_DMS_SEC						(4)							// DMS�̕b�Ŏg�p���鏬���_�ȉ��̌���

//------------------
// �o�̓t�@�C����
//------------------
#define CSV_FILE_NAME_D01							("D01.csv")
#define CSV_FILE_NAME_D02							("D02.csv")
#define CSV_FILE_NAME_D06							("D06.csv")
#define CSV_FILE_NAME_B002							("B002.csv")
#define CSV_FILE_NAME_B003							("B003.csv")
#define CSV_FILE_NAME_M001							("M001.csv")
#define CSV_FILE_NAME_M002							("M002.csv")
#define CSV_FILE_NAME_M003							("M003.csv")
#define CSV_FILE_NAME_R006							("R006.csv")
#define CSV_FILE_NAME_R008							("R008.csv")

//------------------
// �o�̓f�[�^�̐擪�s�̋L�ړ��e
//------------------
// D01
#define CSV_DATA_NUM_D01_MCODE						(3)							// ���b�V���R�[�h�̐�

#define CSV_DATA_CONTENTS_D01_PID					("PID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_D01_B						("B")						// �ʒu�F�ܓx
#define CSV_DATA_CONTENTS_D01_L						("L")						// �ʒu�F�o�x
#define CSV_DATA_CONTENTS_D01_H						("H")						// �ʒu�F����
#define CSV_DATA_CONTENTS_D01_BX					("Bx")						// �ʒu�Fx
#define CSV_DATA_CONTENTS_D01_LY					("Ly")						// �ʒu�Fy
#define CSV_DATA_CONTENTS_D01_REF					("Ref")						// ���ʒ��p���W�n
#define CSV_DATA_CONTENTS_D01_MCODE1				("MCODE1")					// 1�����b�V���R�[�h
#define CSV_DATA_CONTENTS_D01_MCODE2				("MCODE2")					// 2�����b�V���R�[�h
#define CSV_DATA_CONTENTS_D01_MCODE3				("MCODE3")					// 3�����b�V���R�[�h
#define CSV_DATA_CONTENTS_D01_GROUND				("Ground")					// �n�\�_��
#define CSV_DATA_CONTENTS_D01_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_D01_PID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_D01_B							("float")					// �ʒu�F�ܓx
#define CSV_DATA_TYPE_D01_L							("float")					// �ʒu�F�o�x
#define CSV_DATA_TYPE_D01_H							("float")					// �ʒu�F����
#define CSV_DATA_TYPE_D01_BX						("float")					// �ʒu�Fx
#define CSV_DATA_TYPE_D01_LY						("float")					// �ʒu�Fy
#define CSV_DATA_TYPE_D01_REF						("int")						// ���ʒ��p���W�n
#define CSV_DATA_TYPE_D01_MCODE1					("int")						// 1�����b�V���R�[�h
#define CSV_DATA_TYPE_D01_MCODE2					("int")						// 2�����b�V���R�[�h
#define CSV_DATA_TYPE_D01_MCODE3					("int")						// 3�����b�V���R�[�h
#define CSV_DATA_TYPE_D01_GROUND					("int")						// �n�\�_��
#define CSV_DATA_TYPE_D01_DATASET					("int")						// �擾����

// D02
#define CSV_DATA_CONTENTS_D02_LID					("LID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_D02_BPT					("BPT")						// �O�|�C���gID
#define CSV_DATA_CONTENTS_D02_FPT					("FPT")						// ��|�C���gID
#define CSV_DATA_CONTENTS_D02_BLN					("BLN")						// �O���C��ID
#define CSV_DATA_CONTENTS_D02_FLN					("FLN")						// �ド�C��ID
#define CSV_DATA_CONTENTS_D02_PID					("PID")						// �~�ʏ��1�_
#define CSV_DATA_CONTENTS_D02_INVISIBLEFG			("InvisibleFG")				// �A��FG
#define CSV_DATA_CONTENTS_D02_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_D02_LID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_D02_BPT						("int")						// �O�|�C���gID
#define CSV_DATA_TYPE_D02_FPT						("int")						// ��|�C���gID
#define CSV_DATA_TYPE_D02_BLN						("int")						// �O���C��ID
#define CSV_DATA_TYPE_D02_FLN						("int")						// �ド�C��ID
#define CSV_DATA_TYPE_D02_PID						("int")						// �~�ʏ��1�_
#define CSV_DATA_TYPE_D02_INVISIBLEFG				("int")						// �A��FG
#define CSV_DATA_TYPE_D02_DATASET					("int")						// �擾����

// D06
#define CSV_DATA_CONTENTS_D06_AID					("AID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_D06_BLN					("BLN")						// �ŏ��̃��C��ID
#define CSV_DATA_CONTENTS_D06_FLN					("FLN")						// �Ō�̃��C��ID
#define CSV_DATA_CONTENTS_D06_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_D06_AID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_D06_BLN						("int")						// �ŏ��̃��C��ID
#define CSV_DATA_TYPE_D06_FLN						("int")						// �Ō�̃��C��ID
#define CSV_DATA_TYPE_D06_DATASET					("int")						// �擾����

// B002
#define CSV_DATA_CONTENTS_B002_ID					("ID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_B002_PID					("PID")						// �|�C���gID
#define CSV_DATA_CONTENTS_B002_REFID				("RefID")					// �Q��ID
#define CSV_DATA_CONTENTS_B002_KIND					("KIND")					// ���
#define CSV_DATA_CONTENTS_B002_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_B002_ID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_B002_PID						("int")						// �|�C���gID
#define CSV_DATA_TYPE_B002_REFID					("int")						// �Q��ID
#define CSV_DATA_TYPE_B002_KIND						("int")						// ���
#define CSV_DATA_TYPE_B002_DATASET					("int")						// �擾����

// B003
#define CSV_DATA_NUM_B003_LEFTLANE					(2)							// ���Ԑ��̐�
#define CSV_DATA_NUM_B003_RIGHTLANE					(2)							// �E�Ԑ��̐�
#define CSV_DATA_NUM_B003_OPPOSITELANE				(3)							// ���ΎԐ��̐�
#define CSV_DATA_NUM_B003_HIGHERPRIORITYLINK		(3)							// HigherPriorityLink�̐�
#define CSV_DATA_NUM_B003_LOWERPRIORITYLINK			(3)							// LowerPriorityLink�̐�
#define CSV_DATA_NUM_B003_RUNAREA					(4)							// �����G���AID�̐�
#define CSV_DATA_NUM_B003_BID						(3)							// �ڑ������NID�̐�
#define CSV_DATA_NUM_B003_FID						(3)							// ���򃊃��NID�̐�

#define CSV_DATA_CONTENTS_B003_ID					("ID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_B003_BID					("BID")						// ��O�̃����NID
#define CSV_DATA_CONTENTS_B003_FID					("FID")						// ��̃����NID
#define CSV_DATA_CONTENTS_B003_BNID					("BNID")					// ��O�m�[�hID
#define CSV_DATA_CONTENTS_B003_FNID					("FNID")					// ��m�[�hID
#define CSV_DATA_CONTENTS_B003_SPEEDMAX				("SpeedMax")				// �������x
#define CSV_DATA_CONTENTS_B003_SPEEDAVG				("SpeedAvg")				// ���ϑ��x
#define CSV_DATA_CONTENTS_B003_LENGTH				("Length")					// ����
#define CSV_DATA_CONTENTS_B003_LANETYPE				("LaneType")				// ���[�����
#define CSV_DATA_CONTENTS_B003_LANECHANGEALLOWED	("LaneChangeAllowed")		// �i�H�ύX
#define CSV_DATA_CONTENTS_B003_LANENUMBER			("LaneNumber")				// ���[���ԍ�
#define CSV_DATA_CONTENTS_B003_INSIDEINTERSECTION	("InsideIntersection")		// �����_��
#define CSV_DATA_CONTENTS_B003_LEFTLANE1			("LeftLane1")				// �������F����
#define CSV_DATA_CONTENTS_B003_LEFTLANE2			("LeftLane2")				// �������F���ׂ̍���
#define CSV_DATA_CONTENTS_B003_RIGHTLANE1			("RightLane1")				// �������F�E��
#define CSV_DATA_CONTENTS_B003_RIGHTLANE2			("RightLane2")				// �������F�E�ׂ̉E��
#define CSV_DATA_CONTENTS_B003_OPPOSITELANE1		("OppositeLane1")			// ���ΎԐ��F�Ŋ�
#define CSV_DATA_CONTENTS_B003_OPPOSITELANE2		("OppositeLane2")			// ���ΎԐ��F�Ŋ�̊O��
#define CSV_DATA_CONTENTS_B003_OPPOSITELANE3		("OppositeLane3")			// ���ΎԐ��F�O���̊O��
#define CSV_DATA_CONTENTS_B003_RUNCTRL				("RunCtrl")					// ���s�K��
#define CSV_DATA_CONTENTS_B003_LEFTWIDTH			("LeftWidth")				// ���Ԑ���
#define CSV_DATA_CONTENTS_B003_LEFTLANEMARKERID		("LeftLaneMarkerID")		// ������ID
#define CSV_DATA_CONTENTS_B003_LEFTCURBID			("LeftCurbID")				// ������ID
#define CSV_DATA_CONTENTS_B003_LEFTGUTTERID			("LeftGutterID")			// �����aID
#define CSV_DATA_CONTENTS_B003_LEFTOTHERID			("LeftOtherID")				// �����̑�ID
#define CSV_DATA_CONTENTS_B003_RIGHTWIDTH			("RightWidth")				// �E�Ԑ���
#define CSV_DATA_CONTENTS_B003_RIGHTLANEMARKERID	("RightLaneMarkerID")		// �E����ID
#define CSV_DATA_CONTENTS_B003_RIGHTCURBID			("RightCurbID")				// �E����ID
#define CSV_DATA_CONTENTS_B003_RIGHTGUTTERID		("RightGutterID")			// �E���aID
#define CSV_DATA_CONTENTS_B003_RIGHTOTHERID			("RightOtherID")			// �E���̑�ID
#define CSV_DATA_CONTENTS_B003_HIGHERPRIORITYLINK1	("HigherPriorityLink1")		// �D�惊���NID
#define CSV_DATA_CONTENTS_B003_HIGHERPRIORITYLINK2	("HigherPriorityLink2")		// �D�惊���NID
#define CSV_DATA_CONTENTS_B003_HIGHERPRIORITYLINK3	("HigherPriorityLink3")		// �D�惊���NID
#define CSV_DATA_CONTENTS_B003_LOWERPRIORITYLINK1	("LowerPriorityLink1")		// �D�惊���NID
#define CSV_DATA_CONTENTS_B003_LOWERPRIORITYLINK2	("LowerPriorityLink2")		// �D�惊���NID
#define CSV_DATA_CONTENTS_B003_LOWERPRIORITYLINK3	("LowerPriorityLink3")		// �D�惊���NID
#define CSV_DATA_CONTENTS_B003_RUNAREA1				("RunArea1")				// �����G���AID
#define CSV_DATA_CONTENTS_B003_RUNAREA2				("RunArea2")				// �����G���AID
#define CSV_DATA_CONTENTS_B003_RUNAREA3				("RunArea3")				// �����G���AID
#define CSV_DATA_CONTENTS_B003_RUNAREA4				("RunArea4")				// �����G���AID
#define CSV_DATA_CONTENTS_B003_BID2					("BID2")					// �ڑ������NID
#define CSV_DATA_CONTENTS_B003_BID3					("BID3")					// �ڑ������NID
#define CSV_DATA_CONTENTS_B003_BID4					("BID4")					// �ڑ������NID
#define CSV_DATA_CONTENTS_B003_FID2					("FID2")					// ���򃊃��NID
#define CSV_DATA_CONTENTS_B003_FID3					("FID3")					// ���򃊃��NID
#define CSV_DATA_CONTENTS_B003_FID4					("FID4")					// ���򃊃��NID
#define CSV_DATA_CONTENTS_B003_DATASET				("Dataset")					// �擾����
#define CSV_DATA_CONTENTS_B003_LID					("LID")						// �Ԑ��f�[�^ID

#define CSV_DATA_TYPE_B003_ID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_B003_BID						("int")						// ��O�̃����NID
#define CSV_DATA_TYPE_B003_FID						("int")						// ��̃����NID
#define CSV_DATA_TYPE_B003_BNID						("int")						// ��O�m�[�hID
#define CSV_DATA_TYPE_B003_FNID						("int")						// ��m�[�hID
#define CSV_DATA_TYPE_B003_SPEEDMAX					("float")					// �������x
#define CSV_DATA_TYPE_B003_SPEEDAVG					("float")					// ���ϑ��x
#define CSV_DATA_TYPE_B003_LENGTH					("float")					// ����
#define CSV_DATA_TYPE_B003_LANETYPE					("int")						// ���[�����
#define CSV_DATA_TYPE_B003_LANECHANGEALLOWED		("int")						// �i�H�ύX
#define CSV_DATA_TYPE_B003_LANENUMBER				("int")						// ���[���ԍ�
#define CSV_DATA_TYPE_B003_INSIDEINTERSECTION		("int")						// �����_��
#define CSV_DATA_TYPE_B003_LEFTLANE1				("int")						// �������F����
#define CSV_DATA_TYPE_B003_LEFTLANE2				("int")						// �������F���ׂ̍���
#define CSV_DATA_TYPE_B003_RIGHTLANE1				("int")						// �������F�E��
#define CSV_DATA_TYPE_B003_RIGHTLANE2				("int")						// �������F�E�ׂ̉E��
#define CSV_DATA_TYPE_B003_OPPOSITELANE1			("int")						// ���ΎԐ��F�Ŋ�
#define CSV_DATA_TYPE_B003_OPPOSITELANE2			("int")						// ���ΎԐ��F�Ŋ�̊O��
#define CSV_DATA_TYPE_B003_OPPOSITELANE3			("int")						// ���ΎԐ��F�O���̊O��
#define CSV_DATA_TYPE_B003_RUNCTRL					("int")						// ���s�K��
#define CSV_DATA_TYPE_B003_LEFTWIDTH				("float")					// ���Ԑ���
#define CSV_DATA_TYPE_B003_LEFTLANEMARKERID			("int")						// ������ID
#define CSV_DATA_TYPE_B003_LEFTCURBID				("int")						// ������ID
#define CSV_DATA_TYPE_B003_LEFTGUTTERID				("int")						// �����aID
#define CSV_DATA_TYPE_B003_LEFTOTHERID				("int")						// �����̑�ID
#define CSV_DATA_TYPE_B003_RIGHTWIDTH				("float")					// �E�Ԑ���
#define CSV_DATA_TYPE_B003_RIGHTLANEMARKERID		("int")						// �E����ID
#define CSV_DATA_TYPE_B003_RIGHTCURBID				("int")						// �E����ID
#define CSV_DATA_TYPE_B003_RIGHTGUTTERID			("int")						// �E���aID
#define CSV_DATA_TYPE_B003_RIGHTOTHERID				("int")						// �E���̑�ID
#define CSV_DATA_TYPE_B003_HIGHERPRIORITYLINK1		("int")						// �D�惊���NID
#define CSV_DATA_TYPE_B003_HIGHERPRIORITYLINK2		("int")						// �D�惊���NID
#define CSV_DATA_TYPE_B003_HIGHERPRIORITYLINK3		("int")						// �D�惊���NID
#define CSV_DATA_TYPE_B003_LOWERPRIORITYLINK1		("int")						// �D�惊���NID
#define CSV_DATA_TYPE_B003_LOWERPRIORITYLINK2		("int")						// �D�惊���NID
#define CSV_DATA_TYPE_B003_LOWERPRIORITYLINK3		("int")						// �D�惊���NID
#define CSV_DATA_TYPE_B003_RUNAREA1					("int")						// �����G���AID
#define CSV_DATA_TYPE_B003_RUNAREA2					("int")						// �����G���AID
#define CSV_DATA_TYPE_B003_RUNAREA3					("int")						// �����G���AID
#define CSV_DATA_TYPE_B003_RUNAREA4					("int")						// �����G���AID
#define CSV_DATA_TYPE_B003_BID2						("int")						// �ڑ������NID
#define CSV_DATA_TYPE_B003_BID3						("int")						// �ڑ������NID
#define CSV_DATA_TYPE_B003_BID4						("int")						// �ڑ������NID
#define CSV_DATA_TYPE_B003_FID2						("int")						// ���򃊃��NID
#define CSV_DATA_TYPE_B003_FID3						("int")						// ���򃊃��NID
#define CSV_DATA_TYPE_B003_FID4						("int")						// ���򃊃��NID
#define CSV_DATA_TYPE_B003_DATASET					("int")						// �擾����
#define CSV_DATA_TYPE_B003_LID						("int")						// �Ԑ��f�[�^ID

// M001
#define CSV_DATA_NUM_M001_NEARESTLINK				(2)							// NearestLink�̐�

#define CSV_DATA_CONTENTS_M001_ID					("ID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_M001_LID					("LID")						// ���C��ID
#define CSV_DATA_CONTENTS_M001_COLOR				("Color")					// �F
#define CSV_DATA_CONTENTS_M001_LINENUM				("LineNum")					// ����
#define CSV_DATA_CONTENTS_M001_LINETYPE				("LineType")				// ����
#define CSV_DATA_CONTENTS_M001_WIDTH				("Width")					// ��
#define CSV_DATA_CONTENTS_M001_NEARESTLINK1			("NearestLink1")			// �����Ƃ��߂������N
#define CSV_DATA_CONTENTS_M001_NEARESTLINK2			("NearestLink2")			// �����Ƃ��߂������N
#define CSV_DATA_CONTENTS_M001_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_M001_ID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_M001_LID						("int")						// ���C��ID
#define CSV_DATA_TYPE_M001_COLOR					("char")					// �F
#define CSV_DATA_TYPE_M001_LINENUM					("int")						// ����
#define CSV_DATA_TYPE_M001_LINETYPE					("int")						// ����
#define CSV_DATA_TYPE_M001_WIDTH					("float")					// ��
#define CSV_DATA_TYPE_M001_NEARESTLINK1				("int")						// �����Ƃ��߂������N
#define CSV_DATA_TYPE_M001_NEARESTLINK2				("int")						// �����Ƃ��߂������N
#define CSV_DATA_TYPE_M001_DATASET					("int")						// �擾����

// M002
#define CSV_DATA_CONTENTS_M002_ID					("ID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_M002_LID					("LID")						// ���C��ID
#define CSV_DATA_CONTENTS_M002_SIGNALID				("SignalID")				// �ΏېM��
#define CSV_DATA_CONTENTS_M002_SIGNID				("SignID")					// �ΏەW��
#define CSV_DATA_CONTENTS_M002_WIDTH				("Width")					// ��
#define CSV_DATA_CONTENTS_M002_NEARESTLINK			("NearestLink")				// �����Ƃ��߂������N
#define CSV_DATA_CONTENTS_M002_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_M002_ID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_M002_LID						("int")						// ���C��ID
#define CSV_DATA_TYPE_M002_SIGNALID					("int")						// �ΏېM��
#define CSV_DATA_TYPE_M002_SIGNID					("int")						// �ΏەW��
#define CSV_DATA_TYPE_M002_WIDTH					("float")					// ��
#define CSV_DATA_TYPE_M002_NEARESTLINK				("int")						// �����Ƃ��߂������N
#define CSV_DATA_TYPE_M002_DATASET					("int")						// �擾����

// M003
#define CSV_DATA_CONTENTS_M003_ID					("ID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_M003_AID					("AID")						// �G���AID
#define CSV_DATA_CONTENTS_M003_NEARESTLINK			("NearestLink")				// �����Ƃ��߂������N
#define CSV_DATA_CONTENTS_M003_TYPE					("Type")					// ���
#define CSV_DATA_CONTENTS_M003_OUTERAID				("OuterAID")				// ����ID
#define CSV_DATA_CONTENTS_M003_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_M003_ID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_M003_AID						("int")						// �G���AID
#define CSV_DATA_TYPE_M003_NEARESTLINK				("int")						// �����Ƃ��߂������N
#define CSV_DATA_TYPE_M003_TYPE						("int")						// ���
#define CSV_DATA_TYPE_M003_OUTERAID					("int")						// ����ID
#define CSV_DATA_TYPE_M003_DATASET					("int")						// �擾����

// R006
#define CSV_DATA_NUM_R006_NEARAREA					(6)							// NearArea�̐�

#define CSV_DATA_CONTENTS_R006_ID					("ID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_R006_AID					("AID")						// �G���AID
#define CSV_DATA_CONTENTS_R006_NEARESTLINK			("NearestLink")				// �����Ƃ��߂������N
#define CSV_DATA_CONTENTS_R006_NEARAREA1			("NearArea1")				// �אڃG���A
#define CSV_DATA_CONTENTS_R006_NEARAREA2			("NearArea2")				// �אڃG���A
#define CSV_DATA_CONTENTS_R006_NEARAREA3			("NearArea3")				// �אڃG���A
#define CSV_DATA_CONTENTS_R006_NEARAREA4			("NearArea4")				// �אڃG���A
#define CSV_DATA_CONTENTS_R006_NEARAREA5			("NearArea5")				// �אڃG���A
#define CSV_DATA_CONTENTS_R006_NEARAREA6			("NearArea6")				// �אڃG���A
#define CSV_DATA_CONTENTS_R006_TYPE					("Type")					// ���
#define CSV_DATA_CONTENTS_R006_DATASET				("Dataset")					// �擾����

#define CSV_DATA_TYPE_R006_ID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_R006_AID						("int")						// �G���AID
#define CSV_DATA_TYPE_R006_NEARESTLINK				("int")						// �����Ƃ��߂������N
#define CSV_DATA_TYPE_R006_NEARAREA1				("int")						// �אڃG���A
#define CSV_DATA_TYPE_R006_NEARAREA2				("int")						// �אڃG���A
#define CSV_DATA_TYPE_R006_NEARAREA3				("int")						// �אڃG���A
#define CSV_DATA_TYPE_R006_NEARAREA4				("int")						// �אڃG���A
#define CSV_DATA_TYPE_R006_NEARAREA5				("int")						// �אڃG���A
#define CSV_DATA_TYPE_R006_NEARAREA6				("int")						// �אڃG���A
#define CSV_DATA_TYPE_R006_TYPE						("int")						// ���
#define CSV_DATA_TYPE_R006_DATASET					("int")						// �擾����

// R008
#define CSV_DATA_NUM_R008_SL						(40)						// ������~���̐�

#define CSV_DATA_CONTENTS_R008_IID					("IID")						// ���ʔԍ�
#define CSV_DATA_CONTENTS_R008_TYPE					("TYPE")					// �����_���
#define CSV_DATA_CONTENTS_R008_INFOGID				("INFOGID")					// �Ώۈē��Q
#define CSV_DATA_CONTENTS_R008_SL01					("SL01")					// ������~��1
#define CSV_DATA_CONTENTS_R008_SL02					("SL02")					// ������~��2
#define CSV_DATA_CONTENTS_R008_SL03					("SL03")					// ������~��3
#define CSV_DATA_CONTENTS_R008_SL04					("SL04")					// ������~��4
#define CSV_DATA_CONTENTS_R008_SL05					("SL05")					// ������~��5
#define CSV_DATA_CONTENTS_R008_SL06					("SL06")					// ������~��6
#define CSV_DATA_CONTENTS_R008_SL07					("SL07")					// ������~��7
#define CSV_DATA_CONTENTS_R008_SL08					("SL08")					// ������~��8
#define CSV_DATA_CONTENTS_R008_SL09					("SL09")					// ������~��9
#define CSV_DATA_CONTENTS_R008_SL10					("SL10")					// ������~��10
#define CSV_DATA_CONTENTS_R008_SL11					("SL11")					// ������~��11
#define CSV_DATA_CONTENTS_R008_SL12					("SL12")					// ������~��12
#define CSV_DATA_CONTENTS_R008_SL13					("SL13")					// ������~��13
#define CSV_DATA_CONTENTS_R008_SL14					("SL14")					// ������~��14
#define CSV_DATA_CONTENTS_R008_SL15					("SL15")					// ������~��15
#define CSV_DATA_CONTENTS_R008_SL16					("SL16")					// ������~��16
#define CSV_DATA_CONTENTS_R008_SL17					("SL17")					// ������~��17
#define CSV_DATA_CONTENTS_R008_SL18					("SL18")					// ������~��18
#define CSV_DATA_CONTENTS_R008_SL19					("SL19")					// ������~��19
#define CSV_DATA_CONTENTS_R008_SL20					("SL20")					// ������~��20
#define CSV_DATA_CONTENTS_R008_SL21					("SL21")					// ������~��21
#define CSV_DATA_CONTENTS_R008_SL22					("SL22")					// ������~��22
#define CSV_DATA_CONTENTS_R008_SL23					("SL23")					// ������~��23
#define CSV_DATA_CONTENTS_R008_SL24					("SL24")					// ������~��24
#define CSV_DATA_CONTENTS_R008_SL25					("SL25")					// ������~��25
#define CSV_DATA_CONTENTS_R008_SL26					("SL26")					// ������~��26
#define CSV_DATA_CONTENTS_R008_SL27					("SL27")					// ������~��27
#define CSV_DATA_CONTENTS_R008_SL28					("SL28")					// ������~��28
#define CSV_DATA_CONTENTS_R008_SL29					("SL29")					// ������~��29
#define CSV_DATA_CONTENTS_R008_SL30					("SL30")					// ������~��30
#define CSV_DATA_CONTENTS_R008_SL31					("SL31")					// ������~��31
#define CSV_DATA_CONTENTS_R008_SL32					("SL32")					// ������~��32
#define CSV_DATA_CONTENTS_R008_SL33					("SL33")					// ������~��33
#define CSV_DATA_CONTENTS_R008_SL34					("SL34")					// ������~��34
#define CSV_DATA_CONTENTS_R008_SL35					("SL35")					// ������~��35
#define CSV_DATA_CONTENTS_R008_SL36					("SL36")					// ������~��36
#define CSV_DATA_CONTENTS_R008_SL37					("SL37")					// ������~��37
#define CSV_DATA_CONTENTS_R008_SL38					("SL38")					// ������~��38
#define CSV_DATA_CONTENTS_R008_SL39					("SL39")					// ������~��39
#define CSV_DATA_CONTENTS_R008_SL40					("SL40")					// ������~��40

#define CSV_DATA_TYPE_R008_IID						("int")						// ���ʔԍ�
#define CSV_DATA_TYPE_R008_TYPE						("int")						// �����_���
#define CSV_DATA_TYPE_R008_INFOGID					("int")						// �Ώۈē��Q
#define CSV_DATA_TYPE_R008_SL01						("int")						// ������~��1
#define CSV_DATA_TYPE_R008_SL02						("int")						// ������~��2
#define CSV_DATA_TYPE_R008_SL03						("int")						// ������~��3
#define CSV_DATA_TYPE_R008_SL04						("int")						// ������~��4
#define CSV_DATA_TYPE_R008_SL05						("int")						// ������~��5
#define CSV_DATA_TYPE_R008_SL06						("int")						// ������~��6
#define CSV_DATA_TYPE_R008_SL07						("int")						// ������~��7
#define CSV_DATA_TYPE_R008_SL08						("int")						// ������~��8
#define CSV_DATA_TYPE_R008_SL09						("int")						// ������~��9
#define CSV_DATA_TYPE_R008_SL10						("int")						// ������~��10
#define CSV_DATA_TYPE_R008_SL11						("int")						// ������~��11
#define CSV_DATA_TYPE_R008_SL12						("int")						// ������~��12
#define CSV_DATA_TYPE_R008_SL13						("int")						// ������~��13
#define CSV_DATA_TYPE_R008_SL14						("int")						// ������~��14
#define CSV_DATA_TYPE_R008_SL15						("int")						// ������~��15
#define CSV_DATA_TYPE_R008_SL16						("int")						// ������~��16
#define CSV_DATA_TYPE_R008_SL17						("int")						// ������~��17
#define CSV_DATA_TYPE_R008_SL18						("int")						// ������~��18
#define CSV_DATA_TYPE_R008_SL19						("int")						// ������~��19
#define CSV_DATA_TYPE_R008_SL20						("int")						// ������~��20
#define CSV_DATA_TYPE_R008_SL21						("int")						// ������~��21
#define CSV_DATA_TYPE_R008_SL22						("int")						// ������~��22
#define CSV_DATA_TYPE_R008_SL23						("int")						// ������~��23
#define CSV_DATA_TYPE_R008_SL24						("int")						// ������~��24
#define CSV_DATA_TYPE_R008_SL25						("int")						// ������~��25
#define CSV_DATA_TYPE_R008_SL26						("int")						// ������~��26
#define CSV_DATA_TYPE_R008_SL27						("int")						// ������~��27
#define CSV_DATA_TYPE_R008_SL28						("int")						// ������~��28
#define CSV_DATA_TYPE_R008_SL29						("int")						// ������~��29
#define CSV_DATA_TYPE_R008_SL30						("int")						// ������~��30
#define CSV_DATA_TYPE_R008_SL31						("int")						// ������~��31
#define CSV_DATA_TYPE_R008_SL32						("int")						// ������~��32
#define CSV_DATA_TYPE_R008_SL33						("int")						// ������~��33
#define CSV_DATA_TYPE_R008_SL34						("int")						// ������~��34
#define CSV_DATA_TYPE_R008_SL35						("int")						// ������~��35
#define CSV_DATA_TYPE_R008_SL36						("int")						// ������~��36
#define CSV_DATA_TYPE_R008_SL37						("int")						// ������~��37
#define CSV_DATA_TYPE_R008_SL38						("int")						// ������~��38
#define CSV_DATA_TYPE_R008_SL39						("int")						// ������~��39
#define CSV_DATA_TYPE_R008_SL40						("int")						// ������~��40

//------------------
// ���W�ϊ��v�Z�Ŏg�p����l
//------------------
#define HTZ_REF_ID									(9)							// ���W�ϊ��Ŏg�p����n���ID

// �e�n��ʂ̒��S�ܓx�o�x
#define HTZ_REF_DMS_NUM								(19)								// �_�~�[��������HtzRef�̃f�[�^��

#define HTZ_REF_DMS_00								("0.000000000 0.000000000")			// �_�~�[
#define HTZ_REF_DMS_01								("129.300000000 33.000000000")		//  1 ���茧 ���������̂����k���k��32�x����k��27�x�������o128�x18���������o130�x�����E���Ƃ�������i�����Q���͓��o130�x13���܂ł��܂ށB)�ɂ��邷�ׂĂ̓��A�����A�ʋy�ъ�� 
#define HTZ_REF_DMS_02								("131.000000000 33.000000000")		//  2 �������@���ꌧ�@�F�{���@�啪���@�{�茧�@���������iI�n�ɋK�肷����������B) 
#define HTZ_REF_DMS_03								("132.100000000 36.000000000")		//  3 �R�����@�������@�L���� 
#define HTZ_REF_DMS_04								("133.300000000 33.000000000")		//  4 ���쌧�@���Q���@�������@���m�� 
#define HTZ_REF_DMS_05								("134.200000000 36.000000000")		//  5 ���Ɍ��@���挧�@���R�� 
#define HTZ_REF_DMS_06								("136.000000000 36.000000000")		//  6 ���s�{�@���{�@���䌧�@���ꌧ�@�O�d���@�ޗǌ� �a�̎R�� 
#define HTZ_REF_DMS_07								("137.100000000 36.000000000")		//  7 �ΐ쌧�@�x�R���@�򕌌��@���m�� 
#define HTZ_REF_DMS_08								("138.300000000 36.000000000")		//  8 �V�����@���쌧�@�R�����@�É��� 
#define HTZ_REF_DMS_09								("139.500000000 36.000000000")		//  9 �����s�iXIV�n�AXVIII�n�y��XIX�n�ɋK�肷����������B)�@�������@�Ȗ،��@��錧�@��ʌ� ��t�� �Q�n���@�_�ސ쌧 
#define HTZ_REF_DMS_10								("140.500000000 40.000000000")		// 10 �X���@�H�c���@�R�`���@��茧�@�{�錧 
#define HTZ_REF_DMS_11								("140.150000000 44.000000000")		// 11 ���M�s�@���َs�@�ɒB�s�@�k�l�s�@�k�C����u�����U���ǂ̏��ǋ��@�k�C���_�U�����U���ǂ̏��ǋ��̂����L�Y���A�s�˒��y�ѓ���Β��@�k�C���n�������U���ǂ̏��ǋ��@�k�C���w�R�U���ǂ̏��ǋ��
#define HTZ_REF_DMS_12								("142.150000000 44.000000000")		// 12 �k�C���iXI�n�y��XIII�n�ɋK�肷����������B�j
#define HTZ_REF_DMS_13								("144.150000000 44.000000000")		// 13 �k���s�@�эL�s�@���H�s�@�ԑ��s�@�����s�@�k�C���I�z�[�c�N�����U���ǂ̏��ǋ��̂������y���A�Õʒ��A�Η����A�������A���������A�P�q�{���A�u�˒��A���C�Ԓ��y�ё�󒬁@�k�C���\�������U���ǂ̏��ǋ��@�k�C�����H�����U���ǂ̏��ǋ��@�k�C�������U���ǂ̏��ǋ�� 
#define HTZ_REF_DMS_14								("142.000000000 26.000000000")		// 14 �����s�̂����k��28�x�����ł���A�����o140�x30�����瓌�ł��蓌�o143�x���琼�ł����� 
#define HTZ_REF_DMS_15								("127.300000000 26.000000000")		// 15 ���ꌧ�̂������o126�x���瓌�ł���A�����o130�x���琼�ł����� 
#define HTZ_REF_DMS_16								("124.000000000 26.000000000")		// 16 ���ꌧ�̂������o126�x���琼�ł����� 
#define HTZ_REF_DMS_17								("131.000000000 26.000000000")		// 17 ���ꌧ�̂������o130�x���瓌�ł����� 
#define HTZ_REF_DMS_18								("136.000000000 20.000000000")		// 18 �����s�̂����k��28�x�����ł���A�����o140�x30�����琼�ł����� 
#define HTZ_REF_DMS_19								("154.000000000 26.000000000")		// 19 �����s�̂����k��28�x�����ł���A�����o143�x���瓌�ł�����

//////////////////////////////////////////////////////////////////////////////
//	struct																	//
//////////////////////////////////////////////////////////////////////////////
//------------------
// ���̓f�[�^
//------------------

// D01
typedef struct CSV_DATA_VAL_D01
{
	int		m_nPID;									//!< ���ʔԍ�
	double	m_dB;									//!< �ʒu�F�ܓx
	double	m_dL;									//!< �ʒu�F�o�x
	double	m_dH;									//!< �ʒu�F����
	double	m_dBx;									//!< �ʒu�Fx
	double	m_dLy;									//!< �ʒu�F��
	int		m_nRef;									//!< ���ʒ��p���W�n
	int		m_nMCODE1;								//!< 1�����b�V���R�[�h
	int		m_nMCODE2;								//!< 2�����b�V���R�[�h
	int		m_nMCODE3;								//!< 3�����b�V���R�[�h
	int		m_nGround;								//!< �n�\�_��
	int		m_nDataset;								//!< �擾����
}CSV_DATA_VAL_D01;

// D02
typedef struct CSV_DATA_VAL_D02
{
	int		m_nLID;									//!< ���ʔԍ�
	int		m_nBPT;									//!< �O�|�C���gID
	int		m_nFPT;									//!< ��|�C���gID
	int		m_nBLN;									//!< �O���C��ID
	int		m_nFLN;									//!< �ド�C��ID
	int		m_nPID;									//!< �~�ʏ��1�_
	int		m_nInvisibleFG;							//!< �A��FG
	int		m_nDataset;								//!< �擾����
}CSV_DATA_VAL_D02;

// M002
typedef struct CSV_DATA_VAL_M002
{
	int		m_nID;									//!< ���ʔԍ�
	int		m_nLID;									//!< ���C��ID
	int		m_nSignalID;							//!< �ΏېM��
	int		m_nSignID;								//!< �ΏەW��
	double	m_dWidth;								//!< ��
	int		m_nNearestLink;							//!< �����Ƃ��߂������N
	int		m_nDataset;								//!< �擾����
}CSV_DATA_VAL_M002;

#endif // __CSV_DEFINE_H__

////////////////////////////////////////////////////////////////////////////////
//	EOF		CsvDefine.h
////////////////////////////////////////////////////////////////////////////////
