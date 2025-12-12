"""
yourpackage.apps.tasks

i'm pretty sure i had to put my actors here for it to work, but i may be wrong
"""

from dramatiq import actor
from authentik.tasks.middleware import CurrentTask
from django.utils.translation import gettext_lazy as _

@actor(description=_("Custom Task"))
def custom_task():
    self = CurrentTask.get_task()
    self.info("Running your custom task!")