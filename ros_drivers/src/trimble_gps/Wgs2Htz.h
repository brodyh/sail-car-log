////////////////////////////////////////////////////////////////////////////////
//! @file		Wgs2Htz.h
//! @brief		Wgs2Htz
//! @details	���W�ϊ��v�Z�p�N���X
//! @date		2013/09/06 Create
//! @author		FSI Hidetaka Kawamura
//
//  Copyright 2013 NISSAN MOTOR CO.,LTD.
////////////////////////////////////////////////////////////////////////////////

#ifndef __WGS_2_HTZ_H__
#define __WGS_2_HTZ_H__

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <string>
#include <vector>
using namespace std;

//==============================================================================
//! @brief		���W�ϊ��v�Z�p�N���X
//==============================================================================
class CWgs2Htz
{
//------------------
// struct
//------------------
private:
	//==============================================================================
	//! @brief			DMS�\�����W�n
	//! @details		DMS�\�����W�n
	//==============================================================================
	typedef struct _DMS
	{
		string		strLongitude;		// �o�x
		string		strLatitude;		// �ܓx
	} DMS;

	//==============================================================================
	//! @brief			Rad�\�����W�n
	//! @details		Rad�\�����W�n
	//==============================================================================
	typedef struct _RAD
	{
		double		dLongitude;			// �o�x
		double		dLatitude;			// �ܓx
	} RAD;

//--------------
// method
//--------------
public:
	// �C���X�^���X����
    static CWgs2Htz* GetInstance()
    {
    	if( m_poInstance == NULL )
		{
    		m_poInstance = new CWgs2Htz();
    	}
    	return m_poInstance;
    }

	// �C���X�^���X�폜
	static void DeleteInstance()
	{
		if( m_poInstance != NULL )
		{
			delete m_poInstance;
    		m_poInstance = NULL;
    	}
    	return;
	}

	//-----------------------------------
	// Constructor Destructor
	//-----------------------------------
//private:
public: //changed by Yuta 
	CWgs2Htz(void);
	~CWgs2Htz(void);

    //-----------------------------------
    // operator
    //-----------------------------------

    //-----------------------------------
    // AccessMethod
    //-----------------------------------
public:
	// �ܓx�o�x���畽�ʒ��p���W�n�ɍ��W�ϊ�
	void ToHtz(const double dBreiteDeg, const double dLaengeDeg, double& dOutX, double& dOutY) const;
	// �ܓx�o�x���畽�ʒ��p���W�n�ɍ��W�ϊ��iRefId��ʎw��j
	void ToHtzRefId(const double dBreiteDeg, const double dLaengeDeg, const int nRefId, double& dOutX, double& dOutY) const;
	// ���_���W�̐ݒ�
	void SetBasePoint(const double dLatitude, const double dLongitude);
	//setZero heading
	void SetZeroHeading(const double dLatitude,const double dLongitude );
	
	// ����1m�ړ��������̌o�x�ω��ʂ��擾
	double GetLongitudePerMeter(void) const;
	// �k��1m�ړ��������̈ܓx�ω��ʂ��擾
	double GetLatitudePerMeter(void) const;
	// ����1�x�ړ��������̃��[�g���ω��ʂ��擾
	double GetMeterPerLongitude(void) const;
	// �k��1�x�ړ��������̃��[�g���ω��ʂ��擾
	double GetMeterPerLatitude(void) const;
	
	double GetLocalZeroHeading(void) const;
	//-----------------------------------
	// Method
	//-----------------------------------
	// �x���\������x���b�\���ɕύX
	string Deg2Dms(const double dDeg) const;
	// �x���b�\������x���\���ɕϊ�
	double Dms2Deg(const string strDms) const;
	// �x���\�����烉�W�A���\���ɕϊ�
	double Deg2Rad(const double dDeg) const;
private:
	// �ܓx�o�x���畽�ʒ��p���W�n�ɍ��W�ϊ�
	void ConvertWgs2Htz(const double dBreiteDeg, const double dLaengeDeg, const int nRefId, double& dOutX, double& dOutY) const;
	// ���W�ϊ��Ŏg�p����l��\�ߌv�Z���Ă����֐�
	void SetConvertParam(void);
	// ���ʒ��p���W�n�Ŏg�p����n�ԍ��ʂ̌��_���W�e�[�u���̍쐬
	void SetHtzTable(void);
	// ���ʒ��p���W�n�̌��_���W�̈ܓx�o�x�����W�A���̒l�Őݒ�
	void SetHtzTablePart(const string strDmsTxt);

//--------------
// data
//--------------
private:
    static CWgs2Htz*			m_poInstance;					// �B��̃C���X�^���X

	int							m_nRefId;						// ���ʒ��p���W�n�Ŏg�p����n�ԍ�
	vector<RAD>					m_stHtzRefRad;					// �n�ԍ��ʂ̌��_���W�e�[�u���i���W�A���\���j

	bool						m_bIsDefinedBasePoint;			// ���_���W��ݒ�ς݂��ǂ���
	double						m_oBasePointLon;				// ���ʒ��p���W�n�̌��_�̌o�x
	double						m_oBasePointLat;				// ���ʒ��p���W�n�̌��_�̈ܓx
	double						m_oBasePointLonRad;				// ���ʒ��p���W�n�̌��_�̌o�x�i���W�A���\���j
	double						m_oBasePointLatRad;				// ���ʒ��p���W�n�̌��_�̈ܓx�i���W�A���\���j
	
	bool						m_bIsDefinedSecondPoint;			// ���_���W��ݒ�ς݂��ǂ���
	double						m_oSecondPointLon;				// ���ʒ��p���W�n�̌��_�̌o�x
	double						m_oSecondPointLat;				// ���ʒ��p���W�n�̌��_�̈ܓx
	double						m_oSecondPointLonRad;				// ���ʒ��p���W�n�̌��_�̌o�x�i���W�A���\���j
	double						m_oSecondPointLatRad;				// ���ʒ��p���W�n�̌��_�̈ܓx�i���W�A���\���j

	double						m_oBaseLocalZeroHeading;			// Local Zero Heading

	double						m_dLonPerMeter;					// y����1���[�g���ړ����̌o�x�̑���
	double						m_dLatPerMeter;					// x����1���[�g���ړ����̈ܓx�̑���

	double						m_dMeterPerLon;					// �o�x1�x�ړ�����y�������[�g���̑���
	double						m_dMeterPerLat;					// �ܓx1�x�ړ�����x�������[�g���̑���

	// �ȉ��A���W�ϊ��v�Z�p�̌Œ�l
	double						m_dC;							// �ɂł̋ɗ����a
	double						m_dE1;							// ��ꗣ�S��
	double						m_dE2;							// ��񗣐S��

	double						m_dB1;							// ���W�ϊ��̓r���v�Z�p�p�����[�^
	double						m_dB2;							// �@�@�V
	double						m_dB3;							// �@�@�V
	double						m_dB4;							// �@�@�V
	double						m_dB5;							// �@�@�V
	double						m_dB6;							// �@�@�V
	double						m_dB7;							// �@�@�V
	double						m_dB8;							// �@�@�V
	double						m_dB9;							// �@�@�V
};

#endif //__WGS_2_HTZ_H__

////////////////////////////////////////////////////////////////////////////////
//	EOF		Wgs2Htz.h
////////////////////////////////////////////////////////////////////////////////
