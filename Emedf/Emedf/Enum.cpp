#include "Enum.h"

namespace Emedf
{
	Enum::Enum(nlohmann::ordered_json& json) : m_json(json)
	{
		for (auto& valueJson : m_json["values"].items())
		{
			int value = std::stoi(valueJson.key());
			std::string str = valueJson.value().get<std::string>();

			m_values.push_back(new EnumValue(str, value));
		}
	}

	void Enum::addValue(int value, std::string str)
	{
        std::string key = std::to_string(value);
        m_json["values"][key] = str;

        m_values.push_back(new EnumValue(str, value));
	}

	EnumValue* Enum::findValue(int value)
	{
		for (EnumValue* enumValue : m_values)
		{
			if (enumValue->getValue() == value)
				return enumValue;
		}

		return nullptr;
	}

	EnumValue* Enum::findValue(const std::string& name)
	{
		for (EnumValue* enumValue : m_values)
		{
			if (enumValue->getName() == name)
				return enumValue;
		}

		return nullptr;
	}

	int Enum::getValueByName(const std::string& name)
	{
		for (EnumValue* enumValue : m_values)
		{
			if (enumValue->getName() == name)
				return enumValue->getValue();
		}

		throw std::runtime_error("Enum value not found for name: " + name);
	}

	std::string Enum::getNameByValue(int value)
	{
		for (EnumValue* enumValue : m_values)
		{
			if (enumValue->getValue() == value)
				return enumValue->getName();
		}

		throw std::runtime_error("Enum name not found for value: " + std::to_string(value));
	}
}