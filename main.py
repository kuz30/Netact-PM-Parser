import gzip
import xml

from Netact3GPP32435ContentHandler import Netact3GPP32435ContentHandler


# Processing example gzip files with filtering specific elements

def printer(name: str, stack: list[dict]) -> None:
    """
    Example Element printer
    :param name: XML Element Name
    :param stack: XML Element stack
    """
    element = stack[-1]
    print(f'Element: {name}, attrs: {element}')


def some_filter(name: str, attrs: dict, stack: list[dict]) -> str:
    """
    Example ignoring all measInfo != LTE_QoS
    :param name: XML Element name
    :param attrs: XML Element attrs
    :param stack: XML Element stack
    :return: XML Element name to skip
    """
    skip_name = None
    if name == 'measInfo' and attrs.get('measInfoId', None) != 'LTE_QoS':
        skip_name = name
    return skip_name


def parse_gzip_file(filepath: str) -> None:
    """
    Example 3GPP file parsing
    :param filepath: GZIP 3GPP NetAct file
    """
    # SAX Parser
    handler = Netact3GPP32435ContentHandler("Example", filepath, printer, some_filter)
    # GZip input stream
    gzip_file = gzip.open(filepath)
    # Process parsing
    xml.sax.parse(gzip_file, handler)


if __name__ == '__main__':
    parse_gzip_file('./input.gz')
