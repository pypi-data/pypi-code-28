# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""move_deployment_to_env

Absorbed by dc0fe6de6786 and dc0fe6de6786

Revision ID: 7287df262dbc
Revises: a43700a813a5
Create Date: 2018-01-08 15:16:43.023067

"""

from rally import exceptions

# revision identifiers, used by Alembic.
revision = "7287df262dbc"
down_revision = "a43700a813a5"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    raise exceptions.DowngradeNotSupported()
