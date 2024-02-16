#!/usr/bin/env python

import logging
import sys
from sys import platform

import click

from msconsconverter.functions import convert_batch, convert_single
from msconsconverter.logger import CustomLogger


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--file",
    prompt=False,
    required=False,
    type=click.Path(exists=True),
    help="Path to a single MSCONS file",
)
@click.option(
    "--directory",
    prompt=False,
    required=False,
    type=click.Path(exists=True),
    help="Directory with MSCONS data",
)
@click.option(
    "--output-directory",
    prompt=False,
    required=True,
    help="Directory to output CSV file",
)
@click.option("--debug", is_flag=True, show_default=False, default=False, help="Runs in debug mode")
def convert(file: str, directory: str, output_directory: str, debug: bool):
    """MSCONS (EDIFACT) format converter (to CSV)"""

    if not (file or directory):
        raise click.UsageError("At least one of --file or --directory must be provided.")
    elif file and directory:
        raise click.UsageError("Only one of --file or --directory must be provided.")

    _logger, custom_logger = None, CustomLogger()

    if debug:
        _logger = custom_logger.get_logger(logging_level=logging.DEBUG)
    else:
        _logger = custom_logger.get_logger(logging_level=logging.INFO)

    if file is not None:
        convert_single(filename=file, target_dir=output_directory, logger=_logger)
    elif directory is not None:
        convert_batch(directory=directory, target_dir=output_directory, logger=_logger)
    else:
        click.echo("No parameters provided. Nothing to convert")


if __name__ == "__main__":
    cli()
