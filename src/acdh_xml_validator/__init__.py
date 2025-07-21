"""
ACDH XML Validator

A Python package for validating XML files against RelaxNG and Schematron schemas.
This module provides a Validator class that can validate XML documents using
both RelaxNG (.rng) and Schematron (.sch) schemas, particularly useful for
TEI (Text Encoding Initiative) XML documents.

Example:
    Basic usage with both RelaxNG and Schematron validation:

    >>> validator = Validator(
    ...     path_to_rng="schema.rng",
    ...     path_to_schematron="rules.sch",
    ...     verbose=True
    ... )
    >>> is_valid = validator.validate("document.xml")
"""

from pathlib import Path

import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader
from pyschematron import validate_document
from pyschematron.utils import load_xml_document


def hello() -> str:
    """Return a greeting message from the acdh-xml-validator package.

    Returns:
        str: A greeting message.
    """
    return "Hello you from acdh-xml-validator!"


class Validator:
    """XML Validator for RelaxNG and Schematron schemas.

    A validator class that can validate XML documents against both RelaxNG (.rng)
    and Schematron (.sch) schemas. Designed to work with TEI XML documents but
    can be used with any XML format.

    Attributes:
        relaxng_schema: The loaded RelaxNG schema object, or False if not provided.
        path_to_rng (str|bool): Path to the RelaxNG schema file, or False if not provided.
        schematron_schema: The loaded Schematron schema object, or False if not provided.
        path_to_schematron (str|bool): Path to the Schematron schema file, or False if not provided.
        verbose (bool): Whether to print detailed validation messages.

    Example:
        >>> # Validate against both RelaxNG and Schematron
        >>> validator = Validator(
        ...     path_to_rng="schema.rng",
        ...     path_to_schematron="rules.sch"
        ... )
        >>> is_valid = validator.validate("document.xml")

        >>> # Validate against RelaxNG only
        >>> rng_validator = Validator(path_to_rng="schema.rng")
        >>> is_valid = rng_validator.validate_against_rng("document.xml")
    """

    def __init__(self, path_to_rng=None, path_to_schematron=None, verbose=True):
        """Initialize the Validator with schema files.

        Args:
            path_to_rng (str, optional): Path to the RelaxNG schema file (.rng).
                If None, RelaxNG validation will be skipped.
            path_to_schematron (str, optional): Path to the Schematron schema file (.sch).
                If None, Schematron validation will be skipped.
            verbose (bool, optional): Whether to print detailed validation messages
                and errors. Defaults to True.

        Raises:
            FileNotFoundError: If the specified schema files don't exist.
            ET.XMLSyntaxError: If the schema files are not valid XML.
        """
        if path_to_rng:
            rng_path = Path(path_to_rng)
            with open(rng_path, "r") as rng_file:
                rng_doc = ET.parse(rng_file)
            relaxng_schema = ET.RelaxNG(rng_doc)
            self.relaxng_schema = relaxng_schema
            self.path_to_rng = path_to_rng
        else:
            self.path_to_rng = False
        if path_to_schematron:
            schematron_path = Path(path_to_schematron)
            schematron_schema = load_xml_document(schematron_path)
            self.schematron_schema = schematron_schema
            self.path_to_schematron = path_to_schematron
        else:
            self.schematron_schema = False
            self.path_to_schematron = False
        self.verbose = verbose

    def validate_against_rng(self, path_to_xml_file: str) -> bool:
        """Validate an XML file against the RelaxNG schema.

        Args:
            path_to_xml_file (str): Path to the XML file to validate.

        Returns:
            bool: True if the XML file is valid according to the RelaxNG schema,
                False otherwise. Also returns False if no RelaxNG schema was provided
                during initialization or if the XML file cannot be parsed.

        Note:
            If verbose is True, validation errors will be printed to stdout.
        """
        if not self.relaxng_schema:
            print("No RNG file path provided")
            return False
        try:
            doc = TeiReader(path_to_xml_file).tree
        except Exception as e:
            if self.verbose:
                print(f"failed to parse {path_to_xml_file} due to {e}")
            return False
        relaxng_valid = self.relaxng_schema.validate(doc)
        if not relaxng_valid:
            if self.verbose:
                print(
                    f"{path_to_xml_file} is not valid according to {self.path_to_rng} schema"
                )
            if self.verbose:
                for error in self.relaxng_schema.error_log:
                    print(f"  - {error}")
        return relaxng_valid

    def validate_against_schematron(self, path_to_xml_file: str) -> bool:
        """Validate an XML file against the Schematron schema.

        Args:
            path_to_xml_file (str): Path to the XML file to validate.

        Returns:
            bool: True if the XML file is valid according to the Schematron schema,
                False otherwise. Also returns False if no Schematron schema was provided
                during initialization or if the XML file cannot be parsed.

        Note:
            If verbose is True, validation errors will be printed to stdout.
            Schematron validation provides more detailed semantic validation rules
            compared to RelaxNG's structural validation.
        """
        if not self.schematron_schema:
            print("No schematron file path provided")
            return False
        try:
            doc = TeiReader(path_to_xml_file).tree
        except Exception as e:
            if self.verbose:
                print(f"failed to parse {path_to_xml_file} due to {e}")
            return False
        result = validate_document(doc, self.schematron_schema)
        schematron_valid = result.is_valid()
        if self.verbose and not schematron_valid:
            print(
                f"{path_to_xml_file} is not valid according to {self.path_to_schematron}"
            )
            report = result.get_svrl()
            for x in report.xpath(
                ".//svrl:text", namespaces={"svrl": "http://purl.oclc.org/dsdl/svrl"}
            ):
                error = x.text
                print(f"  - {error}")
        return schematron_valid

    def validate(self, path_to_xml_file: str) -> bool:
        """Validate an XML file against both RelaxNG and Schematron schemas.

        This method runs both RelaxNG and Schematron validation on the XML file.
        The file is considered valid only if it passes both validation checks
        (or if only one type of schema is provided, it must pass that check).

        Args:
            path_to_xml_file (str): Path to the XML file to validate.

        Returns:
            bool: True if the XML file is valid according to all provided schemas,
                False otherwise. If no schemas were provided during initialization,
                this will always return False.

        Note:
            This method calls both validate_against_rng() and validate_against_schematron().
            If verbose is True, detailed validation messages will be printed for both
            validation steps.
        """
        rng_valid = self.validate_against_rng(path_to_xml_file)
        schematron_valid = self.validate_against_schematron(path_to_xml_file)
        if rng_valid and schematron_valid:
            return True
        else:
            return False
