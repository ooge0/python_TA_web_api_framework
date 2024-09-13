#  source  http://www.iana.org/assignments/media-types/media-types.xhtml
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class MimeType:
    application: List[str] = field(default_factory=lambda: [
        "application/java-archive", "application/EDI-X12", "application/EDIFACT",
        "application/javascript", "application/octet-stream", "application/ogg",
        "application/pdf", "application/xhtml+xml", "application/x-shockwave-flash",
        "application/json", "application/ld+json", "application/xml",
        "application/zip", "application/x-www-form-urlencoded"
    ])
    audio: List[str] = field(default_factory=lambda: [
        "audio/mpeg", "audio/x-ms-wma", "audio/vnd.rn-realaudio", "audio/x-wav"
    ])
    image: List[str] = field(default_factory=lambda: [
        "image/gif", "image/jpeg", "image/png", "image/tiff",
        "image/vnd.microsoft.icon", "image/x-icon", "image/vnd.djvu", "image/svg+xml"
    ])
    multipart: List[str] = field(default_factory=lambda: [
        "multipart/mixed", "multipart/alternative", "multipart/related", "multipart/form-data"
    ])
    text: List[str] = field(default_factory=lambda: [
        "text/css", "text/csv", "text/html", "text/javascript",
        "text/plain", "text/xml"
    ])
    video: List[str] = field(default_factory=lambda: [
        "video/mpeg", "video/mp4", "video/quicktime",
        "video/x-ms-wmv", "video/x-msvideo", "video/x-flv", "video/webm"
    ])
    vnd: List[str] = field(default_factory=lambda: [
        "application/vnd.android.package-archive", "application/vnd.oasis.opendocument.text",
        "application/vnd.oasis.opendocument.spreadsheet", "application/vnd.oasis.opendocument.presentation",
        "application/vnd.oasis.opendocument.graphics", "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.mozilla.xul+xml"
    ])

    def exclude_types(self, category: str, types_to_exclude: List[str]) -> List[str]:
        """
        Exclude specific MIME types from a category.
        :param category: The category to exclude from (application, audio, etc.)
        :param types_to_exclude: List of types to exclude.
        :return: A list of MIME types with the specified types excluded.
        """
        category_list = getattr(self, category, [])
        return [mime for mime in category_list if mime not in types_to_exclude]

    def all_mime_types(self, exclude: Dict[str, List[str]] = None) -> List[str]:
        """
        Get all MIME types across all categories, optionally excluding specified types.
        :param exclude: A dictionary with categories as keys and lists of MIME types to exclude.
        :return: A list of all MIME types.
        """
        all_types = []
        for category in vars(self).keys():
            category_types = getattr(self, category)
            if exclude and category in exclude:
                category_types = self.exclude_types(category, exclude[category])
            all_types.extend(category_types)
        return all_types
