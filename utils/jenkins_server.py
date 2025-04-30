from jenkins import Jenkins
import json
import requests
from six.moves.urllib.parse import quote, urlencode, urljoin, urlparse
from django.conf import settings  # noqa

BUILD_WITH_PARAMS_JOB = "%(folder_url)sjob/%(short_name)s/buildWithParameters"



class JenkinsException(Exception):
    """General exception type for jenkins-API-related failures."""

    pass


class EmptyResponseException(JenkinsException):
    """A special exception to call out the case receiving an empty response."""

    pass


class Jenkins_server(Jenkins):  
    
    
    def build_job_files(self, name, parameters=None, token=None):
        response = self.jenkins_request(
            requests.Request(
                "POST",
                self.build_job_url(name, parameters, token),
                files=parameters["files"],
            )
        )

        if "Location" not in response.headers:
            raise EmptyResponseException(
                "Header 'Location' not found in "
                "response from server[%s]" % self.server
            )
        location = response.headers["Location"]

        if location.endswith("/"):
            location = location[:-1]
        parts = location.split("/")
        number = int(parts[-1])
        return number


# server = Jenkins_server(
#     "http://10.0.0.207:8080", username="admin", password="XEFCJ9DeR7tZIMJy64", timeout=None
# )
# files = {
#     "large": (
#         "1733732755-hello.zip",
#         open("../uploads/package/1733732755-hello.zip", "rb"),
#     )
# }

# server.build_job_files("1695901740-硬盘读写测试模版", parameters={"files": files})
