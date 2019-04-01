"""Prepare and render Jinja DOCX template."""
import datetime
import locale
import logging
import math
import os
import typing
from dataclasses import dataclass, asdict
from decimal import Decimal

from docxtpl import DocxTemplate

from invoices.report import Report

DEFAULT_HOURLY_RATE = 10
DATE_FORMAT = '%d %B %Y'

LOGGER = logging.getLogger(__name__)


@dataclass
class Context:
    """Template context."""
    invoice_no: int
    date_en: str
    date_uk: str
    hours: str
    rate: str
    amount: str


def context(
        invoice_number: int,
        report: Report,
        settings: typing.Dict[str, typing.Any]
) -> Context:
    """Prepare template context."""
    hours = math.floor(report.hours)

    today = datetime.date.today()
    date_en = datetime.date.strftime(today, DATE_FORMAT)

    locale.setlocale(locale.LC_TIME, 'uk_UA')
    date_uk = datetime.date.strftime(today, DATE_FORMAT)

    rate = Decimal(settings.get('rate', DEFAULT_HOURLY_RATE))
    LOGGER.info('Using hourly rate: %s', rate)

    return Context(
        invoice_no=invoice_number,
        date_en=date_en,
        date_uk=date_uk,
        hours=str(hours),
        rate=str(rate),
        amount='{:,}'.format(hours * rate)
    )


def render(
        context: Context,   # pylint: disable=redefined-outer-name
        input_filename: str,
        output_filename: str,
        force: bool
) -> None:
    """Render DOCX template using the provided context."""
    if os.path.isfile(output_filename):
        if not force:
            raise RuntimeError(
                'Output location exists: {}'.format(output_filename))

        logging.warning(
            'Output location exists, deleting: %s', output_filename)
        os.remove(output_filename)

    context_dict = asdict(context)
    logging.info(
        'Rendering Invoice template with parameters: %s', context_dict)

    doc = DocxTemplate(input_filename)
    doc.render(context_dict)
    doc.save(output_filename)
