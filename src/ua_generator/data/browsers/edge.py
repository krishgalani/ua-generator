"""
Random User-Agent
Copyright: 2022-2024 Ekin Karadeniz (github.com/iamdual)
License: Apache License 2.0 
"""
import random
from typing import List

from ..version import Version, ChromiumVersion, VersionRange
from ...options import Options
from ...exceptions import InvalidVersionError

#ua-generator/src/data/browsers/edge.py
# https://docs.microsoft.com/en-us/deployedge/microsoft-edge-release-schedule
versions: List[ChromiumVersion] = [
    ChromiumVersion(Version(major=100, minor=0, build=1185, patch=(0, 99))),
    ChromiumVersion(Version(major=101, minor=0, build=1210, patch=(0, 99))),
    ChromiumVersion(Version(major=102, minor=0, build=1245, patch=(0, 99))),
    ChromiumVersion(Version(major=103, minor=0, build=1264, patch=(0, 99))),
    ChromiumVersion(Version(major=104, minor=0, build=1293, patch=(0, 99))),
    ChromiumVersion(Version(major=105, minor=0, build=1343, patch=(0, 99))),
    ChromiumVersion(Version(major=106, minor=0, build=1370, patch=(0, 99))),
    ChromiumVersion(Version(major=107, minor=0, build=1418, patch=(0, 99))),
    ChromiumVersion(Version(major=108, minor=0, build=1462, patch=(0, 99))),
    ChromiumVersion(Version(major=109, minor=0, build=1518, patch=(0, 99))),
    ChromiumVersion(Version(major=110, minor=0, build=1587, patch=(0, 99))),
    ChromiumVersion(Version(major=111, minor=0, build=1661, patch=(0, 99))),
    ChromiumVersion(Version(major=112, minor=0, build=1722, patch=(0, 99))),
    ChromiumVersion(Version(major=113, minor=0, build=1774, patch=(0, 99))),
    ChromiumVersion(Version(major=114, minor=0, build=1823, patch=(0, 99))),
    ChromiumVersion(Version(major=115, minor=0, build=1901, patch=(0, 99))),
    ChromiumVersion(Version(major=116, minor=0, build=1938, patch=(0, 99))),
    ChromiumVersion(Version(major=117, minor=0, build=2045, patch=(0, 99))),
    ChromiumVersion(Version(major=118, minor=0, build=2088, patch=(0, 99))),
    ChromiumVersion(Version(major=119, minor=0, build=2151, patch=(0, 99))),
    ChromiumVersion(Version(major=120, minor=0, build=2210, patch=(0, 99))),
    ChromiumVersion(Version(major=121, minor=0, build=2277, patch=(0, 99))),
    ChromiumVersion(Version(major=122, minor=0, build=2365, patch=(0, 99))),
    ChromiumVersion(Version(major=123, minor=0, build=2420, patch=(0, 99))),
    ChromiumVersion(Version(major=124, minor=0, build=2478, patch=(0, 99))),
    ChromiumVersion(Version(major=125, minor=0, build=2535, patch=(0, 99))),
    ChromiumVersion(Version(major=126, minor=0, build=2592, patch=(0, 99))),
    ChromiumVersion(Version(major=127, minor=0, build=2651, patch=(0, 99))),
    ChromiumVersion(Version(major=128, minor=0, build=2739, patch=(0, 99))),
]

versions_idx_map = {}

def get_version(options: Options) -> ChromiumVersion:
    selected_version : ChromiumVersion
    if options.version_ranges is not None and 'edge' in options.version_ranges:
        version_range = options.version_ranges['edge']
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
        weights[-1] = 10.0
        weights[-2] = 9.0
        weights[-3] = 8.0
        selected_version = random.choices(versions, weights=weights, k=1)[0]
    else:
        selected_version = random.choice(versions)
    selected_version.get_version()
    return selected_version
def num_possible_versions() -> float:
    count : float = 0.0
    for i in range(len(versions)):
       if type(versions[i].patches) is tuple:
        count += versions[i].patches[1] - versions[i].patches[0] + 1
       else:
           count += 1
    return count