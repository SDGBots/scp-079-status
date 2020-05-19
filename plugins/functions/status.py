# SCP-079-STATUS - Check Linux server status
# Copyright (C) 2019-2020 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-STATUS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from distro import linux_distribution
from platform import uname
from socket import gethostname

from psutil import boot_time, cpu_count, cpu_freq, cpu_percent, disk_partitions, disk_io_counters, net_if_addrs
from psutil import net_io_counters, virtual_memory, swap_memory

from .. import glovar
from .etc import code, get_now, get_readable_time, get_time_str, lang

# Enable logging
logger = logging.getLogger(__name__)


def get_cpu_count_logical(text: str) -> str:
    # Get logical CPU count
    result = text

    try:
        codename = "$cpu_count_logical$"

        if codename not in text:
            return result

        status = str(cpu_count(logical=True))

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu count logical error: {e}", exc_info=True)

    return result


def get_cpu_count_physical(text: str) -> str:
    # Get physical CPU count
    result = text

    try:
        codename = "$cpu_count_physical$"

        if codename not in text:
            return result

        status = str(cpu_count(logical=False))

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu count physical error: {e}", exc_info=True)

    return result


def get_cpu_freq_current(text: str) -> str:
    # Get CPU current frequency
    result = text

    try:
        codename = "$freq_current$"

        if codename not in text:
            return result

        status = f"{cpu_freq().current:.2f} Mhz"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu freq current error: {e}", exc_info=True)

    return result


def get_cpu_usage_total(text: str) -> str:
    # Get CPU total usage
    result = text

    try:
        codename = "$cpu_percent$"

        if codename not in text:
            return result

        status = f"{cpu_percent()}%"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu usage total error: {e}", exc_info=True)

    return result


def get_cpu_usage_per(text: str) -> str:
    # Get CPU per core usage
    result = text

    try:
        codename = "$cpu_percent_per$"

        if codename not in text:
            return result

        status = ""

        for i, percent in enumerate(cpu_percent(percpu=True, interval=1)):
            status += "\t" * 4 + f"{lang('core')}\t{i + 1}{lang('colon')}{code(f'{percent}%')}\n"

        if status:
            status = status[:-1]

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu usage per error: {e}", exc_info=True)

    return result


def get_cpu_freq_max(text: str) -> str:
    # Get CPU max frequency
    result = text

    try:
        codename = "$freq_max$"

        if codename not in text:
            return result

        status = f"{cpu_freq().max:.0f} Mhz"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu freq max error: {e}", exc_info=True)

    return result


def get_cpu_freq_min(text: str) -> str:
    # Get CPU max frequency
    result = text

    try:
        codename = "$freq_min$"

        if codename not in text:
            return result

        status = f"{cpu_freq().min:.0f} Mhz"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get cpu freq min error: {e}", exc_info=True)

    return result


def get_dist(text: str) -> str:
    # Get dist
    result = text

    try:
        codename = "$dist$"

        if codename not in text:
            return result

        status = " ".join(d for d in linux_distribution()[:-1])

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get dist error: {e}", exc_info=True)

    return result


def get_hostname(text: str) -> str:
    # Get the hostname
    result = text

    try:
        codename = "$hostname$"

        if codename not in text:
            return result

        status = gethostname()

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get hostname error: {e}", exc_info=True)

    return result


def get_interval(text: str) -> str:
    # Get update interval
    result = text

    try:
        codename = "$interval$"

        if codename not in text:
            return result

        status = str(glovar.interval)

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get interval error: {e}", exc_info=True)

    return result


def get_kernel(text: str) -> str:
    # Get current kernel
    result = text

    try:
        codename = "$kernel$"

        if codename not in text:
            return result

        status = uname().release

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get kernel error: {e}", exc_info=True)

    return result


def get_last(text: str) -> str:
    # Get last seen time
    result = text

    try:
        codename = "$last$"

        if codename not in text:
            return result

        status = get_readable_time(the_format=glovar.format_date)

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get last error: {e}", exc_info=True)

    return result


def get_mem_available(text: str) -> str:
    # Get available memory
    result = text

    try:
        codename = "$memory_available$"

        if codename not in text:
            return result

        status = str(get_size(virtual_memory().available))

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get mem available error: {e}", exc_info=True)

    return result


def get_mem_percent(text: str) -> str:
    # Get percent memory
    result = text

    try:
        codename = "$memory_percent$"

        if codename not in text:
            return result

        status = f"{virtual_memory().percent}%"

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get mem percent error: {e}", exc_info=True)

    return result


def get_mem_total(text: str) -> str:
    # Get total memory
    result = text

    try:
        codename = "$memory_total$"

        if codename not in text:
            return result

        status = str(get_size(virtual_memory().total))

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get mem total error: {e}", exc_info=True)

    return result


def get_mem_used(text: str) -> str:
    # Get used memory
    result = text

    try:
        codename = "$memory_used$"

        if codename not in text:
            return result

        status = str(get_size(virtual_memory().used))

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get mem used error: {e}", exc_info=True)

    return result


def get_size(b: int, suffix: str = "B") -> str:
    # Get size
    result = ""

    try:
        factor = 1024

        for unit in ["", "K", "M", "G", "T", "P"]:
            if b < factor:
                break

            b /= factor

        result = f"{b:.2f} {unit}{suffix}"
    except Exception as e:
        logger.warning(f"Get size error: {e}", exc_info=True)

    return result


def get_status() -> str:
    # Get system status
    result = glovar.report

    try:
        # Basic
        result = get_interval(result)
        result = get_last(result)

        # System
        result = get_dist(result)
        result = get_kernel(result)
        result = get_hostname(result)
        result = get_up_time(result)

        # CPU
        result = get_cpu_count_physical(result)
        result = get_cpu_count_logical(result)
        result = get_cpu_freq_max(result)
        result = get_cpu_freq_min(result)
        result = get_cpu_freq_current(result)
        result = get_cpu_usage_total(result)
        result = get_cpu_usage_per(result)

        # Memory
        result = get_mem_total(result)
        result = get_mem_available(result)
        result = get_mem_used(result)
        result = get_mem_percent(result)
    except Exception as e:
        logger.warning(f"Get status error: {e}", exc_info=True)

    return result


def get_up_time(text: str) -> str:
    # Get system up time
    result = text

    try:
        codename = "$up_time$"

        if codename not in text:
            return result

        status = get_time_str(
            secs=get_now() - boot_time(),
            the_format=glovar.format_time
        )

        result = result.replace(codename, status)
    except Exception as e:
        logger.warning(f"Get up time error: {e}", exc_info=True)

    return result
