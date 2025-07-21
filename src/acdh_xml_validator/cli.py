"""Command-line interface for acdh-xml-validator.

This module provides CLI commands for validating XML files against RelaxNG and
Schematron schemas. Three commands are available:

- validate-all: Validate against both RelaxNG and Schematron schemas
- validate-rng: Validate against RelaxNG schema only
- validate-schematron: Validate against Schematron schema only

All commands support glob patterns for batch validation and provide progress bars
for multiple files.
"""

import glob
import sys

import click
from tqdm import tqdm

from . import Validator


@click.group()
@click.version_option()
def cli():
    """XML Validator CLI - Validate XML files against RelaxNG and Schematron schemas.

    This tool validates XML files against schema files to ensure they conform to
    defined structural and rule-based constraints. Particularly useful for
    TEI (Text Encoding Initiative) XML documents.
    """
    pass


@click.command()
@click.option(
    "--files",
    default="data/editions/*.xml",
    required=True,
    help="Glob expression to the XML files.",
    type=str,
)
@click.option(
    "--rng",
    default="schemata/rng.rng",
    required=True,
    help="Path to the RNG file.",
    type=str,
)
@click.option(
    "--schematron",
    default="schemata/schematron.sch",
    required=True,
    help="Path to the Schematron file.",
    type=str,
)
def validate_all(files: str, rng: str, schematron: str) -> None:
    """Validate XML files against both RelaxNG and Schematron schemas.

    This command validates XML files against both RelaxNG (.rng) and Schematron (.sch)
    schemas. Files must pass both validation checks to be considered valid.

    Args:
        files: Glob pattern for XML files to validate (e.g., "data/*.xml")
        rng: Path to the RelaxNG schema file (.rng)
        schematron: Path to the Schematron schema file (.sch)

    Exit codes:
        0: All files are valid
        1: One or more files failed validation
    """
    files = glob.glob(files)
    validator = Validator(path_to_rng=rng, path_to_schematron=schematron)
    results = set()
    for x in tqdm(files):
        results.add(validator.validate(x))
    if False in results:
        click.echo(click.style("ERRORS!!!!", fg="red"))
        sys.exit(1)
    else:
        click.echo(click.style("All good!", fg="green"))


@click.command()
@click.option(
    "--files",
    default="data/editions/*.xml",
    required=True,
    help="Path to the XML file to validate.",
    type=str,
)
@click.option(
    "--rng",
    default="schemata/rng.rng",
    required=True,
    help="Path to the RNG file.",
    type=str,
)
def validate_rng(files: str, rng: str) -> None:
    """Validate XML files against RelaxNG schema only.

    This command validates XML files against a RelaxNG (.rng) schema for
    structural validation. Schematron validation is skipped.

    Args:
        files: Glob pattern for XML files to validate (e.g., "data/*.xml")
        rng: Path to the RelaxNG schema file (.rng)

    Exit codes:
        0: All files are valid according to RelaxNG schema
        1: One or more files failed RelaxNG validation
    """
    files = glob.glob(files)
    validator = Validator(path_to_rng=rng)
    results = set()
    for x in tqdm(files):
        results.add(validator.validate_against_rng(x))
    if False in results:
        click.echo(click.style("ERRORS!!!!", fg="red"))
        sys.exit(1)
    else:
        click.echo(click.style("All good!", fg="green"))


@click.command()
@click.option(
    "--files",
    default="data/editions/*.xml",
    required=True,
    help="Path to the XML file to validate.",
    type=str,
)
@click.option(
    "--schematron",
    default="schemata/schematron.sch",
    required=True,
    help="Path to the Schematron file.",
    type=str,
)
def validate_schematron(files: str, schematron: str) -> None:
    """Validate XML files against Schematron schema only.

    This command validates XML files against a Schematron (.sch) schema for
    rule-based validation. RelaxNG validation is skipped.

    Args:
        files: Glob pattern for XML files to validate (e.g., "data/*.xml")
        schematron: Path to the Schematron schema file (.sch)

    Exit codes:
        0: All files are valid according to Schematron schema
        1: One or more files failed Schematron validation
    """
    files = glob.glob(files)
    validator = Validator(path_to_schematron=schematron)
    results = set()
    for x in tqdm(files):
        results.add(validator.validate_against_schematron(x))
    if False in results:
        click.echo(click.style("ERRORS!!!!", fg="red"))
        sys.exit(1)
    else:
        click.echo(click.style("All good!", fg="green"))
