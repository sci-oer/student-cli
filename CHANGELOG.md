# Changelog

## [v0.4.0](https://github.com/sci-oer/student-cli/releases/v0.4.0) (2022-08-23)

[Full Changelog](https://github.com/sci-oer/student-cli/compare/v0.3.0...v0.4.0)

**Merged pull requests:**

- chore: update dependancy files, added shellingham and rich for pretty printing [\#62](https://github.com/sci-oer/student-cli/pull/62) ([MarshallAsch](https://github.com/MarshallAsch))
- feat: update the help messages [\#61](https://github.com/sci-oer/student-cli/pull/61) ([MarshallAsch](https://github.com/MarshallAsch))
- fix: removed extra / in the ports regex [\#60](https://github.com/sci-oer/student-cli/pull/60) ([MarshallAsch](https://github.com/MarshallAsch))
- chore: remove setting the uid and guid of the user that the container runs as [\#59](https://github.com/sci-oer/student-cli/pull/59) ([MarshallAsch](https://github.com/MarshallAsch))

## [v0.3.0](https://github.com/sci-oer/student-cli/releases/v0.3.0) (2022-08-19)

[Full Changelog](https://github.com/sci-oer/student-cli/compare/v0.2.0...v0.3.0)

**Implemented enhancements:**

- check that start will reuse a container if it already exists [\#47](https://github.com/sci-oer/student-cli/issues/47)
- set the host name of the docker container when it starts so the container  [\#44](https://github.com/sci-oer/student-cli/issues/44)
- if no course name is specified and there is only a single course in the config file use that one [\#43](https://github.com/sci-oer/student-cli/issues/43)
- for the config command use the ~/.scioer.yaml by default [\#41](https://github.com/sci-oer/student-cli/issues/41)
- should not need to specify the config file it should load the default [\#39](https://github.com/sci-oer/student-cli/issues/39)
- single custom port should forward the same port [\#38](https://github.com/sci-oer/student-cli/issues/38)
- Change default storage path to home [\#37](https://github.com/sci-oer/student-cli/issues/37)
- Implement basic start command [\#9](https://github.com/sci-oer/student-cli/issues/9)
- feat: ask they user if they want the default ports instead of asking about each port [\#58](https://github.com/sci-oer/student-cli/pull/58) ([MarshallAsch](https://github.com/MarshallAsch))
- feat: use desktop as storage path instead of ~/.local [\#57](https://github.com/sci-oer/student-cli/pull/57) ([MarshallAsch](https://github.com/MarshallAsch))
- feat: set hostname in the container [\#56](https://github.com/sci-oer/student-cli/pull/56) ([MarshallAsch](https://github.com/MarshallAsch))
- fix: missed default course name in the start command [\#55](https://github.com/sci-oer/student-cli/pull/55) ([MarshallAsch](https://github.com/MarshallAsch))
- feat: default to the one course if there is only one configured course [\#53](https://github.com/sci-oer/student-cli/pull/53) ([MarshallAsch](https://github.com/MarshallAsch))
- feat: if the course container already exists do not recreate it [\#52](https://github.com/sci-oer/student-cli/pull/52) ([MarshallAsch](https://github.com/MarshallAsch))
- fix: no longer print that the port mapping is wrong when none is given [\#50](https://github.com/sci-oer/student-cli/pull/50) ([MarshallAsch](https://github.com/MarshallAsch))
- chore: automaticly load the default config file [\#49](https://github.com/sci-oer/student-cli/pull/49) ([MarshallAsch](https://github.com/MarshallAsch))

**Fixed bugs:**

- no port in the config should not print an error [\#42](https://github.com/sci-oer/student-cli/issues/42)
- make sure path gets expanded for config file [\#36](https://github.com/sci-oer/student-cli/issues/36)
- fix: expand the paths that are passed in for the data dir and config file [\#54](https://github.com/sci-oer/student-cli/pull/54) ([MarshallAsch](https://github.com/MarshallAsch))

**Merged pull requests:**

- feat: when a single port is specified then use that value for the host and the container port number [\#51](https://github.com/sci-oer/student-cli/pull/51) ([MarshallAsch](https://github.com/MarshallAsch))

## [v0.2.0](https://github.com/sci-oer/student-cli/releases/v0.2.0) (2022-08-11)

[Full Changelog](https://github.com/sci-oer/student-cli/compare/v0.1.0...v0.2.0)

**Implemented enhancements:**

- Add the ports specifications to the config file [\#31](https://github.com/sci-oer/student-cli/issues/31)
- flip no pull option [\#10](https://github.com/sci-oer/student-cli/issues/10)
- Check that docker is installed and running [\#6](https://github.com/sci-oer/student-cli/issues/6)
- feat: add port mapping to the config file and pass the ports numbers into the container [\#33](https://github.com/sci-oer/student-cli/pull/33) ([MarshallAsch](https://github.com/MarshallAsch))
- feat: check that docker is running before starting [\#28](https://github.com/sci-oer/student-cli/pull/28) ([MarshallAsch](https://github.com/MarshallAsch))
- feat!: Make config file flag consistent [\#27](https://github.com/sci-oer/student-cli/pull/27) ([MarshallAsch](https://github.com/MarshallAsch))
- chore!: flip the default value for the pull option [\#24](https://github.com/sci-oer/student-cli/pull/24) ([MarshallAsch](https://github.com/MarshallAsch))

**Fixed bugs:**

- Rename pip package to  for publication [\#29](https://github.com/sci-oer/student-cli/issues/29)

**Closed issues:**

- remove test commands [\#30](https://github.com/sci-oer/student-cli/issues/30)

**Merged pull requests:**

- chore!: remove test command: [\#32](https://github.com/sci-oer/student-cli/pull/32) ([MarshallAsch](https://github.com/MarshallAsch))
- chore: Update dependency attrs to v22 [\#26](https://github.com/sci-oer/student-cli/pull/26) ([renovate[bot]](https://github.com/apps/renovate))
- Update actions/setup-python action to v4 [\#25](https://github.com/sci-oer/student-cli/pull/25) ([renovate[bot]](https://github.com/apps/renovate))
- Update actions/checkout action to v3 [\#23](https://github.com/sci-oer/student-cli/pull/23) ([renovate[bot]](https://github.com/apps/renovate))
- Update dependency typing\_extensions to v4.3.0 [\#22](https://github.com/sci-oer/student-cli/pull/22) ([renovate[bot]](https://github.com/apps/renovate))
- Update dependency typer to v0.6.1 [\#21](https://github.com/sci-oer/student-cli/pull/21) ([renovate[bot]](https://github.com/apps/renovate))
- Update dependency black to v22.6.0 [\#20](https://github.com/sci-oer/student-cli/pull/20) ([renovate[bot]](https://github.com/apps/renovate))

## [v0.1.0](https://github.com/sci-oer/student-cli/releases/v0.1.0) (2022-08-01)

[Full Changelog](https://github.com/sci-oer/student-cli/compare/v0.0.1...v0.1.0)

**Implemented enhancements:**

- Release to PyPi [\#1](https://github.com/sci-oer/student-cli/issues/1)

**Merged pull requests:**

- Update dependency pytest to v7.1.2 [\#19](https://github.com/sci-oer/student-cli/pull/19) ([renovate[bot]](https://github.com/apps/renovate))
- Update dependency pyparsing to v3.0.9 [\#18](https://github.com/sci-oer/student-cli/pull/18) ([renovate[bot]](https://github.com/apps/renovate))
- fix: missing dependancies in the test pipeline [\#17](https://github.com/sci-oer/student-cli/pull/17) ([MarshallAsch](https://github.com/MarshallAsch))
- Update dependency platformdirs to v2.5.2 [\#15](https://github.com/sci-oer/student-cli/pull/15) ([renovate[bot]](https://github.com/apps/renovate))
- Update dependency click to v8.1.3 [\#14](https://github.com/sci-oer/student-cli/pull/14) ([renovate[bot]](https://github.com/apps/renovate))
- feat: add pipline to automaticly create and release a new version [\#13](https://github.com/sci-oer/student-cli/pull/13) ([MarshallAsch](https://github.com/MarshallAsch))
- feat: add inital manifest file to prevent too many files from being included [\#12](https://github.com/sci-oer/student-cli/pull/12) ([MarshallAsch](https://github.com/MarshallAsch))
- fix: remove incorrectly commited application config file [\#11](https://github.com/sci-oer/student-cli/pull/11) ([MarshallAsch](https://github.com/MarshallAsch))
- Configure Renovate [\#7](https://github.com/sci-oer/student-cli/pull/7) ([renovate[bot]](https://github.com/apps/renovate))

## [v0.0.1](https://github.com/sci-oer/student-cli/releases/v0.0.1) (2022-04-04)

[Full Changelog](https://github.com/sci-oer/student-cli/compare/d0de775a4608f1aeecebf963071d5bbbb77b3c3f...v0.0.1)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
