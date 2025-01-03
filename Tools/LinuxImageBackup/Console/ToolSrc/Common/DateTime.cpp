#include "DateTime.hpp"

DateTimeInfo::DateTimeInfo()
{
	std::chrono::time_point now = std::chrono::system_clock::now();
	this->calendar = std::chrono::floor<std::chrono::days>(now);
	std::time_t c_time_into = std::chrono::system_clock::to_time_t(now);
	std::tm* time = std::localtime(&c_time_into);
	this->hours = time->tm_hour;
	this->minutes = time->tm_min;
	this->seconds = time->tm_sec;
	this->weekday = std::chrono::weekday(time->tm_wday);
}

DateTimeInfo::DateTimeInfo(int year, int month, int day)
{
	std::chrono::time_point now = std::chrono::system_clock::now();
	this->calendar = std::chrono::year_month_day(
			std::chrono::year(year),
			std::chrono::month(month),
			std::chrono::day(day)
		);
	std::time_t c_time_into = std::chrono::system_clock::to_time_t(now);
	std::tm* time = std::localtime(&c_time_into);
	this->hours = 0;
	this->minutes = 0;
	this->seconds = 0;
	this->weekday = std::chrono::weekday(time->tm_wday);
}

DateTimeInfo::DateTimeInfo(int year, int month, int day, int hours, int minutes, int seconds)
{
	std::chrono::time_point now = std::chrono::system_clock::now();
	this->calendar = std::chrono::year_month_day(
			std::chrono::year(year),
			std::chrono::month(month),
			std::chrono::day(day)
		);
	std::time_t c_time_into = std::chrono::system_clock::to_time_t(now);
	std::tm* time = std::localtime(&c_time_into);
	this->hours = hours;
	this->minutes = minutes;
	this->seconds = seconds;
	this->weekday = std::chrono::weekday(time->tm_wday);
}

DateTimeInfo::DateTimeInfo(const DateTimeInfo &other)
{
	this->calendar = other.calendar;
	this->weekday = other.weekday;
	this->hours = other.hours;
	this->minutes = other.minutes;
	this->seconds = other.seconds;
}

DateTimeInfo::DateTimeInfo(DateTimeInfo &&other) noexcept
{
	this->calendar = std::move(other.calendar);
	this->weekday = std::move(other.weekday);
	this->hours = std::move(other.hours);
	this->minutes = std::move(other.minutes);
	this->seconds = std::move(other.seconds);
}

DateTimeInfo::~DateTimeInfo()
{
}

std::string DateTimeInfo::to_string(bool exportDate, bool exportTime, bool compatibleWithFs)
{
    std::string dtInfoStr;
	char dateSeparator = '/';
	char timeSeparator = ':';

	if (compatibleWithFs)
	{
		dateSeparator = '-';
		timeSeparator = '-';
	}

	if (exportDate)
	{
		dtInfoStr += (int)this->calendar.year();
		dtInfoStr += dateSeparator;
		dtInfoStr += (unsigned int)this->calendar.month();
		dtInfoStr += dateSeparator;
		dtInfoStr += (unsigned int)this->calendar.day();
	}

	if (exportDate && exportTime)
	{
		if (compatibleWithFs)
		{
			dtInfoStr += 'T';
		}
		else
		{
			dtInfoStr += ' ';
		}
	}

	if (exportTime)
	{
		if (this->hours < 10)
		{
			dtInfoStr += '0';
		}
		dtInfoStr += std::to_string(this->hours);
		dtInfoStr += timeSeparator;
		if (this->minutes < 10)
		{
			dtInfoStr += '0';
		}
		dtInfoStr += std::to_string(this->minutes);
		dtInfoStr += timeSeparator;
		if (this->seconds < 10)
		{
			dtInfoStr += '0';
		}
		dtInfoStr += std::to_string(this->seconds);
	}

	return dtInfoStr;
}

int DateTimeInfo::getDateTimeComponent(unsigned char info_id)
{
    switch (info_id)
	{
		case 0:
		{
			return (int)this->calendar.year();
		}
		case 1:
		{
			return static_cast<int>((unsigned int)this->calendar.month());
		}
		case 2:
		{
			return static_cast<int>((unsigned int)this->calendar.day());
		}
		case 3:
		{
			return this->hours;
		}
		case 4:
		{
			return this->minutes;
		}
		case 5:
		{
			return this->seconds;
		}
		case 6:
		{
			return static_cast<int>(this->weekday.c_encoding());
		}
		default:
		{
			return -1;
		}
	}
}

bool DateTimeInfo::isValid()
{
	return this->calendar.ok() && this->weekday.ok() && this->hours >= 0 && this->hours < 24 && this->minutes >= 0 && this->minutes < 60 && this->seconds >= 0 && this->seconds < 60;
}

bool DateTimeInfo::operator==(DateTimeInfo &other)
{
    return this->calendar == other.calendar && this->weekday == other.weekday && this->hours == other.hours && this->minutes == other.minutes && this->seconds == other.seconds;
}

bool DateTimeInfo::operator!=(DateTimeInfo &other)
{
    return !(*this == other);
}

DateTimeInfo &DateTimeInfo::operator=(const DateTimeInfo &other)
{
    this->calendar = other.calendar;
	this->weekday = other.weekday;
	this->hours = other.hours;
	this->minutes = other.minutes;
	this->seconds = other.seconds;

	return *this;
}

DateTimeInfo &DateTimeInfo::operator=(DateTimeInfo &&other) noexcept
{
	if (this == &other)
	{
		return *this;
	}
	
    this->calendar = std::move(other.calendar);
	this->weekday = std::move(other.weekday);
	this->hours = std::move(other.hours);
	this->minutes = std::move(other.minutes);
	this->seconds = std::move(other.seconds);

	return *this;
}

std::ostream &operator<<(std::ostream &os, DateTimeInfo &dt_info)
{
	os << dt_info.to_string();
	return os;
}
