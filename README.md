# NetAct-PM-Parser
NetAct 3GPP 32.435 Performance management data parser from *.gz file using fast SAX / libxml2 parsing with filtering.
Code used as extractor in Apache Airflow instance to collect data from multiple NetActs and to push in TimescaleDB every 15min and 1hour as fast as possible.

[measCollecFile.py](./measCollecFile.py) - data classes for xsd-schema objects

### Reference materials
- [measCollec.xsd](./static/measCollec.xsd) - reference 3GPP TS 32.435 Performance Measurement XML file format definition XSD
- [3GPP TS 32.435 version 17.0.0 Release 17](https://portal.etsi.org/webapp/workprogram/Report_WorkItem.asp?WKI_ID=65243) - reference 3GPP TS 32.435 Performance Measurement XML file