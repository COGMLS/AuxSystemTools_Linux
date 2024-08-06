#include "commands.hpp"

cmd::cmd(std::wstring cmd)
{
	this->cmdValue = cmd;
	this->type = CMDTYPE::UNKNOWN_CMD;

	for (size_t i = 0; i < cmdArr.size(); i++)
	{
		if (cmdArr[i] == this->cmdValue)
		{
			this->type = static_cast<CMDTYPE>(i);
		}
	}

	if (this->type == CMDTYPE::UNKNOWN_CMD)
	{
		this->type = CMDTYPE::ARGUMENT;
	}
}

cmd::cmd(const cmd &other)
{
	this->cmdValue = other.cmdValue;
	this->type = other.type;
}

cmd::cmd(cmd &&other) noexcept
{
	this->cmdValue = std::move(other.cmdValue);
	this->type = std::move(other.type);
}

cmd::~cmd()
{

}

cmd &cmd::operator=(const cmd &other)
{
    this->cmdValue = other.cmdValue;
	this->type = other.type;

	return *this;
}

cmd &cmd::operator=(cmd &&other) noexcept
{
    this->cmdValue = std::move(other.cmdValue);
	this->type = std::move(other.type);

	return *this;
}

bool operator==(cmd &lhs, cmd &rhs)
{
	bool cmdValueEq = lhs.cmdValue == rhs.cmdValue;
	bool cmdTypeEq = lhs.type == rhs.type;

    return cmdValueEq && cmdTypeEq;
}

bool operator==(cmd &other, CMDTYPE type)
{
    return other.type == type;
}

std::wostream &operator<<(std::wostream &os, const cmd &obj)
{
	std::wstring str;

	str += L"[" + std::to_wstring(static_cast<int>(obj.type)) + L"]" + obj.cmdValue;

	os << str;

	return os;
}

std::wstring cmd::getValue()
{
    return this->cmdValue;
}

CMDTYPE cmd::getType()
{
    return this->type;
}

std::vector<cmd> getCmdList(std::wstring cmdLine)
{
    std::vector<cmd> cmdList;

	if (cmdLine.empty())
	{
		return cmdList;
	}

	bool isOpenQuote = false;
	bool isCloseQuote = false;
	size_t openQuotePos = 0;
	size_t closeQuotePos = 0;

	wchar_t c = '\0';
	std::wstring tmp;

	for (size_t i = 0; i < cmdLine.size(); i++)
	{
		c = cmdLine.at(i);

		if (c == SPACE_W)
		{
			if (isOpenQuote && isCloseQuote)
			{
				if (!tmp.empty())
				{
					cmdList.push_back(tmp);
				}

				isOpenQuote = false;
				isCloseQuote = false;
				openQuotePos = 0;
				closeQuotePos = 0;
				tmp.clear();
			}

			if (!openQuotePos && !isCloseQuote)
			{
				if (!tmp.empty())
				{
					cmdList.push_back(tmp);
				}

				tmp.clear();
			}
		}

		if (c == QUOTE_W && isOpenQuote && !isCloseQuote)
		{
			isCloseQuote = true;
			closeQuotePos = i;
		}

		if (c == QUOTE_W && !isOpenQuote && !isCloseQuote)
		{
			isOpenQuote = true;
			openQuotePos = i;
		}

		if (isOpenQuote)
		{
			tmp += c;
		}
		else
		{
			if (c != SPACE_W)
			{
				tmp += c;
			}
		}
	}

	if (!tmp.empty())
	{
		cmdList.push_back(tmp);
		tmp.clear();
	}

	return cmdList;
}

