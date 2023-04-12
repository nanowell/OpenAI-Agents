import dis
import logging
import struct
import sys
import time
from enum import Enum
from types import CodeType
from typing import Union


class AssemblyFormat(Enum):
    DEFAULT = "default"
    EXTENDED = "extended"
    CUSTOM = "custom"


def disassemble_file(file_path: str, asm_format: AssemblyFormat = AssemblyFormat.DEFAULT) -> None:
    """
    Disassemble a compiled Python file.

    Args:
        file_path: The path to the compiled Python file.
        asm_format: The format of the disassembled code. Valid values are DEFAULT, EXTENDED, and CUSTOM.

    Raises:
        ValueError: If the file is not a .pyc or .pyo file.
        FileNotFoundError: If the file does not exist.

    """
    if not file_path.endswith((".pyc", ".pyo")):
        raise ValueError("Invalid file format: must be a .pyc or .pyo file")

    try:
        with open(file_path, "rb") as f:
            magic = f.read(4)
            timestamp = f.read(4)
            code = __import__("marshal").load(f)
    except FileNotFoundError:
        logging.exception("File not found: %s", file_path)
        raise
    except Exception as error:
        logging.exception("Error loading compiled file: %s", error)
        raise

    disassemble_code(code, asm_format)


def disassemble_source(source: str, asm_format: AssemblyFormat = AssemblyFormat.DEFAULT) -> None:
    """
    Disassemble a string of Python source code.

    Args:
        source: The Python source code to disassemble.
        asm_format: The format of the disassembled code. Valid values are DEFAULT, EXTENDED, and CUSTOM.

    """
    try:
        code = compile(source, "<string>", "exec")
    except Exception as error:
        logging.exception("Error compiling source: %s", error)
        raise

    disassemble_code(code, asm_format)


def disassemble_object(code_object: CodeType, asm_format: AssemblyFormat = AssemblyFormat.DEFAULT) -> None:
    """
    Disassemble a pre-compiled code object.

    Args:
        code_object: The pre-compiled code object to disassemble.
        asm_format: The format of the disassembled code. Valid values are DEFAULT, EXTENDED, and CUSTOM.

    """
    disassemble_code(code_object, asm_format)


def print_code_info(code_object: CodeType) -> None:
    """
    Print information about a code object.

    Args:
        code_object: The code object to print information about.

    """
    print(f"Code object header information for {code_object.co_name}:")
    print(f"Number of arguments: {code_object.co_argcount}")
    print(f"Number of local variables: {code_object.co_nlocals}")
    print(f"Number of constants: {len(code_object.co_consts)}")
    print(f"Number of names: {len(code_object.co_names)}")
    print(f"Number of free variables: {len(code_object.co_freevars)}")
    print(f"Number of cell variables: {len(code_object.co_cellvars)}")
    print(f"Flags: {pretty_flags(code_object)}")


def pretty_flags(code_object: CodeType) -> str:
    """
    Get a string representation of the flags set on a code object.

    Args:
        code_object: The code object to get flags for.

    Returns:
        A string representation of the flags set on the code object.

    """
    flags = []
    for flag_name, flag_value in dis.COMPILER_FLAG_NAMES.items():
        if code_object.co_flags & flag_value:
            flags.append(flag_name)
    return ", ".join(flags)


def disassemble_code(code_object: CodeType, asm_format: AssemblyFormat = AssemblyFormat.DEFAULT) -> None:
    """
    Disassemble a code object.

    Args:
        code_object: The code object to disassemble.
        asm_format: The format of the disassembled code. Valid values are DEFAULT, EXTENDED, and CUSTOM.

    Raises:
        ValueError: If an invalid asm_format is specified.

    """
    if asm_format == AssemblyFormat.DEFAULT:
        try:
            dis.disassemble(code_object)
        except Exception as error:
            logging.exception("Error disassembling code: %s", error)
            raise

    elif asm_format == AssemblyFormat.EXTENDED:
        print(f"Disassembly of {code_object.co_filename} ({code_object.co_firstlineno}:{code_object.co_lnotab}):")
        print(f"Python version: {struct.unpack('H', code_object.co_version[:2])[0]}.{code_object.co_version[2]}")
        print(f"Timestamp: {time.asctime(time.localtime(struct.unpack('i', code_object.co_mtime)[0]))}")
        print(f"Magic: {code_object.co_magic}")
        try:
            dis.Bytecode(code_object).dis(sys.stdout)
        except Exception as error:
            logging.exception("Error disassembling code: %s", error)
            raise

    elif asm_format == AssemblyFormat.CUSTOM:
        print("Custom disassembly format not implemented yet")
        # TODO: Implement custom disassembly format

    else:
        raise ValueError(f"Invalid asm_format: {asm_format}")


def main() -> None:
    """
    Parse command line arguments and run the appropriate disassembly function.

    """
    import argparse

    parser = argparse.ArgumentParser(description="Disassemble Python bytecode")
    parser.add_argument("input", help="The input file, source code, or code object to disassemble")
    parser.add_argument("--format", "-f", choices=[format_type.value for format_type in AssemblyFormat],
                        default=AssemblyFormat.DEFAULT.value, help="The format of the disassembled code")
    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            source = f.read()
        disassemble_source(source, AssemblyFormat(args.format))
    except FileNotFoundError:
        try:
            disassemble_file(args.input, AssemblyFormat(args.format))
        except ValueError:
            disassemble_object(eval(args.input), AssemblyFormat(args.format))
    except Exception:
        logging.exception("Error disassembling input: %s", args.input)
        raise


if __name__ == "__main__":
    main()
