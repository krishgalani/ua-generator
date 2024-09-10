"""
Random User-Agent
Copyright: 2022-2024 Ekin Karadeniz (github.com/iamdual)
License: Apache License 2.0 
"""
import random
from typing import List
from ...exceptions import InvalidVersionError,InvalidArgumentError
from ..version import Version, WindowsVersion, VersionRange
from ...options import Options
#ua-generator/src/data/browsers/windows.py
# https://learn.microsoft.com/en-us/windows/win32/sysinfo/operating-system-version
# https://learn.microsoft.com/en-us/microsoft-edge/web-platform/how-to-detect-win11
versions: List[WindowsVersion] = [
    WindowsVersion(Version(major=6, minor=1), ch_platform=Version(major=0)),
    WindowsVersion(Version(major=6, minor=2), ch_platform=Version(major=0)),
    WindowsVersion(Version(major=6, minor=3), ch_platform=Version(major=0)),
    WindowsVersion(Version(major=10, minor=0), ch_platform=Version(major=10)),
    WindowsVersion(Version(major=10, minor=0), ch_platform=Version(major=(13, 15))),
]

versions_idx_map = {}

def get_version(options: Options) -> WindowsVersion:
    selected_version : WindowsVersion
    if options.version_ranges is not None and 'windows' in options.version_ranges: 
        version_range = options.version_ranges['windows']
        min_idx = 0
        max_idx = len(versions)
        if(version_range.min_version is not None):
            if(version_range.min_version.major not in versions_idx_map):
                raise InvalidVersionError("Invalid {} version {} specified, valid versions are {}-{}\n".format("firefox", version_range.min_version.major, versions[0].major, versions[-1].major))
            min_idx = versions_idx_map[version_range.min_version.major]
        if(version_range.max_version is not None):
            if(version_range.max_version.major not in versions_idx_map):
                raise InvalidVersionError("Invalid {} version {} specified, valid versions are {}-{}\n".format("firefox", version_range.min_version.major, versions[0].major, versions[-1].major))
            max_idx = versions_idx_map[version_range.max_version.major]+1
        filtered = versions[min_idx:max_idx]
        if len(filtered) > 0:
            selected_version = random.choice(filtered)
    elif options.weighted_versions:
        weights = [1.0] * len(versions)
        # https://gs.statcounter.com/os-version-market-share/windows/desktop/worldwide
        weights[-1] = 7.0
        weights[-2] = 10.0
        selected_version = random.choices(versions, weights=weights, k=1)[0]
    else:
        selected_version = random.choice(versions)
    selected_version.get_version()
    return selected_version
def num_possible_versions() -> float:
    count : float = 0.0
    for i in range(len(versions)):
       if type(versions[i].ch_platform.majors) is tuple:
        count += versions[i].ch_platform.majors[1] - versions[i].ch_platform.majors[0] + 1
       else:
           count += 1
    return count