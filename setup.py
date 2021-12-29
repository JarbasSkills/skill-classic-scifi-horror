#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-classic-scifi-horror.jarbasai=skill_classic_scifi_horror:ClassicScifiHorrorSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-classic-scifi-horror',
    version='0.0.1',
    description='ovos classic scifi horror skill plugin',
    url='https://github.com/JarbasSkills/skill-classic-scifi-horror',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_classic_scifi_horror": ""},
    package_data={'skill_classic_scifi_horror': ['locale/*', 'ui/*']},
    packages=['skill_classic_scifi_horror'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
