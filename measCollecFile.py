from typing import Optional, TypedDict


# measCollecFile:
# - fileHeader
# - 0.. measData
# - fileFooter
class MeasCollecFile(TypedDict):
    # fileHeader fileFormatVersion vendorName dnPrefix
    fileFormatVersion: Optional[str]
    vendorName: Optional[str]
    dnPrefix: Optional[str]
    # - fileSender
    localDn: Optional[str]
    elementType: Optional[str]
    # - measCollec beginTime
    beginTime: Optional[str]  # dateTime
    # fileFooter
    # - measCollec footer
    endTime: Optional[str]  # dateTime


# measData
# - managedElement
# - 0.. measInfo
class MeasData(TypedDict):
    localDn: Optional[str]
    userLabel: Optional[str]
    swVersion: Optional[str]


# measInfo
# - Optional job
# - granPeriod
# - Optional repPeriod
# - measTypes | 0.. measType
# - 0.. measValue
class MeasInfo(TypedDict):
    measInfoId: Optional[str]
    jobId: Optional[str]
    duration: Optional[str]  # duration PTnS
    endTime: Optional[str]  # dateTime
    repPeriodDuration: Optional[str]  # duration PTnS
    measTypes: Optional[list[str]]


# measValue measObjLdn
# - measResults | 0.. R
# - Optional optionalInformation
# - suspect
class MeasValue(TypedDict):
    measObjLdn: Optional[str]
    optionalInformation: Optional[str]
    measResults: Optional[list[str]]
    suspect: Optional[str]
