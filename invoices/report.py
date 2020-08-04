"""Fetch summary report from Toggl."""
import datetime
import logging
import pprint
import typing
from dataclasses import dataclass
from decimal import Decimal

from toggl.api_client import TogglClientApi

LOGGER = logging.getLogger(__name__)


@dataclass
class Report:
    """Excerpt from Toggl report."""
    hours: Decimal


def fetch(
        settings: typing.Dict[str, typing.Any],
        since: datetime.date,
        until: datetime.date
) -> Report:
    """Fetch Toggle report."""
    LOGGER.info(
        'Fetching Toggl summary report: since=%s, until=%s, workspace_id=%s',
        since, until, settings.get('workspace_id')
    )

    client = TogglClientApi(settings)

    params = settings
    params.pop('token')
    params['since'] = str(since)
    params['until'] = str(until)
    params['grouping'] = 'projects'
    params['subgrouping'] = 'time_entries'

    response = client.query_report('/summary', params=params)
    response_data = response.json()

    if response.status_code != 200:
        raise RuntimeError(
            'Cannot fetch Toggl report: {}'.format(response_data))

    LOGGER.debug('Response: %s', pprint.pformat(response_data))

    total_grand = response_data['total_grand']
    if not total_grand:
        raise RuntimeError('Toggl returned no data: {}'.format(response_data))

    hours = Decimal(total_grand) / Decimal(1_000 * 60 * 60)
    report = Report(hours=hours)
    LOGGER.info('Fetched report: %s', report)

    return report
