from typing import Union, Callable
from xml.sax.handler import ContentHandler

# Parse 3GPP 32.435 xml format in simplified form
# measCollecFile
# - fileHeader
# - 0..measData
# - - 0..measInfo
# - - - 0..measValue
# - fileFooter
from measCollecFile import MeasCollecFile, MeasData, MeasInfo, MeasValue


class Netact3GPP32435ContentHandler(ContentHandler):
    """
        XML SAX Parser coupled to 3GPP 32.435 xml format
        Parsing pauses:
        - on start_element_filter returning Element name - whole Element to be skipped
        - on callback call when whole Element is processed
    """

    def __init__(self, instance: str, path: str,
                 callback: Callable[[str, list[dict]], None],
                 start_element_filter: Callable[[str, dict, list[dict]], str] = None):
        """

        :param instance: Source file Instance
        :param path: Source file Path
        :param callback(ElementName: str, list[Element: dict]) -> None
            called on XML Element end with name and stack for any further processing
        :param start_element_filter(ElementName: str, attrs: dict, list[Element: dict]) -> ElementName: str
            called on XML Element start processed to skip further XML Element processing if name is returned
        """
        self.instance = instance
        self.path = path
        self.callback = callback
        self.start_element_filter = start_element_filter
        super().__init__()

    # Current element hierarchy
    _elements: list[dict] = []
    _names: list[str] = []

    def push(self, name: str, element: dict = None):
        self._names.append(name)
        self._elements.append(element)

    def pop(self):
        return self._names.pop(), self._elements.pop()

    def is_top(self):
        return len(self._names) == 0

    def context(self):
        return self._names[-1]

    def set_attrs(self, values: dict):
        self._elements[-1] |= values

    def set_attr(self, key: str, value: Union[dict, list]):
        self._elements[-1][key] = value

    # current content name
    _parse_name = None

    # do parse content
    def parse_content(self, name):
        self._parse_name = name

    # stop parse content
    def end_parse_content(self):
        self._parse_name = None

    # skip element for some reason
    _skipped_name = None

    def is_skipping(self):
        return self._skipped_name is not None

    def skip_element(self, name: str):
        self._skipped_name = name

    def end_skip_element(self, name):
        if name == self._skipped_name:
            self._skipped_name = None

    # If not skipping and filter provided then apply
    def is_skipping_start(self, name, attrs):
        if not self.is_skipping() and self.start_element_filter is not None:
            if (skip_name := self.start_element_filter(name, attrs, self._elements)) is not None:
                self.skip_element(skip_name)

        return self.is_skipping()

    def startElement(self, name, attrs):
        if not self.is_skipping_start(name, attrs):
            # Handle top-level elements
            if self.is_top():
                if name == 'measCollecFile':
                    self.push(name, MeasCollecFile(
                        fileFormatVersion=None,
                        vendorName=None,
                        dnPrefix=None,
                        localDn=None,
                        elementType=None,
                        beginTime=None,
                        endTime=None,
                    ))
            # Handle child elements
            else:
                context = self.context()
                # measCollecFile
                if context == 'measCollecFile':
                    if name in ('fileHeader', 'fileSender', 'measCollec'):
                        # fileHeader fileFormatVersion, Optional vendorName, Optional dnPrefix
                        # - fileSender Optional localDn, Optional elementType
                        # - measCollec beginTime
                        # fileFooter
                        # - measCollec endTime
                        self.set_attrs(attrs)
                    elif name == 'measData':
                        self.push(name, MeasData(
                            localDn=None,
                            userLabel=None,
                            swVersion=None,
                        ))
                # measData
                elif context == 'measData':
                    if name == 'managedElement':
                        # managedElement Optional localDn, Optional userLabel, Optional swVersion
                        self.set_attrs(attrs)
                    elif name == 'measInfo':
                        self.push(name, MeasInfo(
                            measInfoId=attrs.get('measInfoId', None),
                            jobId=None,
                            endTime=None,
                            duration=None,
                            repPeriodDuration=None,
                            measTypes=None,
                        ))
                # measInfo
                # - job jobId
                # - granPeriod endTime duration
                # - repPeriod duration
                # - measTypes | measType p
                elif context == 'measInfo':
                    if name in ('job', 'granPeriod'):
                        self.set_attrs(attrs)
                    elif name == 'repPeriod':
                        self.set_attr('repPeriodDuration', attrs.get('duration'))
                    elif name == 'measTypes':
                        self.parse_content(name)
                    elif name == 'measValue':
                        self.push(name, MeasValue(
                            measObjLdn=attrs.get('measObjLdn'),
                            optionalInformation=attrs.get('optionalInformation', None),
                            measResults=None,
                            suspect=None,
                        ))
                # measValue
                # - measResults | r p
                # - suspect
                elif context == 'measValue':
                    if name == 'measResults':
                        self.parse_content(name)
                    elif name == 'suspect':
                        self.parse_content(name)

    # Handle endElement
    def endElement(self, name):
        if self.is_skipping():
            self.end_skip_element(name)
        else:
            if name in ('measCollecFile', 'measData', 'measInfo', 'measValue'):
                self.callback(name, self._elements)
                self.pop()

    # Handle characters
    def characters(self, content):
        if self._parse_name:
            if self._parse_name in ('measTypes', 'measResults'):
                self.set_attr(self._parse_name, content.split())
            elif self._parse_name == 'suspect':
                self.set_attr(self._parse_name, content)
            self.end_parse_content()
