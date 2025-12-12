"""
yourpackage.apps

Django looks here for the ManagedAppConfig. It can't be anywhere else.
"""

from authentik.blueprints.apps import ManagedAppConfig
from authentik.tasks.schedules.common import ScheduleSpec


class YourAppConfig(ManagedAppConfig):
  """register into authentik's core for cron"""

  name = "yourpackage.apps"
  label = "yourpackage"
  verbose_name = "Your Package App"
  default = True

  @property
  def tenant_schedule_specs(self) -> list[ScheduleSpec]:
    from yourpackage.apps.tasks import custom_task
    return [
      ScheduleSpec(
        actor=custom_task,
        crontab="0 * * * *",
      )
    ]