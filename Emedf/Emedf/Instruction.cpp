#include "Instruction.h"

namespace Emedf
{
	Instruction::Instruction(nlohmann::ordered_json& json) : m_json(json)
	{
		for (auto& argJson : m_json["args"])
		{
			Argument* arg = new Argument(argJson);
			m_arguments.push_back(arg);
		}
	}

	void Instruction::addArgument(Argument* argument)
	{
		m_json["args"].push_back(argument->getJson());
		m_arguments.push_back(argument);
	}

	size_t Instruction::getArgAlignment()
	{
		size_t maxAlignment = 1;

		for (Argument* arg : m_arguments)
		{
			size_t argAlignment = arg->getMemoryRequirements();
			if (argAlignment > maxAlignment)
				maxAlignment = argAlignment;
		}

		return maxAlignment;
	}

	size_t Instruction::getMemoryRequirements()
	{
		size_t totalSize = 0;

		for (Argument* arg : m_arguments)
		{
			size_t argSize = arg->getMemoryRequirements();
			size_t argAlignment = argSize;

			if (totalSize % argAlignment != 0)
				totalSize += argAlignment - (totalSize % argAlignment);

			totalSize += argSize;
		}

		return totalSize;
	}
}