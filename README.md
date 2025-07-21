# acdh-xml-validator


A Python package for validating XML files against RelaxNG and Schematron schemas.
This module provides a Validator class that can validate XML documents using
both RelaxNG (.rng) and Schematron (.sch) schemas, particularly useful for
TEI (Text Encoding Initiative) XML documents.


## Usage (CLI)

### RNG and Schematron
```shell
uv run validate-all --files "data/editions/*.xml" --rng "schemata/rng.rng" --schematron "schemata/schematron.sch"
```

### RNG
```shell
uv run validate-rng --files "data/editions/*.xml" --rng "schemata/rng.rng"
```

### SCHEMATRON
```shell
uv run validate-schematron --files "data/editions/*.xml" --schematron "schemata/schematron.sch"
```


## Usage (Python)

```python
import glob
from acdh_xml_validator import Validator


validator = Validator(
    path_to_rng="schemata/rng.rng",
    path_to_schematon="schemata/schematron.sch"
)

files = glob.glob("data/editions/*.xml")

for x in files:
    valid = validator.validate(x)
```

result:
```shell
test/xmls/L00003.xml is not valid according to test/schemata/rng.rng schema
  - test/xmls/L00003.xml:120:0:ERROR:RELAXNGV:RELAXNG_ERR_ELEMNAME: Expecting element idno, got rs
  - test/xmls/L00003.xml:119:0:ERROR:RELAXNGV:RELAXNG_ERR_ELEMNAME: Expecting element dateline, got signed
  - test/xmls/L00003.xml:119:0:ERROR:RELAXNGV:RELAXNG_ERR_ELEMWRONG: Did not expect element signed there
  - test/xmls/L00003.xml:87:0:ERROR:RELAXNGV:RELAXNG_ERR_ELEMWRONG: Did not expect element p there
  - test/xmls/L00003.xml:119:0:ERROR:RELAXNGV:RELAXNG_ERR_EXTRACONTENT: Element div has extra content: closer
  - test/xmls/L00003.xml:79:0:ERROR:RELAXNGV:RELAXNG_ERR_CONTENTVALID: Element text failed to validate content
test/xmls/L00107.xml is not valid according to test/schemata/tillich-schematron.sch
  - The @ref attribute for rs type @bible must start with a captial letter or with a number
  - The @ref attribute for rs type @bible must start with a captial letter or with a number
  - The @ref attribute for rs type @bible must start with a captial letter or with a number
```

## develop

install the package in editable mode

```shell
uv pip install -e .
uv run python
```

```python
>>> from acdh_xml_validator import hello
>>> hello()
'Hello you from acdh-xml-validator!'
```