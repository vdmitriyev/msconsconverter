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
    "-if",
    "--input-file",
    prompt=False,
    required=False,
    type=click.Path(exists=True),
    help="Path to a single MSCONS file",
)
@click.option(
    "-id",
    "--input-directory",
    prompt=False,
    required=False,
    type=click.Path(exists=True),
    help="Directory with MSCONS data",
)
@click.option(
    "-od",
    "--output-directory",
    prompt=False,
    required=True,
    help="Directory to output CSV file",
)
@click.option("--debug", is_flag=True, show_default=False, default=False, help="Runs in debug mode")
def convert(input_file: str, input_directory: str, output_directory: str, debug: bool):
    """Converts MSCONS (EDIFACT) to CSV"""

    if not (input_file or input_directory):
        raise click.UsageError("At least one of --input_file or --input-directory must be provided.")
    elif input_file and input_directory:
        raise click.UsageError("Only one of --input_file or --input-directory must be provided.")

    _logger, custom_logger = None, CustomLogger()

    if debug:
        _logger = custom_logger.get_logger(logging_level=logging.DEBUG)
    else:
        _logger = custom_logger.get_logger(logging_level=logging.INFO)

    if input_file is not None:
        convert_single(filename=input_file, target_dir=output_directory, logger=_logger)
    elif input_directory is not None:
        convert_batch(directory=input_directory, target_dir=output_directory, logger=_logger)
    else:
        click.echo("No parameters provided. Nothing to convert")


if __name__ == "__main__":
    cli()
