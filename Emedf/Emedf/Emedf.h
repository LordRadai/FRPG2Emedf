#pragma once
#include <string>
#include <vector>
#include <nlohmann/json.hpp>
#include "Class.h"
#include "Enum.h"

namespace Emedf
{
	class Emedf
	{
		nlohmann::ordered_json m_json;
		std::vector<Class*> m_mainClasses;
		std::vector<Class*> m_extraClasses;
		std::vector<Enum*> m_enums;
	public:
		Emedf() {}
		~Emedf() {}

		void loadFromJson(const std::wstring& path);
		void saveToJson(const std::wstring& path);

		Class* findMainClass(int id);
		Class* findMainClass(const std::string& name);
		std::vector<Class*>& getMainClasses() { return m_mainClasses; }
		void addMainClass(Class* mainClass);

		Class* findExtraClass(int id);
		Class* findExtraClass(const std::string& name);
		std::vector<Class*>& getExtraClasses() { return m_extraClasses; }
		void addExtraClass(Class* extraClass);

		std::vector<Enum*>& getEnums() { return m_enums; }
		void addEnum(Enum* e);
		Enum* findEnum(const std::string& name);
	};
}