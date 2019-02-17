class StaleDependenciesError(Exception):
    pass


class PackagesDependencyChecker(object):

    def __init__(self, options):
        self.throw_on = options.get('--throw-on') or ""
        print("Your throw selection is:", self.throw_on)

    def check_dependencies(self, packages_status_map):

        found_stale_packages = False
        for pkg_name, pkg in packages_status_map.items():
            current = pkg['current_version']
            latest = pkg['latest_version']

            if not pkg['upgrade_available']:
                continue

            msg = "{} is stale, current: {} latest is: {}".format(
                pkg_name, current.base_version, latest.base_version)

            l_release = latest.release
            c_release = current.release

            if len(latest.release) < 3:
                l_release = l_release + (0,)

            if len(current.release) < 3:
                c_release = c_release + (0,)

            if len(latest.release) > 3:
                l_release = l_release[:3]

            if len(current.release) > 3:
                c_release = c_release[:3]

            # check if major, minor, patch
            l_major, l_minor, l_patch = l_release
            c_major, c_minor, c_patch = c_release

            if l_major > c_major and self.throw_on == "major":
                found_stale_packages = True
                print(msg + "| You're a major version behind!")

            elif l_minor > c_minor and self.throw_on == "minor":
                found_stale_packages = True
                print(msg + "| You're a minor version behind!")

            elif l_patch > c_patch and self.throw_on == "patch":
                found_stale_packages = True
                print(msg + "| You're a patch version behind!")
            else:
                print(msg)

        if self.throw_on and found_stale_packages:
            raise StaleDependenciesError("You got stale packages")
