"""Main module."""
import argparse
import datetime
import logging
import tempfile

import toml

from invoices import template, report
from invoices.export import export_docx

LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Script entry-point."""
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--invoice', type=int, required=True,
                        help='Invoice number')
    parser.add_argument('-t', '--template-id', required=True,
                        help='Template document ID')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Overwrite output if it exists')
    args = parser.parse_args()

    today = datetime.date.today()
    start = today.replace(day=1)
    until = start - datetime.timedelta(days=1)
    since = until.replace(day=1)

    LOGGER.info('Generating last month''s invoice')

    config = toml.load('invoices.toml')
    rep = report.fetch(config['toggl'], since=since, until=until)
    context = template.context(args.invoice, rep, config['invoice'])

    with tempfile.TemporaryDirectory() as tmp_dirname:
        filename = export_docx(args.template_id, tmp_dirname)
        template.render(context, filename, args.output, args.force)

    LOGGER.info('Done')


if __name__ == '__main__':
    main()
