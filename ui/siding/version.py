###############################################################################
#
# Copyright 2012 Siding Developers (see AUTHORS.txt)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################
"""
A simple pair of classes for easily comparing and testing version numbers.
These are used internally by :doc:`plugins` for testing plugin
dependencies.
"""

###############################################################################
# Imports
###############################################################################

import re

###############################################################################
# Constants
###############################################################################

version_match = re.compile(r"(\d+)(?:\.(\d+)(?:\.(\d+))?)?(?:-([0-9A-Za-z-\.]+))?(?:\+([0-9A-Za-z-\.]+))?")
rule_match = re.compile(r"(?:\s*([<>=!]+)\s*)([^\s<>=!]+)")
name_match = re.compile(r"^\s*([^\s<>=!]+)")

def _value(val):
    try:
        return int(val)
    except ValueError:
        return val

###############################################################################
# The Version Class
###############################################################################

class Version(object):
    """
    This lightweight class represents a version string in a way that can be
    *accurately* compared to other version strings. Take, for example, the
    following:

    >>> '1.0.0-alpha2' < '1.0'
    False

    Clearly, that's wrong. With Version though:

    .. testsetup::

        from siding.version import Version

    >>> Version('1.0.0-alpha2') < '1.0'
    True

    Version can be compared to other Version instances or strings. Version
    strings should be formatted in a way compatible with
    `Semantic Versioning <http://semver.org/>`_.
    """
    __slots__ = ('_major', '_minor', '_patch', '_prerelease', '_build')

    def __init__(self, version=None):
        self._major = self._minor = self._patch = 0
        self._prerelease = self._build = None

        if version:
            if isinstance(version, Version):
                self._major = version._major
                self._minor = version._minor
                self._patch = version._patch
                self._prerelease = version._prerelease
                self._build = version._build

            elif isinstance(version, basestring):
                match = version_match.match(version)
                if match:
                    self._major = int(match.group(1))

                    if match.group(2):
                        self._minor = int(match.group(2))

                    if match.group(3):
                        self._patch = int(match.group(3))

                    if match.group(4):
                        self._prerelease = tuple(map(_value, match.group(4).
                                                                split('.')))

                    if match.group(5):
                        self._build = tuple(map(_value, match.group(5).
                                                        split('.')))
                else:
                    raise ValueError('%r is not a valid version string.' %
                                version)

            else:
                raise ValueError('%r cannot be converted to a version.' %
                                version)

    ##### Properties ##########################################################

    @property
    def major(self):
        """ The major number. """
        return self._major

    @property
    def minor(self):
        """ The minor number. """
        return self._minor

    @property
    def patch(self):
        """ The patch number. """
        return self._patch

    @property
    def prerelease(self):
        """ The prerelease string. """
        if self._prerelease:
            return '.'.join(str(x) for x in self._prerelease)
        return ''

    @property
    def build(self):
        """ The build string. """
        if self._build:
            return '.'.join(str(x) for x in self._build)
        return ''

    ##### String Conversion ###################################################

    def __repr__(self):
        return '<Version(%s)>' % str(self)

    def __str__(self):
        out = '%d.%d.%d' % (self._major, self._minor, self._patch)
        if self._prerelease:
            out += '-%s' % self.prerelease
        if self._build:
            out += '+%s' % self.build
        return out

    ##### Comparison ##########################################################

    def __nonzero__(self):
        return bool(self._major or self._minor or self._patch or
                self._prerelease or self._build)

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        if isinstance(other, basestring):
            other = Version(other)

        if self._major < other._major:
            return True
        elif self._major > other._major:
            return False

        if self._minor < other._minor:
            return True
        elif self._minor > other._minor:
            return False

        if self._patch < other._patch:
            return True
        elif self._patch > other._patch:
            return False

        if self._prerelease and not other._prerelease:
            return True
        elif not self._prerelease and other._prerelease:
            return False
        elif self._prerelease < other._prerelease:
            return True
        elif self._prerelease > other._prerelease:
            return False

        if self._build < other._build:
            return True

        return False

    def __le__(self, other):
        return not self.__gt__(other)

    def __eq__(self, other):
        if isinstance(other, basestring):
            other = Version(other)

        return (self._major == other._major and self._minor == other._minor and
            self._patch == other._patch and self._build == other._build and
            self._prerelease == other._prerelease)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, basestring):
            other = Version(other)

        if self._major > other._major:
            return True
        elif self._major < other._major:
            return False

        if self._minor > other._minor:
            return True
        elif self._minor < other._minor:
            return False

        if self._patch > other._patch:
            return True
        elif self._patch < other._patch:
            return False

        if other._prerelease and not self._prerelease:
            return True
        elif not other._prerelease and self._prerelease:
            return False
        elif self._prerelease > other._prerelease:
            return True
        elif self._prerelease < other._prerelease:
            return False

        if self._build > other._build:
            return True

        return False

    def __ge__(self, other):
        return not self.__lt__(other)

###############################################################################
# The VersionMatch Class
###############################################################################

class VersionMatch(object):
    """
    This class allows you to perform complex comparisons of a version to a
    list of rules. For example:

    .. testsetup::

        from siding.version import VersionMatch

    >>> match = VersionMatch('> 1.2 < 4.8 != 2.6-alpha3')
    >>> match.test('1')
    False
    >>> match.test('2')
    True
    >>> match.test('2.6-alpha3')
    False
    >>> match.test('4.8-alpha1')
    True
    >>> match.test('4.8.1')
    False

    The rule list may be of any length, and consists of the repetition of an
    operator followed by a version string. Operators may be: ``<``, ``<=``,
    ``=``, ``!=``, ``>=``, ``>``
    """
    __slots__ = ('_comparisons', )

    def __init__(self, rules):
        self._comparisons = []

        if isinstance(rules, VersionMatch):
            self._comparisons = rules._comparisons[:]

        elif isinstance(rules, basestring):
            for cmp, ver in rule_match.findall(rules):
                ver = Version(ver)
                self._comparisons.append((cmp, ver))

        else:
            raise ValueError("%r cannot be converted to a VersionMatch.")

    def __repr__(self):
        return '<VersionMatch(%s)>' % str(self)

    def __str__(self):
        return ' '.join('%s %s' % x for x in self._comparisons)

    def test(self, version):
        """ Test the given version against this VersionMatch. """
        if not version:
            return False

        for cmp, ver in self._comparisons:
            if cmp == '=' or cmp == '==' and not version == ver:
                return False
            elif cmp == '<' and not version < ver:
                return False
            elif cmp == '<=' and not version <= ver:
                return False
            elif cmp == '>' and not version > ver:
                return False
            elif cmp == '>=' and not version >= ver:
                return False
            elif cmp == '!=' and not version != ver:
                return False
        return True

    @staticmethod
    def from_string(rules):
        """
        Create a VersionMatch from a string, and return a tuple of
        ``(name, version_match)`` where name is a trimmed string of all text
        before the first operator.
        """
        name = name_match.match(rules)
        if name:
            name = name.group(1)
        return name, VersionMatch(rules)
