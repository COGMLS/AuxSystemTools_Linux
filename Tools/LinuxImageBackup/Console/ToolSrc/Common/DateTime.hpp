#pragma once

#ifndef DATE_TIME_HPP
#define DATE_TIME_HPP

#include <string>
#include <cstring>
#include <ctime>
#include <chrono>
#include <ostream>

/**
 * @brief Class to holds Date and Time information in a single object
 */
class DateTimeInfo
{
	private:

		std::chrono::year_month_day calendar;
		std::chrono::weekday weekday;
		int hours;
		int minutes;
		int seconds;

	public:

		/**
		 * @brief Create a Date and Time object that holds the actual date and time
		 */
		DateTimeInfo();

		/**
		 * @brief Create a Date and Time object that will holds an specific date with time 00:00:00
		 * @param year Year value
		 * @param month Month value
		 * @param day Day value
		 */
		DateTimeInfo (int year, int month, int day);

		/**
		 * @brief Create a Date and Time object that will holds an specific date and time
		 * @param year Year value
		 * @param month Month value
		 * @param day Day value
		 * @param hours Hours value
		 * @param minutes Minutes value
		 * @param seconds Seconds value
		 */
		DateTimeInfo (int year, int month, int day, int hours, int minutes, int seconds);

		DateTimeInfo (const DateTimeInfo& other);

		DateTimeInfo (DateTimeInfo&& other) noexcept;

		~DateTimeInfo();

		/**
		 * @brief Generate an formatted string using ISO 8601 by default.
		 * @param exportDate Export the date information
		 * @param exportTime Export the time information
		 * @param compatibleWithFs Export the information compatible with filesystems, changing ':' and '/' to '-'
		 */
		std::string to_string(bool exportDate = true, bool exportTime = true, bool compatibleWithFs = false);

		/**
		 * @brief Get an specific value from the object
		 * @param info_id Information ID
		 * @return Value corresponding with the ID.
		 * @return If return -1, it means an unknown ID was inserted
		 * @note The info_id can be 0: Year, 1: Month, 2: Day, 3: Hours, 4: Minutes, 5: Seconds, 6: Weekday (in C format).
		 */
		int getDateTimeComponent(unsigned char info_id);

		/**
		 * @brief Verify if the date and time information are valid
		 */
		bool isValid();

		bool operator== (DateTimeInfo& other);
		
		bool operator!= (DateTimeInfo& other);

		DateTimeInfo& operator= (const DateTimeInfo& other);

		DateTimeInfo& operator= (DateTimeInfo&& other) noexcept;

		friend std::ostream& operator<< (std::ostream& os, DateTimeInfo& dt_info);
};

#endif // !DATE_TIME_HPP