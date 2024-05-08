import platform
import re

import requests


class SourceForge:

    def __init__(self):
        self.project_name = "circuitikz-generator"
        self.api_url = f"https://sourceforge.net/projects/{self.project_name}/best_release.json"

    def check_version(self, name_app):

        new_version_available = False
        print('Checking software version...')

        local_pattern = r'v(.+)'
        local_match = re.search(local_pattern, str(name_app))
        if local_match:

            local_version = local_match.group(1)

            try:
                response = requests.get(self.api_url)
                response.raise_for_status()

                so = platform.system()

                filename = str(response.json()['platform_releases'][so.lower()]['filename'])
                remote_pattern = r'/v(.+)/'
                remote_match = re.search(remote_pattern, filename)

                if remote_match:
                    remote_version = remote_match.group(1)

                    if float(remote_version) > float(local_version):
                        new_version_available = True
                        print(f"A new version is available: {remote_version}.")
                        print("You can download it from: https://sourceforge.net/projects/circuitikz-generator/")
                    else:
                        print("Your software is up to date.")

                else:
                    print("No version found.")

            except Exception as e:
                print("Error checking for updates:", e)

        return new_version_available
