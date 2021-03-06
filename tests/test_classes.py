#!/usr/bin/env python
"""
Tests the classes of cdl_convert

REQUIREMENTS:

mock
"""

#==============================================================================
# IMPORTS
#==============================================================================

# Standard Imports
try:
    from unittest import mock
except ImportError:
    import mock
import os
import sys
import unittest

# Grab our test's path and append the cdL_convert root directory

# There has to be a better method than:
# 1) Getting our current directory
# 2) Splitting into list
# 3) Splicing out the last 3 entries (filepath, test dir, tools dir)
# 4) Joining
# 5) Appending to our Python path.

sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-2]))

import cdl_convert.cdl_convert as cdl_convert

#==============================================================================
# GLOBALS
#==============================================================================

if sys.version_info[0] >= 3:
    enc = lambda x: bytes(x, 'UTF-8')
else:
    enc = lambda x: x

if sys.version_info[0] >= 3:
    builtins = 'builtins'
else:
    builtins = '__builtin__'

#==============================================================================
# TEST CLASSES
#==============================================================================

# AscColorSpaceBase ===========================================================


class TestAscColorSpaceBase(unittest.TestCase):
    """Tests the very simple base class which has colorspace attributes"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.node = cdl_convert.AscColorSpaceBase()

    #==========================================================================
    # TESTS
    #==========================================================================

    def testInputDesc(self):
        """Tests that input_desc exists and defaults to none"""

        self.assertTrue(
            hasattr(self.node, 'input_desc')
        )

        self.assertEqual(
            None,
            self.node.input_desc
        )

        self.node.input_desc = 'Sunset with an Eizo'

        self.assertEqual(
            'Sunset with an Eizo',
            self.node.input_desc
        )

    #==========================================================================

    def testViewingDesc(self):
        """Tests that viewing_desc exists and defaults to none"""

        self.assertTrue(
            hasattr(self.node, 'viewing_desc')
        )

        self.assertEqual(
            None,
            self.node.viewing_desc
        )

        self.node.viewing_desc = 'Darker with a tinge of blah'

        self.assertEqual(
            'Darker with a tinge of blah',
            self.node.viewing_desc
        )

    #==========================================================================

    @mock.patch('xml.etree.ElementTree.Element')
    def test_parse_xml_input_desc(self, mock_elem):
        """Tests the input_desc method, which parses an ElementTree element"""

        mock_elem.find.return_value.text = 'Bob'

        self.assertEqual(
            None,
            self.node.input_desc
        )

        self.assertTrue(
            self.node.parse_xml_input_desc(mock_elem)
        )

        self.assertEqual(
            'Bob',
            self.node.input_desc
        )

        mock_elem.find.return_value.text = None

        self.assertTrue(
            self.node.parse_xml_input_desc(mock_elem)
        )

        self.assertEqual(
            None,
            self.node.input_desc
        )

        # Now we'll make the Element.find raise an AttributeError,
        # mocking that the element has no elem with that name.
        mock_elem.find.side_effect = AttributeError('')

        self.node.input_desc = 'Ralph'

        self.assertFalse(
            self.node.parse_xml_input_desc(mock_elem)
        )

        self.assertEqual(
            'Ralph',
            self.node.input_desc
        )

    #==========================================================================

    @mock.patch('xml.etree.ElementTree.Element')
    def test_parse_xml_viewing_desc(self, mock_elem):
        """Tests the viewing_desc method, which parses an ElementTree element"""

        mock_elem.find.return_value.text = 'Bob'

        self.assertEqual(
            None,
            self.node.viewing_desc
        )

        self.assertTrue(
            self.node.parse_xml_viewing_desc(mock_elem)
        )

        self.assertEqual(
            'Bob',
            self.node.viewing_desc
        )

        mock_elem.find.return_value.text = None

        self.assertTrue(
            self.node.parse_xml_viewing_desc(mock_elem)
        )

        self.assertEqual(
            None,
            self.node.viewing_desc
        )

        # Now we'll make the Element.find raise an AttributeError,
        # mocking that the element has no elem with that name.
        mock_elem.find.side_effect = AttributeError('')

        self.node.viewing_desc = 'Ralph'

        self.assertFalse(
            self.node.parse_xml_viewing_desc(mock_elem)
        )

        self.assertEqual(
            'Ralph',
            self.node.viewing_desc
        )

# AscDescBase =================================================================


class TestAscDescBase(unittest.TestCase):
    """Tests the very simple base class which has desc attributes"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.node = cdl_convert.AscDescBase()

    #==========================================================================
    # TESTS
    #==========================================================================

    def testInit(self):
        """Tests that on init desc is created and empty"""

        self.assertEqual(
            [],
            self.node.desc
        )

    #==========================================================================

    def testFirstSet(self):
        """Tests setting desc to a string appends it to the list"""

        self.node.desc = 'first description'

        self.assertEqual(
            ['first description', ],
            self.node.desc
        )

    #==========================================================================

    def testAppendAdditional(self):
        """Tests that setting desc more than once appends to list"""

        self.node.desc = 'first description'

        self.assertEqual(
            ['first description', ],
            self.node.desc
        )

        self.node.desc = 'second description'

        self.assertEqual(
            ['first description', 'second description'],
            self.node.desc
        )

    #==========================================================================

    def testReplaceWithList(self):
        """Tests extending the desc with another list"""

        # Bypass setter
        self.node._desc = ['first description']

        self.node.desc = ['second description', 'third description']

        self.assertEqual(
            ['second description', 'third description'],
            self.node.desc
        )

    #==========================================================================

    def testExtendWithTuple(self):
        """Tests extending the desc with another tuple"""

        # Bypass setter
        self.node._desc = ['first description']

        self.node.desc = ('second description', 'third description')

        self.assertEqual(
            ['second description', 'third description'],
            self.node.desc
        )

    #==========================================================================

    def testClearWithNone(self):
        """Tests that passing desc None will result in a blank list"""

        # Bypass setter
        self.node._desc = ['first description']

        self.node.desc = None

        self.assertEqual(
            [],
            self.node.desc
        )

    #==========================================================================

    def testReplaceWithList(self):
        """Tests replacing desc with a new list"""

        # Bypass setter
        self.node._desc = [
            'first description',
            'second description',
            'third description'
        ]

        self.node.desc = [
            'forth description',
            'fifth description',
            'sixth description'
        ]

        self.assertEqual(
            [
                'forth description',
                'fifth description',
                'sixth description'
            ],
            self.node.desc
        )

    #==========================================================================

    def testReplaceWithTuple(self):
        """Tests replacing desc with a new tuple"""

        # Bypass setter
        self.node._desc = [
            'first description',
            'second description',
            'third description'
        ]

        self.node.desc = (
            'forth description',
            'fifth description',
            'sixth description'
        )

        self.assertEqual(
            [
                'forth description',
                'fifth description',
                'sixth description'
            ],
            self.node.desc
        )

# ColorNodeBase ===============================================================


class TestColorCollectionBase(unittest.TestCase):
    """Tests the very simple base class ColorCollectionBase"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.node = cdl_convert.ColorCollectionBase()

    #==========================================================================
    # TESTS
    #==========================================================================

    def testInputDesc(self):
        """Tests that input_desc inherited"""

        self.assertTrue(
            hasattr(self.node, 'input_desc')
        )

        self.assertEqual(
            None,
            self.node.input_desc
        )

    #==========================================================================

    def testViewingDesc(self):
        """Tests that viewing_desc inherited"""

        self.assertTrue(
            hasattr(self.node, 'viewing_desc')
        )

        self.assertEqual(
            None,
            self.node.viewing_desc
        )

    #==========================================================================

    def testDesc(self):
        """Tests that desc inherited"""

        self.assertTrue(
            hasattr(self.node, 'desc')
        )

        self.assertEqual(
            [],
            self.node.desc
        )

# ColorCorrection =============================================================


class TestColorCorrection(unittest.TestCase):
    """Tests all aspects of the ColorCorrection class.

    Many of the tests involving Sop and Sat values are obsolete, since those
    values have been moved into their own class. However, the tests will remain
    as they're still an attribute of ColorCorrection

    """

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        # Note that the file doesn't really need to exist for our test purposes
        self.cdl = cdl_convert.ColorCorrection(
            id='uniqueId', cdl_file='../testcdl.cc'
        )

    def tearDown(self):
        # We need to clear the ColorCorrection member dictionary so we don't
        # have to worry about non-unique ids.
        cdl_convert.ColorCorrection.members = {}

    #==========================================================================
    # TESTS
    #==========================================================================

    # Properties & Attributes =================================================

    def testInputDesc(self):
        """Tests that input_desc inherited"""

        self.assertTrue(
            hasattr(self.cdl, 'input_desc')
        )

        self.assertEqual(
            None,
            self.cdl.input_desc
        )

    #==========================================================================

    def testViewingDesc(self):
        """Tests that viewing_desc inherited"""

        self.assertTrue(
            hasattr(self.cdl, 'viewing_desc')
        )

        self.assertEqual(
            None,
            self.cdl.viewing_desc
        )

    #==========================================================================

    def testDesc(self):
        """Tests that desc inherited"""

        self.assertTrue(
            hasattr(self.cdl, 'desc')
        )

        self.assertEqual(
            [],
            self.cdl.desc
        )

    #==========================================================================


    def testFileInReturn(self):
        """Tests that calling ColorCorrection.fileIn returns the file given"""
        self.assertEqual(
            os.path.abspath('../testcdl.cc'),
            self.cdl.file_in
        )

    #==========================================================================

    def testFileInSetException(self):
        """Tests that exception raised when setting file_in after init"""
        def testFileIn():
            self.cdl.file_in = '../NewFile.cc'

        self.assertRaises(
            AttributeError,
            testFileIn
        )

    #==========================================================================

    def testFileOutSetException(self):
        """Tests that exception raised when attempting to set file_out direct"""
        def testFileOut():
            self.cdl.file_out = '../NewFile.cc'

        self.assertRaises(
            AttributeError,
            testFileOut
        )

    #==========================================================================

    def testIdReturn(self):
        """Tests that calling ColorCorrection.id returns the id"""
        self.assertEqual(
            'uniqueId',
            self.cdl.id
        )

    #==========================================================================

    def testIdNonUniqueIdOnInit(self):
        """Tests that exception raised when initializing a non-unique id."""

        self.assertRaises(
            ValueError,
            cdl_convert.ColorCorrection,
            'uniqueId',
            'file'
        )

    #==========================================================================

    def testIdNonUniqueIdOnSet(self):
        """Tests that exception raised when setting a non-unique id."""
        def setId(cdl):
            cdl.id = 'uniqueId'

        new = cdl_convert.ColorCorrection('betterId', 'file')

        self.assertRaises(
            ValueError,
            setId,
            new
        )

    #==========================================================================

    def testBlankId(self):
        """Tests what happens when a blank id is given to CC"""
        cdl_convert.ColorCorrection.members = {}

        cdl1 = cdl_convert.ColorCorrection('', 'file')

        self.assertEqual(
            '001',
            cdl1.id
        )

        cdl2 = cdl_convert.ColorCorrection('', 'file')

        self.assertEqual(
            '002',
            cdl2.id
        )

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            cdl_convert.ColorCorrection,
            '',
            'file'
        )

        cdl_convert.HALT_ON_ERROR = False

    #==========================================================================

    def testIdRenameDictionary(self):
        """Tests that dict entries are removed following a rename"""

        new = cdl_convert.ColorCorrection('betterId', 'file')

        self.assertTrue(
            'betterId' in cdl_convert.ColorCorrection.members.keys()
        )

        new.id = 'betterishId'

        self.assertFalse(
            'betterId' in cdl_convert.ColorCorrection.members.keys()
        )

        self.assertTrue(
            'betterishId' in cdl_convert.ColorCorrection.members.keys()
        )

    #==========================================================================

    def testOffsetSetAndGet(self):
        """Tests setting and getting the offset"""

        offset = (-1.3782, 278.32, 0.738378233782)

        self.cdl.offset = offset

        self.assertEqual(
            offset,
            self.cdl.offset
        )

    #==========================================================================

    def testOffsetBadLength(self):
        """Tests passing offset an incorrect length list"""
        def setOffset():
            self.cdl.offset = ['banana']

        self.assertRaises(
            ValueError,
            setOffset
        )

    #==========================================================================

    def testOffsetSetStrings(self):
        """Tests that TypeError raised if given strings"""
        def setOffset():
            self.cdl.offset = [-1.3782, 278.32, 'banana']

        self.assertRaises(
            TypeError,
            setOffset
        )

    #==========================================================================

    def testOffsetBadType(self):
        """Tests passing offset a correct length but bad type value"""
        def setOffset():
            self.cdl.offset = 'ban'

        self.assertRaises(
            TypeError,
            setOffset
        )

    #==========================================================================

    def testOffsetBecomesTuple(self):
        """Tests offset is converted to tuple from list"""

        offset = [-1.3782, 278.32, 0.738378233782]

        self.cdl.offset = offset

        self.assertEqual(
            tuple(offset),
            self.cdl.offset
        )

    #==========================================================================

    def testPowerSetAndGet(self):
        """Tests setting and getting the power"""

        power = (1.3782, 278.32, 0.738378233782)

        self.cdl.power = power

        self.assertEqual(
            power,
            self.cdl.power
        )

    #==========================================================================

    def testPowerSetNegative(self):
        """Tests that ValueError raised if negative value"""
        def setPower():
            self.cdl.power = [-1.3782, 278.32, 0.738378233782]

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setPower
        )

        cdl_convert.HALT_ON_ERROR = False

        setPower()

        self.assertEqual(
            (0.0, 278.32, 0.738378233782),
            self.cdl.power
        )

    #==========================================================================

    def testPowerSetStrings(self):
        """Tests that TypeError raised if given strings"""
        def setPower():
            self.cdl.power = [1.3782, 278.32, 'banana']

        self.assertRaises(
            TypeError,
            setPower
        )

    #==========================================================================

    def testPowerBadLength(self):
        """Tests passing power an incorrect length list"""
        def setPower():
            self.cdl.power = ['banana']

        self.assertRaises(
            ValueError,
            setPower
        )

    #==========================================================================

    def testPowerBadType(self):
        """Tests passing power a correct length but bad type value"""
        def setPower():
            self.cdl.power = 'ban'

        self.assertRaises(
            TypeError,
            setPower
        )

    #==========================================================================

    def testPowerBecomesTuple(self):
        """Tests power is converted to tuple from list"""

        power = [1.3782, 278.32, 0.738378233782]

        self.cdl.power = power

        self.assertEqual(
            tuple(power),
            self.cdl.power
        )

    #==========================================================================

    def testSlopeSetAndGet(self):
        """Tests setting and getting the slope"""

        slope = (1.3782, 278.32, 0.738378233782)

        self.cdl.slope = slope

        self.assertEqual(
            slope,
            self.cdl.slope
        )

    #==========================================================================

    def testSlopeSetNegative(self):
        """Tests that ValueError raised if negative value"""
        def setSlope():
            self.cdl.slope = [-1.3782, 278.32, 0.738378233782]

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSlope
        )

        cdl_convert.HALT_ON_ERROR = False

        setSlope()

        self.assertEqual(
            (0.0, 278.32, 0.738378233782),
            self.cdl.slope
        )

    #==========================================================================

    def testSlopeSetStrings(self):
        """Tests that TypeError raised if given strings"""
        def setSlope():
            self.cdl.slope = [1.3782, 278.32, 'banana']

        self.assertRaises(
            TypeError,
            setSlope
        )

    #==========================================================================

    def testSlopeBadLength(self):
        """Tests passing slope an incorrect length list"""
        def setSlope():
            self.cdl.slope = ['banana']

        self.assertRaises(
            ValueError,
            setSlope
        )

    #==========================================================================

    def testSlopeBadType(self):
        """Tests passing slope a correct length but bad type value"""
        def setSlope():
            self.cdl.slope = 'ban'

        self.assertRaises(
            TypeError,
            setSlope
        )

    #==========================================================================

    def testSlopeBecomesTuple(self):
        """Tests slope is converted to tuple from list"""

        slope = [1.3782, 278.32, 0.738378233782]

        self.cdl.slope = slope

        self.assertEqual(
            tuple(slope),
            self.cdl.slope
        )

    #==========================================================================

    def testSatSetAndGet(self):
        """Tests setting and getting saturation"""

        sat = 34.3267

        self.cdl.sat = sat

        self.assertEqual(
            sat,
            self.cdl.sat
        )

    #==========================================================================

    def testSatSetNegative(self):
        """Tests that a ValueError is raised if sat is set to negative"""
        def setSat():
            self.cdl.sat = -376.23

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSat
        )

        cdl_convert.HALT_ON_ERROR = False

        setSat()

        self.assertEqual(
            0.0,
            self.cdl.sat
        )
    #==========================================================================

    def testSatSetString(self):
        """Tests that a TypeError is raised if sat is set to string"""
        def setSat():
            self.cdl.sat = 'banana'

        self.assertRaises(
            TypeError,
            setSat
        )

    #==========================================================================

    def testSatBecomesFloat(self):
        """Tests that saturation is converted to float from int"""
        sat = 3

        self.cdl.sat = sat

        self.assertEqual(
            float(sat),
            self.cdl.sat
        )

    # determine_dest() ========================================================

    def testDetermineDest(self):
        """Tests that determine destination is calculated correctly"""
        self.cdl.determine_dest('cdl')

        dir = os.path.abspath('../')
        filename = os.path.join(dir, 'uniqueId.cdl')

        self.assertEqual(
            filename,
            self.cdl.file_out
        )

# ColorNodeBase ===============================================================


class TestColorNodeBase(unittest.TestCase):
    """Tests the very simple base class ColorNodeBase"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.node = cdl_convert.ColorNodeBase()

    #==========================================================================
    # TESTS
    #==========================================================================

    def testDesc(self):
        """Tests that desc inherited"""

        self.assertTrue(
            hasattr(self.node, 'desc')
        )

        self.assertEqual(
            [],
            self.node.desc
        )

# MediaRef ====================================================================


class TestMediaRefProperties(unittest.TestCase):
    """Tests all aspects of the MediaRef class"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        cdl_convert.MediaRef.members = {}
        self.directory = 'heeba/jeeba/race'
        self.filename = 'car.jpg'
        self.protocol = 'ftp'
        self.path = 'heeba/jeeba/race/car.jpg'
        self.ref = 'ftp://heeba/jeeba/race/car.jpg'
        self.parent = cdl_convert.ColorDecision()
        self.mr = cdl_convert.MediaRef(
            ref_uri='ftp://heeba/jeeba/race/car.jpg',
            parent=self.parent
        )

    #==========================================================================

    def tearDown(self):
        cdl_convert.MediaRef.members = {}

    #==========================================================================
    # TESTS
    #==========================================================================

    def testParent(self):
        """Tests that parent gets set correctly"""
        self.assertEqual(
            self.parent,
            self.mr.parent
        )

    #==========================================================================

    def testSeqDefaults(self):
        """Tests that seq attributes start at None"""
        self.assertEqual(
            None,
            self.mr._is_seq
        )

        self.assertEqual(
            None,
            self.mr._sequences
        )

    #==========================================================================

    def testMembership(self):
        """Tests that we were added to the member dictionary"""
        self.assertEqual(
            {self.ref: [self.mr]},
            cdl_convert.MediaRef.members
        )

    #==========================================================================

    def testDirectoryReturn(self):
        """Tests that directory returns correctly"""
        self.assertEqual(
            self.directory,
            self.mr.directory
        )

        self.mr._dir = 'burp'

        self.assertEqual(
            'burp',
            self.mr.directory
        )

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._reset_cached_properties')
    @mock.patch('cdl_convert.cdl_convert.MediaRef._change_membership')
    def testDirectorySetString(self, mock_cm, mock_rcp):
        """Tests that directory sets with a string correctly"""
        self.assertEqual(
            self.directory,
            self.mr.directory
        )

        old_ref = self.mr.ref
        new_directory = 'dhsjkd/hahkad'
        self.mr.directory = new_directory

        self.assertEqual(
            new_directory,
            self.mr.directory
        )

        protocol = self.protocol + '://' if self.protocol else ''
        new_ref = protocol + os.path.join(new_directory, self.filename)

        self.assertEqual(
            new_ref,
            self.mr.ref
        )

        mock_cm.assert_called_once_with(
            old_ref=old_ref
        )
        mock_rcp.assert_called_once_with()

    #==========================================================================

    def testDirectorySetBadType(self):
        """Tests that directory doesn't set with a bad type"""
        def setDirectory():
            self.mr.directory = 12345

        self.assertRaises(
            TypeError,
            setDirectory
        )

    #==========================================================================

    @mock.patch('os.path.exists')
    def testExists(self, mock_exists):
        """Tests that exists returns correct information"""
        mock_exists.return_value = True

        self.assertTrue(
            self.mr.exists
        )

        mock_exists.assert_called_once_with(
            os.path.join(self.directory, self.filename)
        )

        mock_exists.return_value = False

        self.assertFalse(
            self.mr.exists
        )

    #==========================================================================

    def testFilenameReturn(self):
        """Tests that filename returns correctly"""
        self.assertEqual(
            self.filename,
            self.mr.filename
        )

        self.mr._filename = 'burp'

        self.assertEqual(
            'burp',
            self.mr.filename
        )

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._reset_cached_properties')
    @mock.patch('cdl_convert.cdl_convert.MediaRef._change_membership')
    def testFilenameSetString(self, mock_cm, mock_rcp):
        """Tests that filename sets with a string correctly"""
        self.assertEqual(
            self.filename,
            self.mr.filename
        )

        old_ref = self.mr.ref
        new_filename = 'bus.exr'
        self.mr.filename = new_filename

        self.assertEqual(
            new_filename,
            self.mr.filename
        )

        protocol = self.protocol + '://' if self.protocol else ''
        new_ref = protocol + os.path.join(self.directory, new_filename)

        self.assertEqual(
            new_ref,
            self.mr.ref
        )

        mock_cm.assert_called_once_with(
            old_ref=old_ref
        )
        mock_rcp.assert_called_once_with()

    #==========================================================================

    def testFilenameSetBadType(self):
        """Tests that filename doesn't set with a bad type"""
        def setFilename():
            self.mr.filename = 12345

        self.assertRaises(
            TypeError,
            setFilename
        )

    #==========================================================================

    @mock.patch('os.path.abspath')
    def testIsAbs(self, mock_abs):
        """Tests the is_abs property"""
        mock_abs.return_value = True

        self.assertTrue(
            self.mr.is_abs
        )

        mock_abs.assert_called_once_with(
            os.path.join(self.directory, self.filename)
        )

        mock_abs.return_value = False

        self.assertFalse(
            self.mr.is_abs
        )

    #==========================================================================

    @mock.patch('os.path.isdir')
    def testIsDir(self, mock_dir):
        """Tests the is_dir property"""
        mock_dir.return_value = True

        self.assertTrue(
            self.mr.is_dir
        )

        mock_dir.assert_called_once_with(
            os.path.join(self.directory, self.filename)
        )

        mock_dir.return_value = False

        self.assertFalse(
            self.mr.is_dir
        )

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._get_sequences')
    def testIsSeq(self, mock_seq):
        """Tests the is_seq property returns is_seq and calls _get_sequences"""
        self.mr._is_seq = 'bob'

        self.assertEqual(
            'bob',
            self.mr.is_seq
        )

        self.assertFalse(
            mock_seq.called
        )

        self.mr._is_seq = None

        self.assertEqual(
            None,
            self.mr.is_seq
        )

        mock_seq.assert_called_once_with()

    #==========================================================================

    @mock.patch('os.path.join')
    def testPathMock(self, mock_path):
        """Tests that path is called correctly"""
        mock_path.return_value = 'ed'
        self.assertEqual(
            'ed',
            self.mr.path
        )

        mock_path.assert_called_once_with(self.directory, self.filename)

    #==========================================================================

    def testPathNoMock(self):
        """Tests that path is joined correctly without mock"""
        self.assertEqual(
            os.path.join(self.directory, self.filename),
            self.mr.path
        )

    #==========================================================================

    def testProtocolReturn(self):
        """Tests that protocol returns correctly"""
        self.assertEqual(
            self.protocol,
            self.mr.protocol
        )

        self.mr._protocol = 'burp'

        self.assertEqual(
            'burp',
            self.mr.protocol
        )

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._reset_cached_properties')
    @mock.patch('cdl_convert.cdl_convert.MediaRef._change_membership')
    def testProtocolSetString(self, mock_cm, mock_rcp):
        """Tests that protocol sets with a string correctly"""
        self.assertEqual(
            self.protocol,
            self.mr.protocol
        )

        old_ref = self.mr.ref
        new_protocol = 'edward'
        self.mr.protocol = new_protocol

        self.assertEqual(
            new_protocol,
            self.mr.protocol
        )

        protocol = new_protocol + '://'
        new_ref = protocol + os.path.join(self.directory, self.filename)

        self.assertEqual(
            new_ref,
            self.mr.ref
        )

        mock_cm.assert_called_once_with(
            old_ref=old_ref
        )
        mock_rcp.assert_called_once_with()

    #==========================================================================

    def testProtocolSetBadType(self):
        """Tests that protocol doesn't set with a bad type"""
        def setProtocol():
            self.mr.protocol = 12345

        self.assertRaises(
            TypeError,
            setProtocol
        )

    #==========================================================================

    def testProtocolTruncate(self):
        """Tests that protocol truncates the ://"""
        self.assertEqual(
            self.protocol,
            self.mr.protocol
        )

        self.mr.protocol = 'aladdin://'

        self.assertEqual(
            'aladdin',
            self.mr.protocol
        )

    #==========================================================================

    def testRef(self):
        """Tests that ref returns correctly"""
        self.assertEqual(
            self.ref,
            self.mr.ref
        )

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._reset_cached_properties')
    @mock.patch('cdl_convert.cdl_convert.MediaRef._change_membership')
    def testSetRefWithProtocol(self, mock_cm, mock_rcp):
        """Tests that ref sets with a string correctly"""
        self.assertEqual(
            self.ref,
            self.mr.ref
        )

        new_ref = 'edward://loves/to/eat/snow/in/the/winter.#####.ned'
        self.mr.ref = new_ref

        self.assertEqual(
            new_ref,
            self.mr.ref
        )

        self.assertEqual(
            'edward',
            self.mr.protocol
        )

        self.assertEqual(
            'loves/to/eat/snow/in/the',
            self.mr.directory
        )

        self.assertEqual(
            'winter.#####.ned',
            self.mr.filename
        )

        mock_cm.assert_called_once_with(
            old_ref=self.ref
        )
        mock_rcp.assert_called_once_with()

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._reset_cached_properties')
    @mock.patch('cdl_convert.cdl_convert.MediaRef._change_membership')
    def testSetRefNoProtocol(self, mock_cm, mock_rcp):
        """Tests that ref sets with a string correctly"""
        self.assertEqual(
            self.ref,
            self.mr.ref
        )

        new_ref = '/loves/to/eat/snow/in/the/winter.#####.ned'
        self.mr.ref = new_ref

        self.assertEqual(
            new_ref,
            self.mr.ref
        )

        self.assertEqual(
            '',
            self.mr.protocol
        )

        self.assertEqual(
            '/loves/to/eat/snow/in/the',
            self.mr.directory
        )

        self.assertEqual(
            'winter.#####.ned',
            self.mr.filename
        )

        mock_cm.assert_called_once_with(
            old_ref=self.ref
        )
        mock_rcp.assert_called_once_with()

    #==========================================================================

    def testSetRefBadType(self):
        def setRef():
            self.mr.ref = 12345

        self.assertRaises(
            TypeError,
            setRef
        )

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._get_sequences')
    def testSeq(self, mock_gs):
        """Tests the seq attribute makes the correct calls"""
        self.mr._sequences = ['apple', 'banana']

        self.assertEqual(
            'apple',
            self.mr.seq
        )

        mock_gs.assert_called_once_with()
        mock_gs.reset_mock()

        self.mr._is_seq = False

        self.assertEqual(
            None,
            self.mr.seq
        )

        # Test that we pulled from the cache
        self.assertFalse(
            mock_gs.called
        )

    #==========================================================================

    @mock.patch('cdl_convert.cdl_convert.MediaRef._get_sequences')
    def testSeqs(self, mock_gs):
        """Tests the seqs attribute makes the correct calls"""
        self.mr._sequences = ['apple', 'banana']

        self.assertEqual(
            ['apple', 'banana'],
            self.mr.seqs
        )

        mock_gs.assert_called_once_with()
        mock_gs.reset_mock()

        self.mr._is_seq = False

        self.assertEqual(
            [],
            self.mr.seqs
        )

        # Test that we pulled from the cache
        self.assertFalse(
            mock_gs.called
        )


class TestMediaRefPropertiesOdd(TestMediaRefProperties):
    """Tests all aspects of the MediaRef class"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        cdl_convert.MediaRef.members = {}
        self.directory = '/bicycle24/myHat/race_condition14'
        self.filename = '17438.hds356_######.exr'
        self.protocol = ''
        self.path = '/bicycle24/myHat/race_condition14/17438.hds356_######.exr'
        self.ref = self.path
        self.parent = cdl_convert.ColorDecision()
        self.mr = cdl_convert.MediaRef(
            ref_uri=self.ref,
            parent=self.parent
        )


class TestMediaRefChangeMembership(unittest.TestCase):
    """Tests the private method _change_membership"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        cdl_convert.MediaRef.members = {}
        self.mr = cdl_convert.MediaRef('hello')

    def tearDown(self):
        cdl_convert.MediaRef.members = {}

    #==========================================================================
    # TESTS
    #==========================================================================

    def testNormalOperation(self):
        """Tests that in normal circumstances, change membership works"""
        self.assertEqual(
            {'hello': [self.mr]},
            cdl_convert.MediaRef.members
        )

        self.mr._filename = 'goodbye'
        self.mr._change_membership(old_ref='hello')

        self.assertEqual(
            {'goodbye': [self.mr]},
            cdl_convert.MediaRef.members
        )

    #==========================================================================

    def testMultipleNewRefs(self):
        """Tests appended to a list that already has a member"""
        self.mr2 = cdl_convert.MediaRef('goodbye')

        self.assertEqual(
            {'hello': [self.mr], 'goodbye': [self.mr2]},
            cdl_convert.MediaRef.members
        )

        self.mr._filename = 'goodbye'
        self.mr._change_membership(old_ref='hello')

        self.assertEqual(
            {'goodbye': [self.mr2, self.mr]},
            cdl_convert.MediaRef.members
        )

    #==========================================================================

    def testMultipleOldRefs(self):
        """Tests removing from a list that still has a member"""
        self.mr2 = cdl_convert.MediaRef('hello')

        self.assertEqual(
            {'hello': [self.mr, self.mr2]},
            cdl_convert.MediaRef.members
        )

        self.mr._filename = 'goodbye'
        self.mr._change_membership(old_ref='hello')

        self.assertEqual(
            {'hello': [self.mr2],'goodbye': [self.mr]},
            cdl_convert.MediaRef.members
        )

    #==========================================================================

    def testBrokenDict(self):
        """Tests that we don't fail just because we're not in the dict"""
        cdl_convert.MediaRef.members = {}

        self.mr._filename = 'goodbye'
        self.mr._change_membership(old_ref='hello')

        self.assertEqual(
            {'goodbye': [self.mr]},
            cdl_convert.MediaRef.members
        )


class TestMediaRefGetSequences(unittest.TestCase):
    """Tests the functionality of getting sequences"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.mr = cdl_convert.MediaRef('hello')
        self.file = 'TCM1L001_20140330.0830710.ari'
        self.seq = 'TCM1L001_20140330.#######.ari'
        self.files = [
            '.aliases',
            'pepperjack_corn.jpg',
            'TCM1L001_20140330.0830710.ari',
            'TCM1L001_20140330.0830711.ari',
            'TCM1L001_20140330.0830712.ari',
            'TCM1L001_20140330.0830713.ari',
            'TCM1L001_20140330.0830714.ari',
            'TCM1L014_20140330.0863186.ari',
            'TCM1L014_20140330.0863516.ari',
            'TCM1L014_20140330.0863916.ari',
            'TCM1L014_20140330.0864516.ari',
            'TCM1L014_20140330.0899516.ari',
            'TCM1L014_20140330.1863516.ari',
            'TCM1L014_20140330.2863516.ari',
            'TCM1L028_20140330.0926197.ari',
            'The best file of my life..ari',
        ]
        self.seqs = [
            'TCM1L001_20140330.#######.ari',
            'TCM1L014_20140330.#######.ari',
            'TCM1L028_20140330.#######.ari',
        ]

        self.is_seq = True

    #==========================================================================
    # TESTS
    #==========================================================================

    @mock.patch('os.path.isdir')
    def testSingleFile(self, mock_dir):
        """Tests a single file for being a sequence"""
        mock_dir.return_value = False

        self.mr._filename = self.file

        self.assertEqual(
            self.is_seq,
            self.mr.is_seq
        )

        self.assertEqual(
            self.seq,
            self.mr.seq
        )

        if self.seq:
            self.assertEqual(
                [self.seq],
                self.mr.seqs
            )
        else:
            self.assertEqual(
                [],
                self.mr.seqs
            )

    #==========================================================================

    @mock.patch('os.listdir')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isdir')
    def testDirExists(self, mock_dir, mock_exists, mock_listdir):
        """Tests parsing a directory for files"""
        mock_dir.return_value = True
        mock_exists.return_value = True
        mock_listdir.return_value = self.files

        self.assertEqual(
            self.is_seq,
            self.mr.is_seq
        )

        if len(self.seqs) > 0:
            self.assertEqual(
                self.seqs[0],
                self.mr.seq
            )
        else:
            self.assertEqual(
                None,
                self.mr.seq
            )

        self.assertEqual(
            self.seqs,
            self.mr.seqs
        )

        mock_listdir.assert_called_once_with(self.mr.path)

    #==========================================================================

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isdir')
    def testDirDoesNotExist(self, mock_dir, mock_exists):
        """Tests what happens when directory doesn't exist"""
        mock_dir.return_value = True
        mock_exists.return_value = False

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            self.mr._get_sequences
        )

        cdl_convert.HALT_ON_ERROR = False

        self.assertEqual(
            False,
            self.mr.is_seq
        )

        self.assertEqual(
            [],
            self.mr.seqs
        )

        self.assertEqual(
            None,
            self.mr.seq
        )


class TestMediaRefGetSequencesNoSeqs(TestMediaRefGetSequences):
    """Tests the functionality of getting sequences"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.mr = cdl_convert.MediaRef('hello')
        self.file = 'TCM1L00120140.ari'
        self.seq = None
        self.files = [
            '.aliases',
            'pepperjack_corn.jpg',
            'TCM1L001_20140330.08307k10.ari',
            'The best file of my life..ari',
        ]
        self.seqs = []

        self.is_seq = False


class TestMediaRefGetSequencesCrazySeqs(TestMediaRefGetSequences):
    """Tests the functionality of getting sequences with odd names"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.mr = cdl_convert.MediaRef('hello')
        self.file = 'B002_C001_01101G_004.R3D'
        self.seq = 'B002_C001_01101G_###.R3D'
        self.files = [
            'B002_C001_01101G_001.R3D',
            'B002_C001_01101G_002.R3D',
            'B002_C001_01101G_003.R3D',
            'B002_C001_01101G_004.R3D',
            'TakeThis SequenceandShoveitupyour.8.exr',
            'A001C008_R402.ari',  # While these are technically an image seq
            'A001C008_R902.ari',  # we don't support them.
            'BB50A-05_A039.14278002315672351753261757362236126723618.ari'
        ]
        self.seqs = [
            'B002_C001_01101G_###.R3D',
            'TakeThis SequenceandShoveitupyour.#.exr',
            'BB50A-05_A039.#########################################.ari'
        ]

        self.is_seq = True


class TestMediaRefGetSequencesPercentDigit(TestMediaRefGetSequences):
    """Tests the functionality of getting seq match with %0d return"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.mr = cdl_convert.MediaRef('hello')
        self.file = 'B002 C001-01101G_%327864d.R3D'
        self.seq = 'B002 C001-01101G_%327864d.R3D'
        self.files = [
            'B002_C001_01101G_001.R3D',
            'B002_C001_01101G_002.R3D',
            'B002_C001_01101G_003.R3D',
            'B002_C001_01101G_004.R3D',
            'TakeThis SequenceandShoveitupyour.8.exr',
            'A001C008_R402.ari',  # While these are technically an image seq
            'A001C008_R902.ari',  # we don't support them.
            'BB50A-05_A039.14278002315672351753261757362236126723618.ari'
        ]
        self.seqs = [
            'B002_C001_01101G_###.R3D',
            'TakeThis SequenceandShoveitupyour.#.exr',
            'BB50A-05_A039.#########################################.ari'
        ]

        self.is_seq = True

class TestMediaRefGetSequencesPercentDigitUnderscore(TestMediaRefGetSequences):
    """Tests the functionality of getting seq match with %0d return"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.mr = cdl_convert.MediaRef('hello')
        self.file = 'TCM1L001_20140330.%05d.ari'
        self.seq = 'TCM1L001_20140330.%05d.ari'
        self.files = [
            '.aliases',
            'pepperjack_corn.jpg',
            'TCM1L001_20140330.0830710.ari',
            'TCM1L001_20140330.0830711.ari',
            'TCM1L001_20140330.0830712.ari',
            'TCM1L001_20140330.0830713.ari',
            'TCM1L001_20140330.0830714.ari',
            'TCM1L014_20140330.0863186.ari',
            'TCM1L014_20140330.0863516.ari',
            'TCM1L014_20140330.0863916.ari',
            'TCM1L014_20140330.0864516.ari',
            'TCM1L014_20140330.0899516.ari',
            'TCM1L014_20140330.1863516.ari',
            'TCM1L014_20140330.2863516.ari',
            'TCM1L028_20140330.0926197.ari',
            'The best file of my life..ari',
        ]
        self.seqs = [
            'TCM1L001_20140330.#######.ari',
            'TCM1L014_20140330.#######.ari',
            'TCM1L028_20140330.#######.ari',
        ]

        self.is_seq = True

# SatNode =====================================================================


class TestSatNode(unittest.TestCase):
    """Tests all aspects of SatNode"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.node = cdl_convert.SatNode(self)

    #==========================================================================
    # TESTS
    #==========================================================================

    def testDesc(self):
        """Tests that desc inherited"""

        self.assertTrue(
            hasattr(self.node, 'desc')
        )

        self.assertEqual(
            [],
            self.node.desc
        )

    #==========================================================================

    def testParent(self):
        """Tests that parent was attached to us correctly"""
        self.assertEqual(
            self,
            self.node.parent
        )

    #==========================================================================

    def testSetParent(self):
        """Tests that we can't set the parent property after init"""
        def setParent():
            self.node.parent = 'banana'

        self.assertRaises(
            AttributeError,
            setParent
        )

    #==========================================================================

    def testDefault(self):
        """Tests that saturation starts off with a default value of 1.0"""
        self.assertEqual(
            1.0,
            self.node.sat
        )

    #==========================================================================

    def testGetSat(self):
        """Tests that we can get the saturation value"""
        # Bypass setter
        self.node._sat = 12.8

        self.assertEqual(
            12.8,
            self.node.sat,
        )

    #==========================================================================

    def testSetWithString(self):
        """Tests that we can set sat with a single string"""
        self.node.sat = '12.3'

        self.assertEqual(
            12.3,
            self.node.sat
        )

    #==========================================================================

    def testSetWithBadString(self):
        """Tests that we can't set sat with a single bad string"""
        def setSat():
            self.node.sat = 'banana'

        self.assertRaises(
            TypeError,
            setSat
        )

    #==========================================================================

    def testSetWithNegativeString(self):
        """Tests that we can't set sat with a single negative string"""
        def setSat():
            self.node.sat = '-20'

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSat
        )

        cdl_convert.HALT_ON_ERROR = False

        setSat()

        self.assertEqual(
            0.0,
            self.node.sat
        )

    #==========================================================================

    def testSetWithFloat(self):
        """Tests that we can set sat with a single float"""
        self.node.sat = 100.1

        self.assertEqual(
            100.1,
            self.node.sat
        )

    #==========================================================================

    def testSetWithNegativeFloat(self):
        """Tests that we can't set sat with a single negative float"""
        def setSat():
            self.node.sat = -20.1

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSat
        )

        cdl_convert.HALT_ON_ERROR = False

        setSat()

        self.assertEqual(
            0.0,
            self.node.sat
        )

    #==========================================================================

    def testSetWithInt(self):
        """Tests that we can set sat with a single int"""
        self.node.sat = 2

        self.assertEqual(
            2,
            self.node.sat
        )

    #==========================================================================

    def testSetWithNegativeInt(self):
        """Tests that we can't set sat with a single negative float"""
        def setSat():
            self.node.sat = -20

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSat
        )

        cdl_convert.HALT_ON_ERROR = False

        setSat()

        self.assertEqual(
            0.0,
            self.node.sat
        )

    #==========================================================================

    def testSetWithListFails(self):
        """Tests that we can't set sat with a list"""
        def setSat():
            self.node.sat = [-1.1]

        self.assertRaises(
            TypeError,
            setSat
        )

# SopNode =====================================================================


class TestSopNode(unittest.TestCase):
    """Tests all aspects of SopNode"""

    #==========================================================================
    # SETUP & TEARDOWN
    #==========================================================================

    def setUp(self):
        self.node = cdl_convert.SopNode(self)

    #==========================================================================
    # TESTS
    #==========================================================================

    def testDesc(self):
        """Tests that desc inherited"""

        self.assertTrue(
            hasattr(self.node, 'desc')
        )

        self.assertEqual(
            [],
            self.node.desc
        )

    #==========================================================================

    def testParent(self):
        """Tests that parent was attached to us correctly"""
        self.assertEqual(
            self,
            self.node.parent
        )

    #==========================================================================

    def testSetParent(self):
        """Tests that we can't set the parent property after init"""
        def setParent():
            self.node.parent = 'banana'

        self.assertRaises(
            AttributeError,
            setParent
        )

    #==========================================================================

    def testSlopeDefault(self):
        """Tests that slope starts off with a default value of 1.0"""
        self.assertEqual(
            (1.0, 1.0, 1.0),
            self.node.slope
        )

    #==========================================================================

    def testGetSlope(self):
        """Tests that we can get the slope value"""
        # Bypass setter
        self.node._slope = [12.8, 1.2, 1.4]

        self.assertEqual(
            (12.8, 1.2, 1.4),
            self.node.slope,
        )

    #==========================================================================

    def testSetSlopeWithString(self):
        """Tests that we can set slope with a single string"""
        self.node.slope = '12.3'

        self.assertEqual(
            (12.3, 12.3, 12.3),
            self.node.slope
        )

    #==========================================================================

    def testSetSlopeWithBadString(self):
        """Tests that we can't set slope with a single bad string"""
        def setSlope():
            self.node.slope = 'banana'

        self.assertRaises(
            TypeError,
            setSlope
        )

    #==========================================================================

    def testSetSlopeWithNegativeString(self):
        """Tests that we can't set slope with a single negative string"""
        def setSlope():
            self.node.slope = '-20'

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSlope
        )

        cdl_convert.HALT_ON_ERROR = False

        setSlope()

        self.assertEqual(
            (0.0, 0.0, 0.0),
            self.node.slope
        )

    #==========================================================================

    def testSetSlopeWithFloat(self):
        """Tests that we can set slope with a single float"""
        self.node.slope = 100.1

        self.assertEqual(
            (100.1, 100.1, 100.1),
            self.node.slope
        )

    #==========================================================================

    def testSetSlopeWithNegativeFloat(self):
        """Tests that we can't set slope with a single negative float"""
        def setSlope():
            self.node.slope = -20.1

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSlope
        )

        cdl_convert.HALT_ON_ERROR = False

        setSlope()

        self.assertEqual(
            (0.0, 0.0, 0.0),
            self.node.slope
        )

    #==========================================================================

    def testSetSlopeWithInt(self):
        """Tests that we can set slope with a single int"""
        self.node.slope = 2

        self.assertEqual(
            (2, 2, 2),
            self.node.slope
        )

    #==========================================================================

    def testSetSlopeWithNegativeInt(self):
        """Tests that we can't set slope with a single negative float"""
        def setSlope():
            self.node.slope = -20

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSlope
        )

        cdl_convert.HALT_ON_ERROR = False

        setSlope()

        self.assertEqual(
            (0.0, 0.0, 0.0),
            self.node.slope
        )

    #==========================================================================

    def testSlopeSetNegative(self):
        """Tests that ValueError raised if negative value"""
        def setSlope():
            self.node.slope = [-1.3782, 278.32, 0.738378233782]

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setSlope
        )

        cdl_convert.HALT_ON_ERROR = False

        setSlope()

        self.assertEqual(
            (0.0, 278.32, 0.738378233782),
            self.node.slope
        )

    #==========================================================================

    def testSlopeSetStrings(self):
        """Tests that TypeError raised if given strings"""
        def setSlope():
            self.node.slope = [1.3782, 278.32, 'banana']

        self.assertRaises(
            TypeError,
            setSlope
        )

    #==========================================================================

    def testSlopeFromDict(self):
        """Tests that TypeError raised if given dict"""
        def setSlope():
            self.node.slope = {'r': 1.3782, 'g': 278.32, 'b': 2}

        self.assertRaises(
            TypeError,
            setSlope
        )

    #==========================================================================

    def testSlopeBadLength(self):
        """Tests passing slope an incorrect length list"""
        def setSlope():
            self.node.slope = ['banana']

        self.assertRaises(
            ValueError,
            setSlope
        )

    #==========================================================================

    def testSlopeBecomesTuple(self):
        """Tests slope is converted to tuple from list"""

        slope = [1.3782, 278.32, 0.738378233782]

        self.node.slope = slope

        self.assertEqual(
            tuple(slope),
            self.node.slope
        )

    #==========================================================================

    def testOffsetDefault(self):
        """Tests that offset starts off with a default value of 1.0"""
        self.assertEqual(
            (0.0, 0.0, 0.0),
            self.node.offset
        )

    #==========================================================================

    def testGetOffset(self):
        """Tests that we can get the offset value"""
        # Bypass setter
        self.node._offset = [12.8, 1.2, 1.4]

        self.assertEqual(
            (12.8, 1.2, 1.4),
            self.node.offset,
        )

    #==========================================================================

    def testSetOffsetWithString(self):
        """Tests that we can set offset with a single string"""
        self.node.offset = '12.3'

        self.assertEqual(
            (12.3, 12.3, 12.3),
            self.node.offset
        )

    #==========================================================================

    def testSetOffsetWithBadString(self):
        """Tests that we can't set offset with a single bad string"""
        def setOffset():
            self.node.offset = 'banana'

        self.assertRaises(
            TypeError,
            setOffset
        )

    #==========================================================================

    def testSetOffsetWithNegativeString(self):
        """Tests that we can set offset with a single negative string"""
        self.node.offset = '-20'

        self.assertEqual(
            (-20.0, -20.0, -20.0),
            self.node.offset
        )

    #==========================================================================

    def testSetOffsetWithFloat(self):
        """Tests that we can set offset with a single float"""
        self.node.offset = 100.1

        self.assertEqual(
            (100.1, 100.1, 100.1),
            self.node.offset
        )

    #==========================================================================

    def testSetOffsetWithNegativeFloat(self):
        """Tests that we can set offset with a single negative float"""
        self.node.offset = -20.1

        self.assertEqual(
            (-20.1, -20.1, -20.1),
            self.node.offset
        )

    #==========================================================================

    def testSetOffsetWithInt(self):
        """Tests that we can set offset with a single int"""
        self.node.offset = 2

        self.assertEqual(
            (2, 2, 2),
            self.node.offset
        )

    #==========================================================================

    def testSetOffsetWithNegativeInt(self):
        """Tests that we can set offset with a single negative int"""
        self.node.offset = -20

        self.assertEqual(
            (-20.0, -20.0, -20.0),
            self.node.offset
        )

    #==========================================================================

    def testOffsetSetNegative(self):
        """Tests that offset can be set to negative value"""
        self.node.offset = [-1.3782, 278.32, 0.738378233782]

        self.assertEqual(
            (-1.3782, 278.32, 0.738378233782),
            self.node.offset
        )

    #==========================================================================

    def testOffsetSetStrings(self):
        """Tests that TypeError raised if given strings"""
        def setOffset():
            self.node.offset = [1.3782, 278.32, 'banana']

        self.assertRaises(
            TypeError,
            setOffset
        )

    #==========================================================================

    def testOffsetFromDict(self):
        """Tests that TypeError raised if given dict"""
        def setOffset():
            self.node.offset = {'r': 1.3782, 'g': 278.32, 'b': 2}

        self.assertRaises(
            TypeError,
            setOffset
        )

    #==========================================================================

    def testOffsetBadLength(self):
        """Tests passing offset an incorrect length list"""
        def setOffset():
            self.node.offset = ['banana']

        self.assertRaises(
            ValueError,
            setOffset
        )

    #==========================================================================

    def testOffsetBecomesTuple(self):
        """Tests offset is converted to tuple from list"""

        offset = [1.3782, 278.32, 0.738378233782]

        self.node.offset = offset

        self.assertEqual(
            tuple(offset),
            self.node.offset
        )

    #==========================================================================

    def testPowerDefault(self):
        """Tests that power starts off with a default value of 1.0"""
        self.assertEqual(
            (1.0, 1.0, 1.0),
            self.node.power
        )

    #==========================================================================

    def testGetPower(self):
        """Tests that we can get the power value"""
        # Bypass setter
        self.node._power = [12.8, 1.2, 1.4]

        self.assertEqual(
            (12.8, 1.2, 1.4),
            self.node.power,
        )

    #==========================================================================

    def testSetPowerWithString(self):
        """Tests that we can set power with a single string"""
        self.node.power = '12.3'

        self.assertEqual(
            (12.3, 12.3, 12.3),
            self.node.power
        )

    #==========================================================================

    def testSetPowerWithBadString(self):
        """Tests that we can't set power with a single bad string"""
        def setPower():
            self.node.power = 'banana'

        self.assertRaises(
            TypeError,
            setPower
        )

    #==========================================================================

    def testSetPowerWithNegativeString(self):
        """Tests that we can't set power with a single negative string"""
        def setPower():
            self.node.power = '-20'

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setPower
        )

        cdl_convert.HALT_ON_ERROR = False

        setPower()

        self.assertEqual(
            (0.0, 0.0, 0.0),
            self.node.power
        )

    #==========================================================================

    def testSetPowerWithFloat(self):
        """Tests that we can set power with a single float"""
        self.node.power = 100.1

        self.assertEqual(
            (100.1, 100.1, 100.1),
            self.node.power
        )

    #==========================================================================

    def testSetPowerWithNegativeFloat(self):
        """Tests that we can't set power with a single negative float"""
        def setPower():
            self.node.power = -20.1

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setPower
        )

        cdl_convert.HALT_ON_ERROR = False

        setPower()

        self.assertEqual(
            (0.0, 0.0, 0.0),
            self.node.power
        )

    #==========================================================================

    def testSetPowerWithInt(self):
        """Tests that we can set power with a single int"""
        self.node.power = 2

        self.assertEqual(
            (2, 2, 2),
            self.node.power
        )

    #==========================================================================

    def testSetPowerWithNegativeInt(self):
        """Tests that we can't set power with a single negative float"""
        def setPower():
            self.node.power = -20

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setPower
        )

        cdl_convert.HALT_ON_ERROR = False

        setPower()

        self.assertEqual(
            (0.0, 0.0, 0.0),
            self.node.power
        )

    #==========================================================================

    def testPowerSetNegative(self):
        """Tests that ValueError raised if negative value"""
        def setPower():
            self.node.power = [-1.3782, 278.32, 0.738378233782]

        cdl_convert.HALT_ON_ERROR = True

        self.assertRaises(
            ValueError,
            setPower
        )

        cdl_convert.HALT_ON_ERROR = False

        setPower()

        self.assertEqual(
            (0.0, 278.32, 0.738378233782),
            self.node.power
        )

    #==========================================================================

    def testPowerSetStrings(self):
        """Tests that TypeError raised if given strings"""
        def setPower():
            self.node.power = [1.3782, 278.32, 'banana']

        self.assertRaises(
            TypeError,
            setPower
        )

    #==========================================================================

    def testPowerFromDict(self):
        """Tests that TypeError raised if given dict"""
        def setPower():
            self.node.power = {'r': 1.3782, 'g': 278.32, 'b': 2}

        self.assertRaises(
            TypeError,
            setPower
        )

    #==========================================================================

    def testPowerBadLength(self):
        """Tests passing power an incorrect length list"""
        def setPower():
            self.node.power = ['banana']

        self.assertRaises(
            ValueError,
            setPower
        )

    #==========================================================================

    def testPowerBecomesTuple(self):
        """Tests power is converted to tuple from list"""

        power = [1.3782, 278.32, 0.738378233782]

        self.node.power = power

        self.assertEqual(
            tuple(power),
            self.node.power
        )

#==============================================================================
# RUNNER
#==============================================================================
if __name__ == '__main__':
    unittest.main()
