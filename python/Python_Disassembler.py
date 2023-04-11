import dis
import struct
import time
import traceback
import logging
import sys
from types import CodeType
from typing import Union


def disassemble_file(file_name: str, asm_format: str = "default") -> None:
    if not file_name.endswith(".py"):
        raise ValueError("Invalid file format: must be a .py file")

    try:
        with open(file_name, "rb") as f:
            magic = f.read(4)
            timestamp = f.read(4)
            code = marshal.load(f)
    except Exception as error:
        logging.exception("Error loading compiled file: %s", error)
        raise

    dis_code(code, asm_format)


def disassemble_source(source: str, asm_format: str = "default") -> None:
    try:
        code = compile(source, "<string>", "exec")
    except Exception as error:
        logging.exception("Error compiling source: %s", error)
        raise

    dis_code(code, asm_format)


def disassemble_object(obj: CodeType, asm_format: str = "default") -> None:
    dis_code(obj, asm_format)


def code_info(code: CodeType) -> None:
    print(f"Code object header information for {code.co_name}:")
    print(f"Number of arguments: {code.co_argcount}")
    print(f"Number of local variables: {code.co_nlocals}")
    print(f"Number of constants: {len(code.co_consts)}")
    print(f"Number of names: {len(code.co_names)}")
    print(f"Number of free variables: {len(code.co_freevars)}")
    print(f"Number of cell variables: {len(code.co_cellvars)}")
    print(f"Flags: {pretty_flags(code)}")


def pretty_flags(code: CodeType) -> str:
    flags = []
    for flag, value in dis.COMPILER_FLAG_NAMES.items():
        if code.co_flags & value:
            flags.append(flag)
    return ", ".join(flags)


def get_opcode() -> type[dis.Instruction]:
    """Get the opcode module based on the version of Python and whether it is PyPy or not."""
    if hasattr(dis, "Bytecode"):
        # Python 3.6 and above
        return dis.Bytecode
    elif hasattr(dis, "opcode"):
        # Python 2.x or PyPy
        return dis.opcode
    else:
        raise RuntimeError("Unsupported Python version")


def dis_code(code: CodeType, asm_format: str = "default") -> None:
    if asm_format == "default":
        try:
            dis.disassemble(code)
        except Exception as error:
            logging.exception("Error disassembling code: %s", error)
            raise

    elif asm_format == "extended":
        print(f"Disassembly of {code.co_filename} ({code.co_firstlineno}:{code.co_lnotab}):")
        print(f"Python version: {struct.unpack('H', code.co_version[:2])[0]}.{code.co_version[2]}")
        print(f"Timestamp: {time.asctime(time.localtime(struct.unpack('i', code.co_mtime)[0]))}")
        print(f"Magic: {code.co_magic}")
        try:
            get_opcode().dis(code, None, sys.stdout.write)
        except Exception as error:
            logging.exception("Error disassembling code: %s", error)
            raise

    elif asm_format == "custom":
        print("Custom disassembly format not implemented yet")
        # TODO: Implement custom disassembly format

    else:
        raise ValueError(f"Invalid asm_format: {asm_format}")



if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        disassemble_file(sys.argv[1])
    elif len(sys.argv) == 3:
        disassemble_file(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python Untitled-1.py <file> [asm_format]")
        print("asm_format: default, extended, custom")
