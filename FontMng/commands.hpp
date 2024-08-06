#pragma once

#ifndef COMMANDS_HPP
#define COMMANDS_HPP

#include <string>
#include <vector>
#include <array>

#include "constants.hpp"

// Command library types:

/**
 * @brief Command Type Enumerator used to facilitate the command identification
 */
enum CMDTYPE : int
{
	UNKNOWN_CMD = -2,
	ARGUMENT = -1,
	HELP_CMD,
	LIST_CMD,
	ADD_CMD,
	REMOVE_CMD,
	EXIT_CMD
};


/**
 * @brief Constant Command Array used to determinate the command in Command Class.
 * @note The command strings need have exactly the same index as the CMDTYPE.
 */
const std::array<std::wstring, 5> cmdArr = 
{
	L"help",
	L"list",
	L"add",
	L"remove",
	L"exit"
};

/**
 * @brief Command Class used to create objects that can represent a command or a command argument
 */
class cmd
{
	private:

		std::wstring cmdValue;
		CMDTYPE type;

	public:

		/**
		 * @brief Create a Command Object that can represent a application command or an argument for one of the commands available.
		 * @param cmd String command that will be interpreted as a possible command.
		 */
		cmd (std::wstring cmd);

		cmd (const cmd& other);
		cmd (cmd&& other) noexcept;

		~cmd();

		cmd& operator=(const cmd& other);
		cmd& operator=(cmd&& other) noexcept;

		friend bool operator==(cmd& lhs, cmd& rhs);
		friend bool operator==(cmd& other, CMDTYPE type);

		friend std::wostream& operator<< (std::wostream& os, const cmd& obj);

		/**
		 * @brief Get the value inside the command object
		 * @return Return the string given to create the command object
		 */
		std::wstring getValue();

		/**
		 * @brief Get the type of command this object is representing.
		 */
		CMDTYPE getType();
};

// Functions for check commands:

std::vector<cmd> getCmdList (std::wstring cmdLine);


// Command functions:

void help_cmd();
void help_cmd(cmd hCmd);
void list_cmd();
void install_cmd();
void remove_cmd();

#endif // !COMMANDS_HPP