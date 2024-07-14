#!/usr/bin/env python

import logging
import sys
from sys import platform

import click
import typer

from msconsconverter.functions import convert_batch, convert_single
from msconsconverter.logger import CustomLogger

app = typer.Typer()


@app.command()
def convert(
    convert: str = typer.Argument(
        ...,
        help="Argument to convert MSCONS (EDIFACT)",
    ),
    input_file: str = typer.Option(None, prompt=False, help="Path to a single MSCONS file"),
    input_directory: str = typer.Option(None, prompt=False, help="Directory with MSCONS data"),
    output_directory: str = typer.Option(None, help="Directory to output CSV file"),
    debug: bool = typer.Option(False, is_flag=True, show_default=False, help="Runs in debug mode"),
):
    # Your conversion logic here
    # Access arguments using function parameters
    #  - input_file
    #  - input_directory
    #  - output_directory
    #  - debug

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
        pass
        # tuper.echo("No parameters provided. Nothing to convert")


if __name__ == "__main__":
    app()
