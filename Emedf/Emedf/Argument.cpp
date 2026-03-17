#include "Argument.h"

namespace Emedf
{
	void Argument::setFormatString(const std::string& formatString)
	{
		if (formatString.empty())
		{
			switch (getType())
			{
			case kTypeFloat32:
				m_json["format_string"] = "%f";
				break;
			default:
				m_json["format_string"] = "%d";
				break;
			}

			return;
		}

		m_json["format_string"] = formatString;
	}

	std::string Argument::getEnumName()
	{
		if (m_json.contains("enum_name") && !m_json["enum_name"].is_null())
			return m_json["enum_name"].get<std::string>();
		else
			return "";
	}

	bool Argument::isVarargs() const
	{
		return m_json.contains("vararg") && m_json["vararg"].get<bool>();
	}

	size_t Argument::getMemoryRequirements()
	{
		switch (getType())
		{
		case kTypeU8:
		case kTypeS8:
			return 1;
		case kTypeU16:
		case kTypeS16:
			return 2;
		case kTypeU32:
		case kTypeS32:
		case kTypeFloat32:
			return 4;
		default:
			throw std::runtime_error("Unknown argument type: " + std::to_string(getType()));
		}
	}

	void Argument::setEnumName(const std::string& enumName)
	{
		if (enumName.empty())
		{
			m_json["enum_name"] = nullptr;
			return;
		}

		m_json["enum_name"] = enumName;
	}

	const char* Argument::getTypeName(int type)
	{
		switch (type)
		{
		case kTypeU8:
			return "u8";
		case kTypeU16:
			return "u16";
		case kTypeU32:
			return "u32";
		case kTypeS8:
			return "s8";
		case kTypeS16:
			return "s16";
		case kTypeS32:
			return "s32";
		case kTypeFloat32:
			return "float32";
		default:
			return "unknown";
		}
	}

	int Argument::getTypeFromName(const std::string& str)
	{
		if (str == "u8")
			return kTypeU8;
		else if (str == "u16")
			return kTypeU16;
		else if (str == "u32")
			return kTypeU32;
		else if (str == "s8")
			return kTypeS8;
		else if (str == "s16")
			return kTypeS16;
		else if (str == "s32")
			return kTypeS32;
		else if (str == "float32")
			return kTypeFloat32;
		else
			throw std::runtime_error("Unknown type name: " + str);
	}
}