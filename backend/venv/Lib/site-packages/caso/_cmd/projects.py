# -*- coding: utf-8 -*-

# Copyright 2014 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from oslo_config import cfg
from oslo_log import log

import caso.config
import caso.manager

cli_opts = [
    cfg.BoolOpt(
        "migrate-projects",
        default=False,
        help="Migrate also the project list to Keystone tags (i.e. stop using the "
        "'projects' option in the configuration file).",
    ),
]

CONF = cfg.CONF
CONF.register_cli_opts(cli_opts)


def migrate():
    """Migrate cASO VO file mapping to Keystone-based configuration."""
    caso.config.parse_args(sys.argv)
    log.setup(cfg.CONF, "caso")

    CONF.set_default("dry_run", True)
    manager = caso.manager.Manager()
    if CONF.dry_run:
        print(
            "WARNING: Running in 'dry-run' mode, no actions will be peformed. If you "
            "want to apply the changes, run with '--nodry-run'. Be aware that in "
            "that case the cASO user will need write access to Keystone. If unsure "
            "run the following commands as admin."
        )

    manager._load_managers()
    for prj, vo in manager.extractor_manager.voms_map.items():
        if CONF.dry_run:
            print(f"openstack project set --property {CONF.vo_property}={vo} {prj}")
        else:
            try:
                kw = {CONF.vo_property: vo}
                manager.extractor_manager.keystone.projects.update(prj, **kw)
            except Exception as e:
                print(f"ERROR: could not add property for project {prj}.")
                print(f"ERROR: {e}")

    if CONF.migrate_projects:
        for prj in CONF.projects:
            if CONF.dry_run:
                print(f"openstack project set --tag {CONF.caso_tag} {prj}")
            else:
                try:
                    project = manager.extractor_manager.keystone.projects.get(prj)
                    project.add_tag(CONF.caso_tag)
                except Exception as e:
                    print(f"ERROR: could not add tag for project {prj}.")
                    print(f"ERROR: {e}")


def main():
    """Get cASO configured projects."""
    caso.config.parse_args(sys.argv)
    log.setup(cfg.CONF, "caso")
    manager = caso.manager.Manager()
    for prj, vo in manager.projects_and_vos():
        prj_name = None
        try:
            prj_name = manager.extractor_manager.keystone.projects.get(prj).name
        except Exception as e:
            print(f"ERROR: Could not get project {prj}")
            print(f"ERROR: {e}")

        print(f"'{prj} ({prj_name}) mapped to VO '{vo}'")


if __name__ == "__main__":
    main()
